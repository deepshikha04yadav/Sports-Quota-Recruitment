from django import forms

class CandidateRegistrationForm(forms.Form):
    fname = forms.CharField(max_length=30)
    lname = forms.CharField(max_length=30)
    email = forms.EmailField()
    number = forms.CharField(max_length=10)
    age = forms.IntegerField()
    dob = forms.DateField()
    gender = forms.ChoiceField(choices=[('female', 'Female'), ('male', 'Male'), ('other', 'Other')])
    photo = forms.ImageField(required=False)
    transaction_no = forms.IntegerField()
    document = forms.FileField()
