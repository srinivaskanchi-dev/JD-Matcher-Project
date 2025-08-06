from django import forms

class ResumeMatchForm(forms.Form):
    resume_file = forms.FileField(
        required=False,
        label="Upload Resume (PDF or Text)",
        help_text="Upload your resume as a PDF or plain text file."
    )
    resume_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 6}),
        label="Or Paste Resume Text",
        help_text="Paste your resume text here if not uploading a file."
    )
    jd_text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 6}),
        label="Paste Job Description",
        help_text="Paste the job description here."
    )

    def clean(self):
        cleaned_data = super().clean()
        resume_file = cleaned_data.get("resume_file")
        resume_text = cleaned_data.get("resume_text")
        if not resume_file and not resume_text:
            raise forms.ValidationError("Please upload a resume file or paste resume text.")
        return cleaned_data 