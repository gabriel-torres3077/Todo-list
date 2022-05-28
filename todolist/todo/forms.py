from django import forms
from .models import Todo


class DateInput(forms.DateTimeInput):
    input_type = 'date'

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = [
            'title', 'description', 'important', 'goal'
        ]
        widgets = {
            'goal': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }
            )
        }