# Copyright (c) 2013 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the 
# MIT License set forth at:
#   https://github.com/riverbed/flyscript-portal/blob/master/LICENSE ("License").  
# This software is distributed "AS IS" as set forth in the License.


from apps.datasource.models import Device

from django.contrib import admin

'''
class ReportAdmin(admin.ModelAdmin):
    fields = [ 'title' ]
    
admin.site.register(Report, ReportAdmin)

class DeviceAdmin(admin.ModelAdmin):
    fields = [ 'name', 'host', 'port', 'username' ]
    
admin.site.register(Device, DeviceAdmin)

'''