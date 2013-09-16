# Copyright (c) 2013 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the 
# MIT License set forth at:
#   https://github.com/riverbed/flyscript-portal/blob/master/LICENSE ("License").  
# This software is distributed "AS IS" as set forth in the License.

"""
This module renders raw data from a data source to be displayed
on a Google Map.
"""

from .maps_base import BaseMapWidget, subnet


def authorized(userprofile):
    """ Verifies the Google Maps API can be used given the version selected
        and the API key supplied.

        Returns True/False, and an error message if applicable
    """
    maps_version = userprofile.maps_version
    api_key = userprofile.maps_api_key

    if maps_version == 'DISABLED':
        msg = (u'Google Maps API has been disabled.\n'
               'See Configure->Preferences to update.')
        return False, msg
    elif maps_version in ('FREE', 'BUSINESS') and not api_key:
        msg = (u'A valid API_KEY must be provided for either \n'
               '"Free" or "Business" Google Maps API choices.\n'
               'See Configure->Preferences to update.')
        return False, msg
    else:
        return True, ''


class MapWidget(BaseMapWidget):
    @classmethod
    def create(cls, report, table, title, width=6, height=300, column=None):
        """Class method to create a MapWidget.

        `column` is the data column to graph
        """
        super(MapWidget, cls).create(report, table, title, width, height, column,
                                     module=__name__, uiwidget=cls.__name__)

    @classmethod
    def process(cls, widget, data):
        """Class method to generate JSON for the JavaScript-side of the MapWidget
        from the incoming data.
        """
        data = super(MapWidget, cls).process(widget, data)

        circles = []
        for c in data['circles']:
            circle = {
                'strokeColor': '#FF0000',
                'strokeOpacity': 0.8,
                'strokeWeight': 2,
                'fillColor': '#FF0000',
                'fillOpacity': 0.35,
                'center': [c.lat, c.long],
                'size': 15 * (c.value / c.value_max),
                'title': c.title,
                'value': c.value,
                'units': c.units,
                'formatter': c.formatter
            }
            circles.append(circle)
        data['circles'] = circles

        return data
