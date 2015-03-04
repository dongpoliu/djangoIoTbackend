# -*- coding: UTF-8 -*-
import json
import logging
import operator
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext
from django.views.generic import (
    CreateView,
    DeleteView,
    FormView,
    TemplateView,
    UpdateView,
)
from braces.views import LoginRequiredMixin
from django_datatables_view.base_datatable_view import BaseDatatableView
from core.utils import airdetectordata_by_unit_setting, to_mg
from .utils import get_initial_category, import_airdetectordata_from_csv
from .models import AirCleaner, AirDetectorData, AirDetector
from .reports import AirDetectorDataCsvReport, AirDetectorDataPdfReport, ChartData, UserStats
from .forms import (
    #AirCleanerCreateForm,
    #AirCleanerUpdateForm,
    AirDetectorDataCreateForm,
    AirDetectorDataUpdateForm,    
    AirDetectorDataEmailReportForm,
    AirDetectorDataFilterForm,
    AirDetectorDataQuickAddForm,
    AirDetectorDataImportForm,    
)

DATE_FORMAT = '%m/%d/%Y'
TIME_FORMAT = '%I:%M %p'

logger = logging.getLogger(__name__)

@login_required
def map (request):
    user = request.user
    airdetectors = AirDetector.objects.filter(owner__username=request.user)
    #markers = Marker.objects.filter(device__name=user).order_by('name')

    ctx = {
            'airdetectors': airdetectors,
            #'markers':markers,
        }        
    
    return render_to_response('air/map.html', ctx, context_instance=RequestContext(request))

@login_required
def import_data(request):
    if request.method == 'POST':
        form = AirDetectorDataImportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                logger.info('Importing data from uploaded CSV file for user: %s',
                            request.user)
                import_airdetectordata_from_csv(request.user, request.FILES['file'])
            except ValueError, e:
                logger.error('Could not import data from uploaded CSV file for' ' user: %s. Details: %s', request.user, e)
                message = 'Could not import your data. Make sure that it follows' ' the suggested format. (Error Details: %s)' % e
                messages.add_message(request, messages.WARNING, message)
                return render_to_response(
                    'air/airdetectordata_import.html',
                    {'form': form},
                    context_instance=RequestContext(request),
                )
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = AirDetectorDataImportForm()

    return render_to_response(
        'air/airdetectordata_import.html',
        {'form': form},
        context_instance=RequestContext(request),
    )

@login_required
def filter_view(request):
    """
    Displays the Air Detector data table for the currently logged in user with
    filter options.

    The data is loaded by the AirDetectorDataListJson view and rendered by the
    Datatables plugin via Javascript.
    """
    form = AirDetectorDataFilterForm(request.user)
    form.fields['start_date'].initial = (datetime.now(tz=request.user.settings.time_zone) - timedelta(days=7)).date().strftime(DATE_FORMAT)
    form.fields['end_date'].initial = datetime.now(tz=request.user.settings.time_zone).date().strftime(DATE_FORMAT)

    data = reverse('airdetectordata_list_json')

    if request.method == 'POST' and request.is_ajax:
        # We need to create a copy of request.POST because it's immutable and
        # we need to convert the content of the Value field to mg/dL if the
        # user's Air Detector data unit setting is set to mmol/L.
        params = request.POST.copy()
        if request.user.settings.airdetectordata_unit.name == 'mmol/L':
            # Only do the conversion if the values are not None or empty.
            if params['start_value']:
                params['start_value'] = to_mg(params['start_value'])
            if params['end_value']:
                params['end_value'] = to_mg(params['end_value'])

        # Create the URL query string and strip the last '&' at the end.
        data = ('%s?%s' % (reverse('airdetectordata_list_json'), ''.join(
            ['%s=%s&' % (k, v) for k, v in params.iteritems()]))).rstrip('&')

        return HttpResponse(json.dumps(data), content_type='application/json')

    return render_to_response('air/airdetectordata_filter.html', {'form': form, 'data': data}, context_instance=RequestContext(request),)

