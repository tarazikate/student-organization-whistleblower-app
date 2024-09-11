from django import forms
from django.core.exceptions import ValidationError

class UploadFileForm(forms.Form):

    """cite from chatgpt"""

    question_1 = forms.MultipleChoiceField(
        choices=[
            ('option1', 'Hazing'),
            ('option2', 'Sexual Misconduct'),
            ('option3', 'Verbal Abuse'),
            ('option4', 'Physical Abuse'),
            ('option5', 'Substance Abuse'),
            ('option6', 'Discrimination'),
            ('other', 'Other'),
        ],
        required=True,
        widget=forms.CheckboxSelectMultiple
    )


    # Organizations involved
    question_2 = forms.ChoiceField(
        choices=[
            ('', '---------'),
            ('option1', 'None'),
            ('option2', 'Fraternity'),
            ('option3', 'Sorority'),
            ('option4', 'Academic Club'),
            ('option5', 'Non-Academic Club'),
            ('option6', 'Sports'),
            ('option7', 'Societies'),
            ('other', 'Other'),
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    #Who was involved
    question_3 = forms.CharField(widget=forms.TextInput, required=True)
    #Injuries
    question_4 = forms.CharField(widget=forms.TextInput, required=True)
    # Time/ Date
    question_5 = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control datetimepicker-input',  # Ensures Bootstrap styling
            'id': 'datetimepicker'  # You can specify an ID for targeting with JavaScript or CSS if needed
        }),
        input_formats=['%Y-%m-%dT%H:%M'],  # Make sure to match the format expected by HTML datetime-local
        required=False
    )
    #explain incident
    additional_info = forms.CharField(widget=forms.Textarea, required=True)
    #upload a file
    file = forms.FileField(required=False)
    def clean_file(self):
        file = self.cleaned_data['file']
        if file is not None:
            if not (file.name.endswith('.pdf') or file.name.endswith('.txt') or file.name.endswith('.jpg')):
                raise ValidationError("Only pdf, txt, or jpg files are allowed.")
        return file