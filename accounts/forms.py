from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


User = get_user_model()


INPUT_CLASSES = 'w-full rounded-2xl border border-slate-700 bg-slate-950/90 px-4 py-3 text-slate-100 placeholder:text-slate-500 focus:border-slate-500 focus:outline-none focus:ring-2 focus:ring-slate-600'


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email',
                'autocomplete': 'email',
                'class': INPUT_CLASSES,
            }
        )
    )

    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'autocomplete': 'new-password',
                'class': INPUT_CLASSES,
            }
        ),
    )

    password2 = forms.CharField(
        label='Password confirmation',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm password',
                'autocomplete': 'new-password',
                'class': INPUT_CLASSES,
            }
        ),
    )

    class Meta:
        model = User
        fields = ('email',)


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'autofocus': True,
                'autocomplete': 'email',
                'class': INPUT_CLASSES,
            }
        ),
    )
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'class': INPUT_CLASSES,
            }
        ),
    )

    class Meta:
        model = User
        fields = ('username', 'password')
