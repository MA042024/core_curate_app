""" Apps file for setting core package when app is ready
"""
from django.apps import AppConfig
import core_curate_app.permissions.discover as discover


class CurateAppConfig(AppConfig):
    """ Core application settings
    """
    name = 'core_curate_app'

    def ready(self):
        """ Run when the app is ready

        Returns:

        """
        discover.init_rules()
