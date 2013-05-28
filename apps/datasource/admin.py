# Copyright (c) 2013 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the 
# MIT License set forth at:
#   https://github.com/riverbed/flyscript-portal/blob/master/LICENSE ("License").  
# This software is distributed "AS IS" as set forth in the License.


from apps.datasource.models import Device, Table, Column, Job

from django.contrib import admin


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'module', 'host', 'port')

admin.site.register(Device, DeviceAdmin)


class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'module', 'device')
    list_filter = ('module', )

admin.site.register(Table, TableAdmin)


class ColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'table', 'iskey')
    list_filter = ('table', )

admin.site.register(Column, ColumnAdmin)


class JobAdmin(admin.ModelAdmin):
    list_display = ('table', 'status', 'progress', 'message')

admin.site.register(Job, JobAdmin)
