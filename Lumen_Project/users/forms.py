from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Wymagane. Podaj poprawny adres email.')

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        """
        Walidacja sprawdzająca, czy email nie jest już zajęty.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Użytkownik z tym adresem email już istnieje.")
        return email