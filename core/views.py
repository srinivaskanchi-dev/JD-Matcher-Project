from django.shortcuts import render
from django.http import HttpResponse
from .forms import ResumeMatchForm
from .models import UserInput, ResumeResult
import pdfplumber
from .utils import (
    compute_match_score,
    generate_ats_resume,
    generate_interview_questions,
    generate_explanation
)
import json
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse
import io

# Utility function to extract text from PDF
def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = "\n".join(page.extract_text() or '' for page in pdf.pages)
    return text

# Main view for uploading resume and job description
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeMatchForm(request.POST, request.FILES)
        if form.is_valid():
            # Extract resume text
            resume_text = form.cleaned_data['resume_text']
            if not resume_text and form.cleaned_data['resume_file']:
                resume_file = form.cleaned_data['resume_file']
                if resume_file.name.lower().endswith('.pdf'):
                    resume_text = extract_text_from_pdf(resume_file)
                else:
                    resume_text = resume_file.read().decode('utf-8', errors='ignore')
            jd_text = form.cleaned_data['jd_text']
            # Compute match score
            match_score = compute_match_score(resume_text, jd_text)
            # Generate ATS resume
            ats_resume = generate_ats_resume(resume_text, jd_text)
            # session for PDF download
            request.session['optimized_resume'] = ats_resume
            # Generate interview questions
            interview_questions = generate_interview_questions(resume_text, jd_text, num_questions=7)
            # Generate explanation
            explanation = generate_explanation(resume_text, jd_text, match_score)
            # Save user input and result
            user_input = UserInput.objects.create(
                resume_text=resume_text,
                jd_text=jd_text,
                match_score=match_score
            )
            ResumeResult.objects.create(
                user_input=user_input,
                ats_resume=ats_resume,
                interview_questions=json.dumps(interview_questions),
                explanation=explanation
            )
            # Render result page with all info
            return render(request, 'core/result.html', {
                'user_input': user_input,
                'ats_resume': ats_resume,
                'match_score': match_score,
                'interview_questions': interview_questions,
                'explanation': explanation
            })
    else:
        form = ResumeMatchForm()
    return render(request, 'core/upload.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('upload_resume')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def download_ats_resume(request, user_input_id):
    """Serve the ATS resume as a downloadable text file."""
    try:
        result = ResumeResult.objects.get(user_input_id=user_input_id)
    except ResumeResult.DoesNotExist:
        return HttpResponse("Resume not found.", status=404)
    response = HttpResponse(result.ats_resume, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=ATS_Resume_{user_input_id}.txt'
    return response
def download_pdf(request):
    resume_text = request.session.get('optimized_resume', 'No resume found')
    html = render_to_string('pdf_template.html', {'optimized_resume': resume_text})

    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=ATS_Resume.pdf'
        return response
    else:
        return HttpResponse('PDF generation failed')
