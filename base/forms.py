from django import forms
import datetime as dt
from django.db.models import fields
from django.forms import ModelForm
from django.forms.fields import DateTimeField
from django.forms.widgets import DateInput, DateTimeInput, PasswordInput
from .models import Attendants, Feedbacks, Offers, Profiles
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField

#OFFER FORMS
class OffersForm(ModelForm):
    class Meta:
        model = Offers
        TIMES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]
        fields =['title', 'description', 'picture', 'hashtags', 'location', 'date', 'time', 'credits', 'numberOfParticipants', 'type']
        widgets = {
            'date': DateTimeInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'type': 'date',
                'placeholder': 'date'
                }),
            'time': forms.Select(choices=TIMES, attrs={'class': "form-control", 
            'style': 'max-width: 300px;', 
            'type': 'time',
            'placeholder': 'time'})
        }
        

#USER CREATION FORM
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

#PROFILE EDIT FORM
class ProfileEdit(ModelForm):
    class Meta:
        model = Profiles
        fields = ['name', 'surname', 'email', 'password', 'interests', 'picture' ]
        widgets = {
            'password': PasswordInput()
        }

#APPROVAL FORMS
class ApproveForm(ModelForm):
    class Meta:
        model = Attendants
        fields = ['status']

#ATTENDEE STATUS FORMS
class AttendeeForm(ModelForm):
    class Meta:
        model = Attendants
        fields = ['offerstatus']

#STATUS FORMS
class StatusForm(ModelForm):
    class Meta:
        model = Offers
        fields =  ['eventstatus']

#FEEDBACK FORMS
class FeedbackForm(ModelForm):
    class Meta:
        model = Feedbacks
        fields =  ['value', 'body']

