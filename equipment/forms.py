from django import forms
from datetime import date
from .models import Item
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Div, Field, Row, Column

class ItemBookingForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            "equipment",
            "ICON_ref",
            'brand',
            'model_spec',
            'location',
            'current_user',
            'borrow_date',
            'return_date',
            'asset_number',
            'serial_number',
            'value',
            'PAT',
            'comments'
        ]

    equipment       = forms.CharField(disabled=True)
    ICON_ref        = forms.CharField(disabled=True)
    brand           = forms.CharField(disabled=True)
    model_spec      = forms.CharField(disabled=True)  
    borrow_date     = forms.DateField(widget=forms.SelectDateWidget(), initial=date.today)
    return_date     = forms.DateField(widget=forms.SelectDateWidget(), initial=date.today)
    asset_number    = forms.CharField(disabled=True, required=False)
    serial_number   = forms.CharField(disabled=True, required=False)
    location        = forms.CharField(required=False)
    value           = forms.CharField(disabled=True, required=False)
    PAT             = forms.DateField(disabled=True, required=False)
    current_user    = forms.EmailField(required=False)
    comments        = forms.TextInput()
    db_user         = forms.HiddenInput()

class ItemCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('equipment', css_class='form-group col-md-3 mb-0'),
                Column('ICON_number', css_class='form-group col-md-3 mb-0'),
                Column('location', css_class='form-group col-md-3 mb-0'),
            css_class='form-row'),
            Row(
                Column('current_user', css_class='form-group col-md-3 mb-0'),
                Column('borrow_date', css_class='form-group col-md-3 mb-0'),
                Column('return_date', css_class='form-group col-md-3 mb-0'),
            css_class='form-row'),
            Row(
                Column('asset_number', css_class='form-group col-md-3 mb-0'),
                Column('serial_number', css_class='form-group col-md-3 mb-0'),
                Column('value', css_class='form-group col-md-3 mb-0'),
                Column('PAT', css_class='form-group col-md-3 mb-0'),
            css_class='form-row'),
            Row(
                Column('comments', css_class='form-group col-md-3 mb-0'),
            css_class='form-row'),
    )
    
    class Meta:
        model = Item
        fields = [
            "equipment",
            "ICON_ref",
            'brand',
            'model_spec',
            'location',
            'current_user',
            'asset_number',
            'serial_number',
            'value',
            'PAT',
            'comments'
        ]

    equipment       = forms.CharField()
    ICON_ref        = forms.CharField()
    brand           = forms.CharField()
    model_spec      = forms.CharField()
    asset_number    = forms.CharField(required=False)
    serial_number   = forms.CharField(required=False)
    location        = forms.CharField(required=True, initial="storeroom")
    value           = forms.CharField(required=False)
    PAT             = forms.DateField(required=False)
    current_user    = forms.EmailField(required=False)
    comments        = forms.TextInput()
    db_user         = forms.HiddenInput()