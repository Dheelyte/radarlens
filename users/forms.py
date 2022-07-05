from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Invalid Login Details')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password')

    class Meta:
        model = User
        fields = [
            'name',
            'email',
            'password',
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        email_check = User.objects.filter(email=email)
        if email_check.exists():
            raise forms.ValidationError('This Email already exists')
        if len(password) < 5:
            raise forms.ValidationError('Your password should have more than 5 characters')
        return super(UserRegisterForm, self).clean(*args, **kwargs)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'name',
            'email',
        ]

class UserThumbnailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'image',
        ]

class VerifyUserEmail(forms.Form):
    email = forms.EmailField()
    class Meta:
        fields = ['email',]
