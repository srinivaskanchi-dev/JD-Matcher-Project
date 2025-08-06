from django.db import models
from django.shortcuts import render

# Create your models here.

class UserInput(models.Model):
    resume_text = models.TextField(help_text="Extracted text from the uploaded resume (PDF or text)")
    jd_text = models.TextField(help_text="Job description text pasted by the user")
    upload_time = models.DateTimeField(auto_now_add=True)
    match_score = models.FloatField(null=True, blank=True, help_text="TF-IDF + Cosine Similarity score")

    def __str__(self):
        return f"UserInput {self.id} - {self.upload_time}"  # For admin display

class ResumeResult(models.Model):
    user_input = models.OneToOneField(UserInput, on_delete=models.CASCADE, related_name="result")
    ats_resume = models.TextField(help_text="ATS-friendly, customized resume")
    interview_questions = models.TextField(help_text="Generated interview Q&A (JSON or plain text)")
    explanation = models.TextField(help_text="Plain English explanation of the match")

    def __str__(self):
        return f"ResumeResult for UserInput {self.user_input.id}"  # For admin display