@login_required
def dashboard(request):
    """
    Displays the AirDetectorData table for the currently logged in user. A form
    for quickly adding airdectordata values is also included.

    The data is loaded by the AirDetectorDataListJson view and rendered by the
    Datatables plugin via Javascript.
    """
    form = AirDetectorDataQuickAddForm()
    form.fields['category'].initial = get_initial_category(request.user)

    return render_to_response(
        'core/dashboard.html',
        {'form': form,
         'airdetectordata_unit_name': request.user.settings.airdetectordata_unit.name},
        context_instance=RequestContext(request),
    )


@login_required
def chart_data_json(request):
    data = {}
    params = request.GET

    days = params.get('days', 0)
    name = params.get('name', '')
    if name == 'avg_by_category':
        data['chart_data'] = ChartData.get_avg_by_category(
            user=request.user, days=int(days))
    elif name == 'avg_by_day':
        data['chart_data'] = ChartData.get_avg_by_day(
            user=request.user, days=int(days))
    elif name == 'level_breakdown':
        data['chart_data'] = ChartData.get_level_breakdown(
            user=request.user, days=int(days))
    elif name == 'count_by_category':
        data['chart_data'] = ChartData.get_count_by_category(
            user=request.user, days=int(days))

    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def stats_json(request):
    data = {'stats': UserStats(request.user).user_stats}

    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def quick_add(request):
    if request.method == 'POST' and request.is_ajax:
        # We need to create a copy of request.POST because it's immutable and
        # we need to convert the content of the Value field to mg/dL if the
        # user's airdectordata unit setting is set to mmol/L.
        post_values = request.POST.copy()
        if request.user.settings.airdetectordata_unit.name == 'mmol/L':
            post_values['value'] = to_mg(post_values['value'])

        form = AirDetectorDataCreateForm(post_values)
        if form.is_valid():
            user = request.user

            obj = form.save(commit=False)
            obj.user = user

            obj.record_date = datetime.now(tz=user.settings.time_zone).date()
            obj.record_time = datetime.now(tz=user.settings.time_zone).time()
            obj.save()

            logger.info('Quick Add by %s: %s', request.user, post_values['value'])

            message = {'success': True}

            return HttpResponse(json.dumps(message))
        else:
            message = {
                'success': False,
                'error': 'Invalid value.'
            }

            return HttpResponse(json.dumps(message))

    raise PermissionDenied


class AirDetectorDataChartsView(LoginRequiredMixin, TemplateView):
    template_name = 'air/airdetectordata_charts.html'


