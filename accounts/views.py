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
from core.utils import glucose_by_unit_setting, to_mg

from .models import UserSettings
from .forms import UserSettingsForm, SignUpForm

from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
import urlparse

logger = logging.getLogger(__name__)

class LoginView(FormView):
    """
    This is a class based version of django.contrib.auth.views.login.


    """
    form_class = AuthenticationForm
    redirect_field_name = '/map'
    template_name = 'accounts/login.html'


    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        can check the test cookie stuff and log him in.
        """
        self.check_and_delete_test_cookie()
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        self.extend_template="base.html"
        context['extend_template']=self.extend_template
        return context    

    def form_invalid(self, form):
        """
        The user has provided invalid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        set the test cookie again and re-render the form with errors.
        """
        self.set_test_cookie()
        return super(LoginView, self).form_invalid(form)

    def get_success_url(self):
        if self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')

        netloc = urlparse.urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        # Security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = settings.LOGIN_REDIRECT_URL
        return redirect_to

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.get(), but adds test cookie stuff
        """
        self.set_test_cookie()
        return super(LoginView, self).get(request, *args, **kwargs)

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
                #return HttpResponseRedirect('/dashboard/')
                return HttpResponseRedirect('/map/')            
        else:
            login_failed = True

    return render_to_response('accounts/login.html', {'login_failed': login_failed},context_instance=RequestContext(request))


class SignUpView(FormView):
    success_url = '/map/'
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def get_initial(self):
        # Force logout.
        logout(self.request)

        return {'time_zone': settings.TIME_ZONE}

    @csrf_exempt     
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
            #user_settings.glucose_unit = form.cleaned_data['glucose_unit']
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
            #'glucose_unit': settings.glucose_unit,
            #'default_category': settings.default_category,
            #'glucose_low': glucose_by_unit_setting(user, settings.glucose_low),
            #'glucose_high': glucose_by_unit_setting(user, settings.glucose_high),
            #'glucose_target_min': glucose_by_unit_setting(user, settings.glucose_target_min),
            #'glucose_target_max': glucose_by_unit_setting(user, settings.glucose_target_max),
        }

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Settings Saved!')

        return super(UserSettingsView, self).form_valid(form)

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

            #glucose_unit = form.cleaned_data['glucose_unit']
            #user.settings.glucose_unit = glucose_unit

            #user.settings.default_category = form.cleaned_data['default_category']

            #glucose_low = form.cleaned_data['glucose_low']
            #glucose_high = form.cleaned_data['glucose_high']
            #glucose_target_min = form.cleaned_data['glucose_target_min']
            #glucose_target_max = form.cleaned_data['glucose_target_max']

            # If user's glucose unit setting is set to mmol/L, convert the
            # values to mg/dL.
            #if glucose_unit.name == 'mmol/L':
                #glucose_low = to_mg(glucose_low)
                #glucose_high = to_mg(glucose_high)
                #glucose_target_min = to_mg(glucose_target_min)
                #glucose_target_max = to_mg(glucose_target_max)

            #user.settings.glucose_low = glucose_low
            #user.settings.glucose_high = glucose_high
            #user.settings.glucose_target_min = glucose_target_min
            #user.settings.glucose_target_max = glucose_target_max
            user.settings.save()

            logger.info('Account Settings updated by %s', user)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)
