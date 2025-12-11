from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder": "Enter your email"}))
    phone = forms.CharField(max_length=15,widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your phonr number"}))
    desc = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "rows":3, "placeholder": "How my we help you..?"}))