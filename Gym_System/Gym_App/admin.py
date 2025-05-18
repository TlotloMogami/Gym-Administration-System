from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'gender', 'dob', 'membership_type', 'status', 'joined', 'email', 'phone', 'address']
