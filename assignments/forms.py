from django import forms
from django.core.exceptions import ValidationError

class UpdateAssignmentForm(forms.Form):
    grade = forms.IntegerField()
    
    def clean_grade(self):
        grade = self.cleaned_data.get('grade')
        if grade < 0:
            raise ValidationError('Invalid grade - grades cannot be less than 0')
        return grade
