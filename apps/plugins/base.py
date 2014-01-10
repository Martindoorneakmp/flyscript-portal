# Copyright (c) 2013 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the
# MIT License set forth at:
#   https://github.com/riverbed/flyscript-portal/blob/master/LICENSE ("License").
# This software is distributed "AS IS" as set forth in the License.

from project.utils import Importer

# portions and concepts used from sentry project:
# https://getsentry.com/welcome/


class PluginMount(type):
    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        if IPlugin in bases:
            return new_cls
        if not new_cls.title:
            new_cls.title = new_cls.__name__
        if not new_cls.slug:
            new_cls.slug = new_cls.title.replace(' ', '-').lower()
        return new_cls


class IPlugin(object):
    """ Plugin base class. Should not be inherited from directly.
    """
    # Generic plugin metadata
    title = None
    slug = None
    description = None
    version = None
    author = None
    plugin_url = None

    # list of dependencies for this plugin
    dependencies = []

    # Global enabled state
    enabled = True
    can_disable = True

    # Plugin components
    reports = []        # list of report modules
    libraries = []      # list of library directories
                        # XXX do we need this?

    _reports_loaded = False

    def is_enabled(self):
        """ Returns boolean if this plugin is enabled. """
        return self.enabled or not self.can_disable

    def load_reports(self):
        if self.reports is not None and self.is_enabled():
            module_path = self.__module__.rsplit('.', 1)[0]

            importer = Importer()

            for report in self.reports:
                path, module = report.split('.', 1)
                name = '.'.join([module_path, path, module])

                importer.import_file(module, name)
            self._reports_loaded = True


class Plugin(IPlugin):
    """ Portal plugin class for subclassing. """
    __metaclass__ = PluginMount
