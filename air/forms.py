# -*- coding: UTF-8 -*-
import itertools
from datetime import date, timedelta
from django import forms
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Button, Submit, MultiField, Div, HTML, Field, Fieldset, Reset
from crispy_forms.bootstrap import FormActions
from .models import AirDetectorData, Category
from .fields import RestrictedFileField
from django.utils.translation import ugettext_lazy as _

DATE_FORMAT = '%m/%d/%Y'
TIME_FORMAT = '%I:%M %p'

class AirDetectorDataFilterForm(forms.Form):
    quick_date_select = forms.ChoiceField(
        label='快速选择日期',
        choices=(
            (7, '最近7 天'),
            (30, '最近 30 天'),
            (60, '最近 60 天'),
            (90, '最近 90 天'),
        ),
        required=False,
    )
    start_date = forms.DateField(
        label='日期范围', required=False, input_formats=[DATE_FORMAT])
    end_date = forms.DateField(
        label='', required=False, input_formats=[DATE_FORMAT])

    start_value = forms.IntegerField(
        label='数值范围', required=False, min_value=0)
    end_value = forms.IntegerField(label='', required=False, min_value=0)

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=False)

    notes = forms.CharField(label='备注包括', required=False,
                            widget=forms.Textarea(attrs={'rows': 2}))

    def __init__(self, user, *args, **kwargs):
        super(AirDetectorDataFilterForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'filter_form'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'

        self.fields['tags'] = forms.ChoiceField(
            choices=self.get_tags(AirDetectorData.objects.filter(user=user).exclude(
                tags__name__isnull=True)),
            required=False)

        self. helper.layout = Layout(
            'quick_date_select',
            Field('start_date', placeholder='From (mm/dd/yyyy)'),
            Field('end_date', placeholder='To (mm/dd/yyyy)'),
            'category',
            Field('start_value', placeholder='From', step='any'),
            Field('end_value', placeholder='To', step='any'),
            'notes',
            Field('tags'),
            FormActions(
                Submit('submit', _(u"筛选")),
                Reset('reset', _(u"重设")),
            ),
        )

    def get_tags(self, queryset):
        """
        Iterate through the queryset and get the unique tag names.
        """
        tag_list = list(itertools.chain.from_iterable(
            [i.tags.names() for i in queryset]))

        empty_label = [('', '---------')]
        # The tag_list here is converted to a set to create a unique
        # collection.
        choices = empty_label + [
            (tag, tag) for tag in sorted(list(set(tag_list)))]

        return choices


class AirDetectorDataQuickAddForm(forms.ModelForm):
    """
    A simple form for adding AirDetectorData values. Date and time are automatically
    set to the user's current local date and time using Javascript (see
    dashboard.html template).
    """
    def __init__(self, *args, **kwargs):
        super(AirDetectorDataQuickAddForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'quick_add_form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-inline'
        self.helper.form_show_labels = False

        # Remove the blank option from the select widget.
        self.fields['category'].empty_label = None

        self.helper.layout = Layout(
            HTML('''
            <div id="div_id_value" class="form-group"> <div class="controls">
            <input autofocus="True" class="numberinput form-control"
            id="id_value" name="value"
            placeholder="Value ({{ user.settings.glucose_unit.name }})"
            required="True" type="number" step="any" min="0"/></div></div>
            '''),
            Field('category'),
            Field('record_date', type='hidden'),
            Field('record_time', type='hidden'),
            Submit('submit', _(u"快速添加")),
        )

    class Meta:
        model = AirDetectorData
        exclude = ('user', 'notes')


class AirDetectorDataEmailReportForm(forms.Form):
    report_format = forms.ChoiceField(
        label='Format',
        choices=(
            ('csv', 'CSV'),
            ('pdf', 'PDF'),
        )
    )

    optional_fields = forms.MultipleChoiceField(
        choices=(
            ('notes', 'Notes'),
            ('tags', 'Tags'),
        ),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    start_date = forms.DateField(label='From')
    end_date = forms.DateField(label='To')
    subject = forms.CharField(required=False)
    recipient = forms.EmailField(label='Send To')
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 50}), required=False)

    def __init__(self, *args, **kwargs):
        super(AirDetectorDataEmailReportForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3 col-md-3'
        self.helper.field_class = 'col-sm-9 col-md-9'

        valid_date_formats = ['%m/%d/%Y']
        self.fields['start_date'].input_formats = valid_date_formats
        self.fields['end_date'].input_formats = valid_date_formats
        

        self. helper.layout = Layout(
            MultiField(
                None,
                Div(
                    HTML('''
                    {% if messages %}
                    {% for message in messages %}
                    <p {% if message.tags %}
                    class="alert alert-{{ message.tags }}"
                    {% endif %}>{{ message }}</p>{% endfor %}{% endif %}
                    '''),
                    Div(
                        'report_format',
                        Field('start_date', required=True),
                        Field('end_date', required=True),
                        'optional_fields',
                        css_class='well col-sm-4 col-md-4',
                    ),
                    Div('subject',
                        Field('recipient', placeholder='Email address',
                              required=True),
                        'message',
                        FormActions(
                            Submit('submit',  _(u"发送")),
                            css_class='pull-right'
                        ),
                        css_class='col-sm-8 col-md-8',
                    ),
                    css_class='row'
                ),
            ),
        )

        # Initial values.
        now = date.today()
        last_90_days = now - timedelta(days=90)
        self.fields['start_date'].initial = last_90_days.strftime(DATE_FORMAT)
        self.fields['end_date'].initial = now.strftime(DATE_FORMAT)

        self.fields['report_format'].initial = 'pdf'
        self.fields['optional_fields'].initial = ['notes']
        self.fields['subject'].initial = '[AirDetectorDataTracker] AirDetectorData Report'


class AirDetectorDataInputForm(forms.ModelForm):
    # This is a hidden field that holds the submit type value. Used to
    # determine whether the user clicked 'Save' or 'Save & Add Another' in
    # the AirDetectorData Create Form.
    submit_button_type = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(AirDetectorDataInputForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal col-xs-12 col-md-6 col-lg-5'
        self.helper.label_class = 'col-xs-3 col-md-2 col-lg-2'
        self.helper.field_class = 'col-xs-9 col-md-10 col-lg-10'
        self.helper.add_input(Submit('submit', '保存'))
        self.helper.add_input(Button('cancel', 'Cancel', onclick='location.href="%s";' % reverse('dashboard')))

        # Remove the blank option from the select widget.
        self.fields['category'].empty_label = None
        self.fields['category'].required = False

        # Specify which time formats are valid for this field. This setting is
        # necessary when using the bootstrap-datetimepicker widget as it
        # doesn't allow inputting of seconds.
        valid_time_formats = ['%H:%M', '%I:%M%p', '%I:%M %p']
        self.fields['record_time'].input_formats = valid_time_formats
        valid_date_formats = ['%m/%d/%Y']
        self.fields['record_date'].input_formats = valid_date_formats

        self. helper.layout = Layout(
            HTML(
                '''
                {% if messages %}
                {% for message in messages %}
                <p {% if message.tags %}
                class="alert alert-{{ message.tags }}"
                {% endif %}>{{ message }}</p>{% endfor %}{% endif %}
                '''
            ),
            Field('value', placeholder='Value', required=True, autofocus=True, min=0, step='any'),
            'category',
            'record_date',
            'record_time',
            'notes',
            Field('tags', placeholder='e.g. fasting, sick, "after meal"'),
            Field('submit_button_type', type='hidden')
        )

    class Meta:
        model = AirDetectorData
        exclude = ('user',)
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }


class AirDetectorDataCreateForm(AirDetectorDataInputForm):

    def __init__(self, *args, **kwargs):
        super(AirDetectorDataCreateForm, self).__init__(*args, **kwargs)

        # Make record date and time not required. If these fields are empty
        # the current date and time will be used.
        self.fields['record_date'].widget.format = DATE_FORMAT
        self.fields['record_time'].widget.format = TIME_FORMAT        
        self.fields['record_date'].required = False
        self.fields['record_time'].required = False

        self.helper.add_input(Submit('submit_and_add', '保存并添加下一个', css_class='pull-right'))


class AirDetectorDataUpdateForm(AirDetectorDataInputForm):

    def __init__(self, *args, **kwargs):
        super(AirDetectorDataUpdateForm, self).__init__(*args, **kwargs)

        # Set date and time formats to those supported by the
        # bootstrap-datetimepicker widget.
        self.fields['record_date'].widget.format = DATE_FORMAT
        self.fields['record_time'].widget.format = TIME_FORMAT

        delete_url = reverse('airdetectordata_delete', args=(self.instance.id,))
        self.helper.add_input(Button('delete', 'Delete',
                                     onclick='location.href="%s";' % delete_url,
                                     css_class='btn-danger pull-right'))


class AirDetectorDataImportForm(forms.Form):
    # File size limited to 2MB
    file = RestrictedFileField(
        label='CSV File (Max Size 2MB)',
        content_types=[
            'text/csv',
            'application/csv',
            'application/octet-stream',
            'text/plain',
        ],
        max_upload_size=2097152,
    )

    def __init__(self, *args, **kwargs):
        super(AirDetectorDataImportForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self. helper.layout = Layout(
            MultiField(
                None,
                HTML(
                    '''
                    {% if messages %}
                    {% for message in messages %}
                    <p {% if message.tags %}
                    class="alert alert-{{ message.tags }}"
                    {% endif %}>{{ message }}</p>{% endfor %}{% endif %}
                    '''
                ),
                Div(
                    'file',
                    FormActions(
                        Submit('submit', 'Import'),
                        css_class='pull-right',
                    ),
                    css_class='well col-xs-10 col-sm-8 col-md-8',
                ),
            ),
        )