class AirDetectorDataEmailReportView(LoginRequiredMixin, FormView):
    """
    Sends out an email containing the airdectordata data report.
    """
    success_url = '.'
    form_class = AirDetectorDataEmailReportForm
    template_name = 'air/airdetectordata_email_report.html'

    def get_initial(self):
        display_name = self.request.user.get_full_name() or self.request.user
        message = 'AirDetectorData data for %s.\n\nDo not reply to this email.\n\n' \
                  'This email was sent by: %s' % (display_name,
                                                  self.request.user.email)

        return {'recipient': self.request.user.email, 'message': message}

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Email Sent!')
        return super(AirDetectorDataEmailReportView, self).form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING,
                             'Email not sent. Please try again.')
        return super(AirDetectorDataEmailReportView, self).form_invalid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            optional_fields = form.cleaned_data['optional_fields']

            if form.cleaned_data['report_format'] == 'pdf':
                report = AirDetectorDataPdfReport(form.cleaned_data['start_date'],
                                          form.cleaned_data['end_date'],
                                          request.user,
                                          'notes' in optional_fields,
                                          'tags' in optional_fields)
            else:
                report = AirDetectorDataCsvReport(form.cleaned_data['start_date'],
                                          form.cleaned_data['end_date'],
                                          request.user,
                                          'notes' in optional_fields,
                                          'tags'in optional_fields)

            logger.info(
                'Sending email report from user: %s, subject: %s, recipient: %s',
                request.user,
                form.cleaned_data['subject'],
                form.cleaned_data['recipient']
            )

            report.email(form.cleaned_data['recipient'],
                         form.cleaned_data['subject'],
                         form.cleaned_data['message'])

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AirDetectorDataCreateView(LoginRequiredMixin, CreateView):
    model = AirDetectorData
    success_url = '/dashboard/'
    template_name = 'air/airdetectordata_create.html'
    form_class = AirDetectorDataCreateForm

    def get_initial(self):
        time_zone = self.request.user.settings.time_zone
        record_date = datetime.now(tz=time_zone).date().strftime(DATE_FORMAT)
        record_time = datetime.now(tz=time_zone).time().strftime(TIME_FORMAT)

        return {
            'category': get_initial_category(self.request.user),
            'record_date': record_date,
            'record_time': record_time,
        }

    def form_valid(self, form):
        # If the 'Save & Add Another' button is clicked, the submit_button_type
        # field will be set to 'submit_and_add' by Javascript. We'll change
        # the success URL to go back to the Add AirDetectorData page and display a
        # successful message in this case.
        if form.cleaned_data['submit_button_type'] == 'submit_and_add':
            self.success_url = '/air/add/'
            value = form.cleaned_data['value']
            messages.add_message(self.request, messages.SUCCESS, "AirDetectorData '%s' successfully added. You may " "add another." % value)

        # Set the value of the 'user' field to the currently logged-in user.
        form.instance.user = self.request.user

        # Set the values of the record date and time to the current date and
        # time factoring in the user's timezone setting if they're not
        # specified.
        if not form.instance.record_date:
            form.instance.record_date = datetime.now(tz=self.request.user.settings.time_zone).date()

        if not form.instance.record_time:
            form.instance.record_time = datetime.now(tz=self.request.user.settings.time_zone).time()

        return super(AirDetectorDataCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        # We need to create a copy of request.POST because it's immutable and
        # we need to convert the content of the Value field to mg/dL if the
        # user's airdectordata unit setting is set to mmol/L.
        request.POST = request.POST.copy()
        if request.user.settings.airdetectordata_unit.name == 'mmol/L':
            request.POST['value'] = to_mg(request.POST['value'])

        logger.info('New airdetectordata added by %s: %s', request.user, request.POST['value'])

        return super(AirDetectorDataCreateView, self).post(request, *args, **kwargs)

class AirDetectorDataUpdateView(LoginRequiredMixin, UpdateView):
    model = AirDetectorData
    context_object_name = 'airdetectordata'
    template_name = 'air/airdetectordata_update.html'
    form_class = AirDetectorDataUpdateForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # If the record's user doesn't match the currently logged-in user,
        # deny viewing/updating of the object by showing the 403.html
        # forbidden page. This can occur when the user changes the id in
        # the URL field to a record that the user doesn't own.
        if self.object.user != request.user:
            raise PermissionDenied
        else:
            return super(AirDetectorDataUpdateView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('dashboard')

    def get_object(self, queryset=None):
        obj = AirDetectorData.objects.get(pk=self.kwargs['pk'])

        # Convert the value based on user's airdetectordata unit setting.
        obj.value = airdetectordata_by_unit_setting(self.request.user, obj.value)

        return obj

    def post(self, request, *args, **kwargs):
        # We need to create a copy of request.POST because it's immutable and
        # we need to convert the content of the Value field to mg/dL if the
        # user's airdetectordata unit setting is set to mmol/L.
        request.POST = request.POST.copy()
        if request.user.settings.airdetectordata_unit.name == 'mmol/L':
            request.POST['value'] = to_mg(request.POST['value'])

        logger.info('AirDetectorDataData updated by %s, airdetectordata id: %s', request.user, kwargs['pk'])

        return super(AirDetectorDataUpdateView, self).post(request, *args, **kwargs)


class AirDetectorDataDeleteView(LoginRequiredMixin, DeleteView):
    model = AirDetectorData
    success_url = '/dashboard/'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # If the record's user doesn't match the currently logged-in user,
        # deny viewing/updating of the object by showing the 403.html
        # forbidden page. This can occur when the user changes the id in
        # the URL field to a record that the user doesn't own.
        if self.object.user != request.user:
            raise PermissionDenied
        else:
            # Convert the value based on user's airdectordata unit setting.
            self.object.value = airdetectordata_by_unit_setting(request.user, self.object.value)
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)


class AirDetectorDataListJson(LoginRequiredMixin, BaseDatatableView):
    model = AirDetectorData

    columns             = ['id','value', 'category', 'record_date', 'record_time','notes', 'tags', 'actions']
    order_columns = ['id','value', 'category', 'record_date', 'record_time', 'notes']
    max_display_length = 500

    def render_column(self, row, column):
        user = self.request.user
        user_settings = user.settings
        low = user_settings.airdetectordata_low
        high = user_settings.airdetectordata_high
        target_min = user_settings.airdetectordata_target_min
        target_max = user_settings.airdetectordata_target_max

        if id == 'value':
            return '%s' % row.id
        elif column == 'value':
            value_by_unit_setting = airdetectordata_by_unit_setting(user, row.value)
            edit_url = reverse('airdetectordata_update', args=(row.id,))
            if row.value < low or row.value > high:
                return self.get_value_cell_style(edit_url, value_by_unit_setting,'red')
            elif row.value >= target_min and row.value <= target_max:
                return self.get_value_cell_style(edit_url, value_by_unit_setting,'green')
            else:
                return self.get_value_cell_style(edit_url, value_by_unit_setting)
        elif column == 'category':
            return '%s' % row.category.name
        elif column == 'record_date':
            return row.record_date.strftime('%m/%d/%Y')
        elif column == 'record_time':
            return row.record_time.strftime('%I:%M %p')
        elif column == 'tags':
            return ', '.join([t.name for t in row.tags.all()])
        elif column == 'actions':
            edit_link = """<a href="%s">
                <img src="/static/images/icons/icon_changelink.gif"></a>""" % \
                reverse('airdetectordata_update', args=(row.id,))
            delete_link = """<a href="%s">
                <img src="/static/images/icons/icon_deletelink.gif"></a>""" % \
                reverse('airdetectordata_delete', args=(row.id,))
            return '<center>%s&nbsp;&nbsp;%s</center>' % (edit_link, delete_link)
        else:
            return super(AirDetectorDataListJson, self).render_column(row, column)

    def get_value_cell_style(self, url, value, color=None):
        style = '''<center><a href="%s">%s</a></center>''' % (url, value)
        if color:
            style = '''<center><a href="%s"><font color="%s">%s</font></a>
                </center>''' % (url, color, value)

        return style

    def get_initial_queryset(self):
        """
        Filter records to show only entries from the currently logged-in user.
        """
        return AirDetectorData.objects.by_user(self.request.user)

    def filter_queryset(self, qs):
        params = self.request.GET

        search = params.get('sSearch')
        if search:
            qs = qs.filter(
                Q(value__startswith=search) |
                Q(category__name__istartswith=search) |
                reduce(operator.and_, (Q(notes__icontains=i) for i in search.split())) |
                reduce(operator.and_, (Q(tags__name__icontains=i) for i in search.split()))
            )

        start_date = params.get('start_date', '')
        if start_date:
            qs = qs.filter(record_date__gte=datetime.strptime(start_date, DATE_FORMAT))
            
        end_date = params.get('end_date', '')
        if end_date:
            qs = qs.filter(record_date__lte=datetime.strptime(end_date, DATE_FORMAT))

        start_value = params.get('start_value', '')
        if start_value:
            qs = qs.filter(value__gte=start_value)
            
        end_value = params.get('end_value', '')
        if end_value:
            qs = qs.filter(value__lte=end_value)

        category = params.get('category', '')
        if category:
            qs = qs.filter(category=category)

        notes = params.get('notes', '')
        if notes:
            qs = qs.filter(reduce(
                operator.and_, (Q(notes__icontains=i) for i in notes.split())))

        tags = params.get('tags', '')
        if tags:
            qs = qs.filter(tags__name=tags)

        return qs