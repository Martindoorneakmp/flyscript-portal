# Copyright (c) 2013 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the 
# MIT License set forth at:
#   https://github.com/riverbed/flyscript-portal/blob/master/LICENSE ("License").  
# This software is distributed "AS IS" as set forth in the License.


from django.conf.urls import patterns, include, url
import apps.preferences.views as views

urlpatterns = patterns(
    'apps.report.views',
    url(r'^$', views.PreferencesView.as_view(), name='preferences'),
)
