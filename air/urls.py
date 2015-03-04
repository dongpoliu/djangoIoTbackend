# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url

from .views import (
    import_data,
    filter_view,
    quick_add,
    stats_json,
    chart_data_json,
    AirDetectorDataChartsView,
    AirDetectorDataCreateView,
    AirDetectorDataUpdateView,
    AirDetectorDataDeleteView,
    AirDetectorDataEmailReportView,
    AirDetectorDataListJson,
)


urlpatterns = patterns('',
    url(regex=r'^import/', view=import_data, name='airdetectordata_import', ),
    url(regex=r'^filter/', view=filter_view, name='airdetectordata_filter', ),
    url(regex=r'^quick_add/', view=quick_add, name='airdetectordata_quick_add', ),
    url(regex=r'^add/', view=AirDetectorDataCreateView.as_view(),name='airdetectordata_create',),
    url(regex=r'^list_json/$', view=AirDetectorDataListJson.as_view(), name='airdetectordata_list_json',),
    url(regex=r'^chart_data_json/$', view=chart_data_json, name='chart_data_json',),
    url(regex=r'^stats_json/$', view=stats_json, name='stats_json', ),
    url(regex=r'^charts/$', view=AirDetectorDataChartsView.as_view(), name='airdetectordata_charts',),
    url(regex=r'^email_report/', view=AirDetectorDataEmailReportView.as_view(), name='airdetectordata_email_report', ),
    url(regex=r'^(?P<pk>\d+)/edit/', view=AirDetectorDataUpdateView.as_view(), name='airdetectordata_update',),
    url(regex=r'^(?P<pk>\d+)/delete/', view=AirDetectorDataDeleteView.as_view(), name='airdetectordata_delete', ),
)
