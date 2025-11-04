from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib import messages

from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm,
    CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm
)
from .models import User

class CustomLoginView(LoginView):
    """Özelleştirilmiş giriş view'ı."""
    
    template_name = 'accounts/login.html'
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('boards:list')
    
    def form_valid(self, form):
        """Giriş başarılı olduğunda mesaj göster."""
        messages.success(self.request, 'Başarıyla giriş yaptınız.')
        return super().form_valid(form)

class RegisterView(CreateView):
    """Kullanıcı kayıt view'ı."""
    
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('boards:list')
    
    def form_valid(self, form):
        """Kullanıcı oluşturulduktan sonra otomatik giriş yap."""
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Hesabınız başarıyla oluşturuldu ve giriş yaptınız.')
        return response

class ProfileView(LoginRequiredMixin, DetailView):
    """Kullanıcı profil görüntüleme view'ı."""
    
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        """Mevcut kullanıcıyı döndür."""
        return self.request.user

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Kullanıcı profil güncelleme view'ı."""
    
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        """Mevcut kullanıcıyı döndür."""
        return self.request.user
    
    def form_valid(self, form):
        """Form başarıyla doğrulandığında mesaj göster."""
        messages.success(self.request, 'Profiliniz başarıyla güncellendi.')
        return super().form_valid(form)

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Özelleştirilmiş şifre değiştirme view'ı."""
    
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('accounts:profile')
    
    def form_valid(self, form):
        """Form başarıyla doğrulandığında mesaj göster."""
        messages.success(self.request, 'Şifreniz başarıyla değiştirildi.')
        return super().form_valid(form)

class CustomPasswordResetView(PasswordResetView):
    """Özelleştirilmiş şifre sıfırlama view'ı."""
    
    template_name = 'accounts/password_reset.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    
    def form_valid(self, form):
        """Form başarıyla doğrulandığında mesaj göster."""
        messages.success(self.request, 'Şifre sıfırlama talimatları e-posta adresinize gönderildi.')
        return super().form_valid(form)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Özelleştirilmiş şifre sıfırlama onay view'ı."""
    
    template_name = 'accounts/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete') 