from django import forms
from .models import Profile, PostModel
from django.core.validators import MinLengthValidator

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(
        label = "Password",
        widget=  forms.PasswordInput,
    #     validators = [MinLengthValidator(6, message="Password must be at least 6 characters long.")
    # ]
    )
    confirm_password = forms.CharField(
        label = "Confirm Password",
        widget = forms.PasswordInput
    )


#validaion
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'gender', 'avatar', 'birth_date', 'bio']
        gender = forms.ChoiceField(choices=model.GENDER_CHOICES)
        birth_date = forms.DateField(
            widget=forms.DateInput(attrs={'type': 'date'})  # Устанавливаем тип date для браузера
        )

    def __str__(self):
        return f"{self.cleaned_data.get('first_name', '')} {self.cleaned_data.get('last_name', '')}"


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    remember = forms.BooleanField(required=False)

class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['text', 'image']
