# Copyright (c) 2013 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the 
# MIT License set forth at:
#   https://github.com/riverbed/flyscript-portal/blob/master/LICENSE ("License").  
# This software is distributed "AS IS" as set forth in the License.

import time
import logging
import threading
import datetime
import pandas

import rvbd.profiler
from rvbd.profiler.filters import TimeFilter, TrafficFilter
from rvbd.common.jsondict import JsonDict

from apps.datasource.models import Table
from apps.devices.devicemanager import DeviceManager

logger = logging.getLogger(__name__)
lock = threading.Lock()


def new_device_instance(*args, **kwargs):
    # Used by DeviceManager to create a Profiler instance
    return rvbd.profiler.Profiler(*args, **kwargs)


class DevicesTable:
    @classmethod
    def create(cls, name, device, **kwargs):
        logger.debug('Creating Profiler DevivceTable table %s' % (name))

        t = Table(name=name, module=__name__, device=device,
                  duration=None, **kwargs)
        t.save()
        return t
        

class TableQuery:
    # Used by Table to actually run a query
    def __init__(self, table, job):
        self.table = table
        self.job = job

    def fake_run(self):
        import fake_data
        self.data = fake_data.make_data(self.table)
        
    def run(self):
        """ Main execution method
        """

        profiler = DeviceManager.get_device(self.table.device.id)
        report = rvbd.profiler.report.SingleQueryReport(profiler)

        columns = [col.name for col in self.table.get_columns(synthetic=False)]

        # This returns an array of rows, one row per device
        # Each row is a dict containing elements such as id, ipaddr, name, type, type_id, and version
        devicedata = profiler.api.devices.get_all()

        # Convert to a DataFrame to make it easier to work with
        df = pandas.DataFrame(devicedata)

        for col in columns:
            if col not in df:
                raise KeyError("Devices table has no column '%s'" % col.name)

        df = df.ix[:,columns]

        if self.table.sortcol is not None:
            df = df.sort(self.table.sortcol.name)
            
        if self.table.rows > 0:
            df = df[:self.table.rows]

        self.data = df
        
        logger.info("DeviceTable job %s returning %d devices" % (self.job, len(self.data)))
        return True
