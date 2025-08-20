from django import forms
from django_select2.forms import Select2MultipleWidget
from django.forms import inlineformset_factory
from .models import ProfileModel, PostModel, PostImage, User

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(
        label = "Password",
        widget =  forms.PasswordInput,
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
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        if username:
            User.objects.filter(username=username, is_active=False).delete()
        if email:
            User.objects.filter(email=email, is_active=False).delete()
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('User with this email already exists')
        return email


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['first_name', 'last_name', 'gender', 'avatar', 'birth_date', 'bio']
        gender = forms.ChoiceField(choices = model.GENDER_CHOICES)
        birth_date = forms.DateField(
            widget=forms.DateInput(attrs={'type': 'date'})
        )

    def __str__(self):
        return f"{self.cleaned_data.get('first_name', '')} {self.cleaned_data.get('last_name', '')}"


class LoginForm(forms.Form):
    username = forms.CharField(widget = forms.TextInput())
    password = forms.CharField(widget = forms.PasswordInput())
    remember = forms.BooleanField(required = False)


class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['text', 'tags']
        widgets = {
            'tags': Select2MultipleWidget(attrs = {
                'data-placeholder': 'Choose tags...',
                'style': 'width: 100%;',
                'class': 'select2-chips'
            }),
        }


class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['image']

PostImageFormSet = inlineformset_factory(PostModel, PostImage, form = PostImageForm, extra = 3, can_delete = False)

class RestorePasswordForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    email = forms.EmailField(label='Email')