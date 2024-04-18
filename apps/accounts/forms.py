from django import forms
from django.forms.widgets import TextInput, PasswordInput, EmailInput
from .models import User, UserResetPasswordCode
from django.contrib.auth.forms import PasswordResetForm
from apps.base.utilits import VerifyEmailCode


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': "Username..."}), required=True)
    email = forms.CharField(widget=TextInput(attrs={'placeholder': "email..."}), required=True)
    first_name = forms.CharField(widget=TextInput(attrs={'placeholder': "first_name..."}), required=True)
    last_name = forms.CharField(widget=TextInput(attrs={'placeholder': "last_name..."}), required=True)
    phone = forms.CharField(widget=TextInput(attrs={'placeholder': "phone..."}), required=True)

    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': "password..."}), required=True)
    confirm_password = forms.CharField(widget=PasswordInput(attrs={'placeholder': "confirm_password..."}), required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("Bu email oldin ro'yxatdan o'tgan")

        return email
    
    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')

        if password1 != password2:
            raise forms.ValidationError("Parollar bir biriga mos emas!!!")

        return password2

    def save(self, commit=True):
        password = self.cleaned_data.get('password')

        user = super().save(commit)
        user.set_password(password)
        user.save()

        return user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=EmailInput(attrs={'placeholder': "Email..."}), required=True)
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': "password..."}), required=False)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if not email or not password:
            raise forms.ValidationError("Bo'sh bo'lmasligi lozim")

        return self.cleaned_data


class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'photo')


class CustomPasswordResetForm(forms.ModelForm):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}))

    class Meta:
        model = UserResetPasswordCode
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bunday email bo'yicha hech kim ro'yxatdan o'tmagan")

        return email

    def get_code(self):
        coder = VerifyEmailCode()
        code = coder.new_code()
        return code

    def save(self, commit=True):
        code = self.get_code()
        verify_code = super().save(commit)
        verify_code.code = code
        verify_code.save()
        return verify_code


class CustomCheckVerifyCodeForm(forms.Form):
    code = forms.CharField(widget=TextInput(attrs={'placeholder': "code..."}), required=True)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not code or not code.isdigit() or len(code) != 6:
            raise forms.ValidationError("Noto'g'ri tekshiruv kodi")

        return code


class CustomPasswordResetConfirmForm(forms.Form):
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': "password..."}), required=True)
    confirm_password = forms.CharField(widget=PasswordInput(attrs={'placeholder': "confirm_password..."}), required=True)

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if password1 != password2:
            raise forms.ValidationError("Parollar bir biriga mos emas!!!")

        return password2

