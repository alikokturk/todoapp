from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    """Giriş formu."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring focus:ring-primary focus:ring-opacity-50'})
        self.fields['password'].widget.attrs.update({'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring focus:ring-primary focus:ring-opacity-50'})

class CustomUserCreationForm(UserCreationForm):
    """Kullanıcı oluşturma formu."""
    
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'w-full rounded-md border-gray-300'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'w-full rounded-md border-gray-300'})
        self.fields['password2'].widget.attrs.update({'class': 'w-full rounded-md border-gray-300'})
        
        # Yardım metinlerini düzenle
        for field in self.fields:
            self.fields[field].help_text = self.fields[field].help_text.replace('<ul>', '<ul class="text-xs text-gray-500 list-disc ml-4 mt-1">')

class CustomAuthenticationForm(AuthenticationForm):
    """Kullanıcı giriş formu."""
    
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full rounded-md border-gray-300'}))

class UserProfileForm(forms.ModelForm):
    """Kullanıcı profil güncelleme formu."""
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_image')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300'}),
            'email': forms.EmailInput(attrs={'class': 'w-full rounded-md border-gray-300'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300'}),
            'profile_image': forms.FileInput(attrs={'class': 'w-full border border-gray-300 rounded-md py-2 px-3'}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    """Şifre değiştirme formu."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'w-full rounded-md border-gray-300'})
        self.fields['new_password1'].widget.attrs.update({'class': 'w-full rounded-md border-gray-300'})
        self.fields['new_password2'].widget.attrs.update({'class': 'w-full rounded-md border-gray-300'})
        
        # Yardım metinlerini düzenle
        for field in self.fields:
            if self.fields[field].help_text:
                self.fields[field].help_text = self.fields[field].help_text.replace('<ul>', '<ul class="text-xs text-gray-500 list-disc ml-4 mt-1">')

class CustomPasswordResetForm(PasswordResetForm):
    """Şifre sıfırlama formu."""
    
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'w-full rounded-md border-gray-300'})
    )

class CustomSetPasswordForm(SetPasswordForm):
    """Yeni şifre belirleme formu."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'w-full rounded-md border-gray-300'})
        self.fields['new_password2'].widget.attrs.update({'class': 'w-full rounded-md border-gray-300'})
        
        # Yardım metinlerini düzenle
        for field in self.fields:
            if self.fields[field].help_text:
                self.fields[field].help_text = self.fields[field].help_text.replace('<ul>', '<ul class="text-xs text-gray-500 list-disc ml-4 mt-1">') 