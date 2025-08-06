from django import forms
# core/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class StyledRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(StyledRegisterForm, self).__init__(*args, **kwargs)

        # Email field
        self.fields['username'].label = "Email ID"
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter your Email ID',
            'class': 'w-full px-4 py-3 rounded-lg bg-gray-300 text-gray-800 border border-gray-400 placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-gray-200 transition'
        })

        # Password
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Create a password',
            'class': 'w-full px-4 py-3 pr-12 rounded-lg bg-gray-300 text-gray-800 border border-gray-400 placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-gray-200 transition'
        })

        # Confirm Password
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Re-enter your password',
            'class': 'w-full px-4 py-3 pr-12 rounded-lg bg-gray-300 text-gray-800 border border-gray-400 placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-gray-200 transition'
        })
class StyledLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(StyledLoginForm, self).__init__(*args, **kwargs)

        cement_style = (
            "w-full px-4 py-3 rounded-lg bg-gray-300 text-gray-800 "
            "border border-gray-400 placeholder-gray-600 "
            "focus:outline-none focus:ring-2 focus:ring-emerald-500 transition"
        )

        self.fields['username'].label = "Email ID"
        self.fields['username'].widget.attrs.update({
            'class': cement_style,
            'placeholder': 'Enter your Email ID'
        })

        self.fields['password'].widget.attrs.update({
            'class': cement_style,
            'placeholder': 'Enter your password'
        })

class ResumeMatchForm(forms.Form):
    resume_file = forms.FileField(
        required=False,
        label="Upload Resume (PDF or Text)",
        help_text="Upload your resume as a PDF or plain text file."
    )
    resume_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 6}),
        initial='',
        label="Or Paste Resume Text",
        help_text="Paste your resume text here if not uploading a file."
    )
    jd_text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 6}),
        initial='',
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