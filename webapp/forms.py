from django import forms
from .models import Property


class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property
        exclude = ['publish_date','approved_date','approver','publisher','is_approved','is_active']
