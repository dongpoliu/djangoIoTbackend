# -*- coding: UTF-8 -*-
from django import forms
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Button, Submit, Fieldset, HTML, Field
from crispy_forms.bootstrap import FormActions
from timezone_field import TimeZoneFormField
from chineseaddress.models import AddressField ,Country ,  Province ,  City , DistrictCounty , VillageTown, Address
from django.utils.translation import ugettext_lazy as _
from air.models import Category, Unit
from .validators import validate_email_unique, validate_username_unique
from .util import PROVINCE_CHOICES

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=30, validators=[validate_username_unique])
    password = forms.CharField(max_length=128, widget=forms.PasswordInput())
    email = forms.EmailField(max_length=75, validators=[validate_email_unique])
    airdetectordata_unit = forms.ModelChoiceField(Unit.objects.all(), empty_label=None,label='AirDetectorData Unit')
    time_zone = TimeZoneFormField(label=_(u'时区'))
    address  = forms.CharField(max_length=60)
    province  = forms.CharField(label=_(u'省份'),  required = True, widget=forms.Select(choices=PROVINCE_CHOICES)) 

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal col-xs-12 col-md-6 col-lg-5'
        self.helper.label_class = 'col-xs-4 col-md-4 col-lg-4'
        self.helper.field_class = 'col-xs-8 col-md-8 col-lg-8'

        self. helper.layout = Layout(
            Fieldset(
                'Create Your Account',
                Field('username', autofocus=True),
                Field('password'),
                Field('email'),
                Field('airdetectordata_unit'),
                Field('time_zone'),
                Field('province'),
                Field('address'),                
            ),
            FormActions(
                Submit('submit', 'Create My Account',css_class='btn-success pull-right'),
            ),
        )

class UserSettingsForm(forms.Form):
    """
    Form to allow users to change profile settings and preferences.
    """
    username = forms.CharField(required=False)
    first_name = forms.CharField(label=_(u'名') , required=False)
    last_name = forms.CharField(label=_(u'姓') , required=False)
    email = forms.EmailField(label='Email')
    time_zone = TimeZoneFormField(label=_(u'时区') )     
    #villagetown  = forms.ModelChoiceField(VillageTown.objects.all(), empty_label=None, label=_(u'乡镇街道') )      
    province                      = forms.ModelChoiceField(Province.objects.all(), empty_label=None, label=_(u'省份'))     
    city                               = forms.ModelChoiceField(City.objects.all(), empty_label=None, label=_(u'城市'))
    districtcounty              = forms.ModelChoiceField(DistrictCounty.objects.all(), empty_label=None, label=_(u'区县'))
    #province  = forms.CharField(label=_(u'省份'),  required = True, widget=forms.Select(choices=PROVINCE_CHOICES))
    address  = forms.CharField(label=_(u'地址'), required=True, help_text=_(u'地址格式：上海市 闵行区 银都路3399弄457号'))    
    airdetectordata_unit = forms.ModelChoiceField( Unit.objects.all(), label='AirDetectorData Unit', empty_label=None)
    default_category = forms.ModelChoiceField( Category.objects.all(), label='Default Category',empty_label='Auto', required=False)

    airdetectordata_low = forms.DecimalField( label='Low', max_digits=6, max_value=3000, min_value=0, help_text="Below this value is a low AirDetectorData.")
    airdetectordata_high = forms.DecimalField( label='High', max_digits=6, max_value=3000, min_value=0, help_text="Above this value is a high AirDetectorData.")
    airdetectordata_target_min = forms.DecimalField( label='Target Min', max_digits=6, max_value=3000, min_value=0, help_text="Your target range's minimum value.")
    airdetectordata_target_max = forms.DecimalField( label='Target Max', max_digits=6, max_value=3000, min_value=0, help_text="Your target range's maximum value.")

    def __init__(self, *args, **kwargs):
        super(UserSettingsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal col-xs-12 col-md-6 col-lg-6'
        self.helper.label_class = 'col-xs-4 col-md-4 col-lg-4'
        self.helper.field_class = 'col-xs-8 col-md-8 col-lg-8'
        self.helper.help_text_inline = False

        self. helper.layout = Layout(
            HTML('''
            {% if messages %}
            {% for message in messages %}
            <p {% if message.tags %} class="alert alert-{{ message.tags }}"\
            {% endif %}>{{ message }}</p>{% endfor %}{% endif %}
            </p>
            '''),
            Fieldset(
                _(u'个人信息'),
                Field('username', readonly=True),
                Field('email'),
                Field('first_name'),
                Field('last_name'),
                Field('time_zone'),
                #Field('villagetown'),          
                Field('province'),        
                Field('city'),
                Field('districtcounty'),        
                Field('address'),
            ),
            Fieldset(
                _(u'参数选择'),
                Field('airdetectordata_unit'),
                Field('default_category'),
            ),
            Fieldset(
                _(u'AirDectorData 范围设置'),
                Field('airdetectordata_low'),
                Field('airdetectordata_high'),
                Field('airdetectordata_target_min'),
                Field('airdetectordata_target_max'),
            ),
            FormActions(
                Submit('submit', 'Save'),
                Button('cancel', 'Cancel', onclick='location.href="%s";' % reverse('map')),
            ),
        )

    def clean_email(self):
        """
        Validates the email field.

        Check if the email field changed. If true, check whether the new email
        address already exists in the database and raise an error if it does.
        """
        email = self.cleaned_data['email']
        user = User.objects.get(username=self.cleaned_data['username'])

        if email.lower() != user.email.lower():
            if User.objects.filter(email__iexact=email):
                raise forms.ValidationError('Another account is already using '  'this email address.')

        return email
