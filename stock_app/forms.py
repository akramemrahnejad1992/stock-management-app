from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class StockDataForm(forms.Form):
    symbol = forms.CharField(label='Stock Symbol', max_length=10)
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))
    period = forms.ChoiceField(label='Period', choices=[
        ('1d', '1 Day'),
        ('5d', '5 Days'),
        ('1mo', '1 Month'),
        ('3mo', '3 Months'),
        ('6mo', '6 Months'),
        ('1y', '1 Year'),
        ('2y', '2 Years'),
        ('5y', '5 Years'),
        ('ytd', 'Year to Date'),
        ('max', 'Max'),
    ])
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # Check if end_date is after start_date
        if start_date and end_date:
            if end_date <= start_date:
                raise ValidationError('End date must be after start date.')