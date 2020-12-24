from django import forms

class Register(forms.Form):
    fullname=forms.CharField(min_length=6)
    username=forms.CharField(min_length=6)
    email=forms.EmailField()
    phones=forms.CharField(min_length=10)
    password=forms.CharField(min_length=6)