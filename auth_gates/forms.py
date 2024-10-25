from django import forms
from django.forms import ModelForm
from captcha.fields import ReCaptchaField
from django.contrib.auth.models import User
from captcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# create a class that inherits from the UserCreationForm. We will name our
# class UserForm.
class RegistrationForm(UserCreationForm):
    
    first_name = forms.CharField()
    
    last_name = forms.CharField()
    
    email = forms.EmailField(required=True)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        # To indicate which model we are using which in this case is the
        # default user model
        model = User
        # To show which fields we want to include in our final form and what
        # order they should be rendered on our page.
        fields = ('first_name', 'last_name', 'username', 'email', 'password1',
                  'password2', 'captcha')


class UserLoginForm(AuthenticationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
