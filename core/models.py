from django.db import models
from django.shortcuts import render
from django.contrib.auth.models import User
# Create your models here.

class UserInput(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_text = models.TextField(help_text="Extracted text from the uploaded resume (PDF or text)")
    jd_text = models.TextField(help_text="Job description text pasted by the user")
    upload_time = models.DateTimeField(auto_now_add=True)
    match_score = models.FloatField(null=True, blank=True, help_text="TF-IDF + Cosine Similarity score")

    def __str__(self):
        return f"UserInput {self.id} - {self.upload_time}"

class ResumeResult(models.Model):
    user_input = models.OneToOneField(UserInput, on_delete=models.CASCADE, related_name="result")
    ats_resume = models.TextField(help_text="ATS-friendly, customized resume")
    interview_questions = models.TextField(help_text="Generated interview Q&A (JSON or plain text)")
    explanation = models.TextField(help_text="Plain English explanation of the match")

    def __str__(self):
        return f"ResumeResult for UserInput {self.user_input.id}"
    
class ChatLog(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat by {self.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"



