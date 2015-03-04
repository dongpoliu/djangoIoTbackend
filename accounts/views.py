# -*- coding: UTF-8 -*-
import logging
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.views.generic import FormView
from django.template import RequestContext
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.translation import ugettext_lazy as _
from axes.decorators import watch_login
from braces.views import LoginRequiredMixin
from core.utils import airdetectordata_by_unit_setting, to_mg
from .models import UserSettings
from .forms import UserSettingsForm, SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
import urlparse

logger = logging.getLogger(__name__)

@csrf_exempt 
@watch_login
def login_view(request):
    # Force logout.
    logout(request)
    username = password = ''

    # Flag to keep track whether the login was invalid.
    login_failed = False

    if request.POST:
        username = request.POST['username'].replace(' ', '').lower()
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
        else:
            login_failed = True

    return render_to_response('accounts/login.html', {'login_failed': login_failed},context_instance=RequestContext(request))


class SignUpView(FormView):
    success_url = '/dashboard/'
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    @csrf_exempt 
    def get_initial(self):
        # Force logout.
        logout(self.request)

        return {'time_zone': settings.TIME_ZONE}

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.full_clean()

        if form.is_valid():
            username = form.cleaned_data['username'].replace(' ', '').lower()
            password = form.cleaned_data['password']
            user = User.objects.create(username=username)
            user.email = form.cleaned_data['email']
            user.set_password(password)
            user.save()

            # Create an entry for the User Settings.
            user_settings = UserSettings.objects.create(user=user)
            user_settings.airdetectordata_unit = form.cleaned_data['airdetectordata_unit']
            user_settings.time_zone = form.cleaned_data['time_zone']
            user_settings.save()

            logger.info('New user signed up: %s (%s)', user, user.email)

            # Automatically authenticate the user after user creation.
            user_auth = authenticate(username=username, password=password)
            login(request, user_auth)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class UserSettingsView(LoginRequiredMixin, FormView):
    success_url = '.'
    form_class = UserSettingsForm
    template_name = 'accounts/usersettings.html'
 
    def get_initial(self):
        user = self.request.user
        settings = user.settings

        return {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'time_zone': settings.time_zone,
            'province': settings.province,
            'city': settings.city,
            'districtcounty': settings.districtcounty,            
            'address': settings.address,            
            'airdetectordata_unit': settings.airdetectordata_unit,
            'default_category': settings.default_category,
            'airdetectordata_low': airdetectordata_by_unit_setting(user, settings.airdetectordata_low),
            'airdetectordata_high': airdetectordata_by_unit_setting(user, settings.airdetectordata_high),
            'airdetectordata_target_min': airdetectordata_by_unit_setting(user, settings.airdetectordata_target_min),
            'airdetectordata_target_max': airdetectordata_by_unit_setting(user, settings.airdetectordata_target_max),
        }

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Settings Saved!')

        return super(UserSettingsView, self).form_valid(form)
   
    @method_decorator(csrf_protect)
    @csrf_exempt         
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.full_clean()

        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            user.settings.time_zone = form.cleaned_data['time_zone']
            address                             = form.cleaned_data['address']            
            user.settings.address     = address
            province                           = form.cleaned_data['province']      
            user.settings.province   = province            
            city                                    = form.cleaned_data['city']     
            user.settings.city            = city
            districtcounty                  = form.cleaned_data['districtcounty']   
            user.settings.districtcounty  = districtcounty
            airdetectordata_unit            = form.cleaned_data['airdetectordata_unit']
            user.settings.airdetectordata_unit = airdetectordata_unit
            user.settings.default_category = form.cleaned_data['default_category']
            airdetectordata_low = form.cleaned_data['airdetectordata_low']
            airdetectordata_high = form.cleaned_data['airdetectordata_high']
            airdetectordata_target_min = form.cleaned_data['airdetectordata_target_min']
            airdetectordata_target_max = form.cleaned_data['airdetectordata_target_max']

            # If user's airdetectordata unit setting is set to mmol/L, convert the
            # values to mg/dL.
            if airdetectordata_unit.name == 'mmol/L':
                airdetectordata_low = to_mg(airdetectordata_low)
                airdetectordata_high = to_mg(airdetectordata_high)
                airdetectordata_target_min = to_mg(airdetectordata_target_min)
                airdetectordata_target_max = to_mg(airdetectordata_target_max)

            user.settings.airdetectordata_low = airdetectordata_low
            user.settings.airdetectordata_high = airdetectordata_high
            user.settings.airdetectordata_target_min = airdetectordata_target_min
            user.settings.airdetectordata_target_max = airdetectordata_target_max
            user.settings.save()

            logger.info('Account Settings updated by %s', user)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)
