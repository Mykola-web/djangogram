from django import forms
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

    # Валидация на совпадение пароля
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

class EditProfileForm(forms.Form):
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length=20)
    gender = forms.ChoiceField()
    avatar = forms.ImageField(allow_empty_file = True)
    bio = forms.CharField(max_length = 500)
    birth_date = forms.DateField()