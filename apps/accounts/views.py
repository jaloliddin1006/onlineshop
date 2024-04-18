from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import RegisterUserForm, LoginForm, UpdateUserForm, CustomPasswordResetForm, CustomCheckVerifyCodeForm, CustomPasswordResetConfirmForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from apps.base.utilits import send_mail_code
from apps.base.utilits import VerifyEmailCode

from django.urls import reverse_lazy

from django.utils.encoding import smart_bytes

from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator


from .models import User, UserResetPasswordCode


class UserRegisterView(View):
    form_class = RegisterUserForm

    def get(self, request):
        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request):
        user_form = self.form_class(data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Tizimdam muvaffaqiyatli ro'yxatdan o'tdingiz.")
            return redirect('index_url')
        
        messages.error(request, "Tizindan ro'yxatdan o'ta olmadingiz!!!")
        context = {
            'form': user_form
        }
        return render(request, 'accounts/register.html', context)


class LoginView(View):
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, 'accounts/login.html', context)

    def post(self, request):
        user_form = self.form_class(data=request.POST)
        if user_form.is_valid():
            user = authenticate(request, email=user_form.cleaned_data['email'], password=user_form.cleaned_data['password'])

            if user is not None:
                login(request, user)
                messages.success(request, "Siz tizimga muvaffaqiyatli kirdingiz.")
                return redirect('index_url')

            messages.error(request, "Login yoki parol noto'g'ri!!!!")
            return render(request, 'accounts/login.html', {'form':user_form})

        messages.error(request, user_form.errors)
        return render(request, 'accounts/login.html', {'form': user_form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('index_url')


class UpdateUserView(View):
    form_class = UpdateUserForm

    def get(self, request):
        form = self.form_class(instance=request.user)
        context = {
            'form': form
        }

        return render(request, 'accounts/update-profile.html', context)

    def post(self, request):
        user_form = self.form_class(data=request.POST, files=request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()

            messages.success(request, "Muvaffaqiyatli yangilandi.")
            return redirect('index_url')

        messages.error(request, user_form.errors)
        return render(request, 'accounts/update-profile.html', {'form': user_form})



class CustomPasswordResetView(View):
    form_class = CustomPasswordResetForm

    def get(self, request):
        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, 'accounts/password_reset_form.html', context)

    def post(self, request):
        user_form = self.form_class(data=request.POST)

        if user_form.is_valid():
            verify = user_form.save()
            send_mail_code(verify.email, verify.code)
            messages.success(request, "Yangi code Yuborildi")
            return redirect('accounts:check-verify', uuid=verify.private_id)
        return render(request, 'accounts/password_reset_form.html', {'form': user_form})


class CustomCheckVerifyCodeView(View):
    form_class = CustomCheckVerifyCodeForm

    def get(self, request, uuid):
        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, 'accounts/password_reset_check_verify_code.html', context)

    def post(self, request, uuid):
        code_form = self.form_class(request.POST)
        if code_form.is_valid():
            print(code_form.cleaned_data)
            print(uuid)
            code = code_form.cleaned_data['code']
            user_code = UserResetPasswordCode.objects.filter(private_id=uuid, expiration_time__gte=datetime.now(), code=code, is_confirmation=False).first()
            print(user_code)
            if user_code:

                user_code.is_confirmation = True
                user_code.save()

                messages.success(request, "tekshiruvdan o'tdi endi yangi parolingizni kiriting")
                return redirect('accounts:password-reset-confirm', uuid=uuid)

            messages.error(request, "tekshiruv kodi notog'ri yoki eskirgan ")
            return render(request, 'accounts/password_reset_check_verify_code.html', {'form': code_form})

        messages.error(request, code_form.errors)
        return render(request, 'accounts/password_reset_check_verify_code.html', {'form': code_form})


class CustomPasswordResetConfirmView(View):
    form_class = CustomPasswordResetConfirmForm

    def get(self, request, uuid):
        form = self.form_class()
        is_confirmation = UserResetPasswordCode.objects.filter(private_id=uuid, expiration_time__gte=datetime.now(), is_confirmation=True).first()

        if not is_confirmation:
            messages.error(request, "bu url yaroqsiz")
            return redirect('accounts:password-reset')

        context = {
            'form': form
        }
        return render(request, 'accounts/password_reset_confirm.html', context)

    def post(self, request, uuid):
        password_reset_form = self.form_class(request.POST)
        if password_reset_form.is_valid():
            email = UserResetPasswordCode.objects.get(private_id=uuid)
            user = User.objects.get(email=email.email)
            password = password_reset_form.cleaned_data['password']
            user.set_password(password)
            user.save()

            messages.success(request, 'Parolingiz muvaffaqiyatli yangilandi')
            return render(request, 'accounts/password_reset_complete.html')

        context = {
            'form': password_reset_form
        }
        messages.error(request, password_reset_form.errors)
        return render(request, 'accounts/password_reset_confirm.html', context)

