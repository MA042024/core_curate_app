""" Apps file for setting core package when app is ready
"""
import sys

from django.apps import AppConfig


class CurateAppConfig(AppConfig):
    """Core application settings."""

    name = "core_curate_app"
    verbose_name = "Core Curate App"

    def ready(self):
        """Run when the app is ready.

        Returns:

        """
        if "migrate" not in sys.argv:
            from core_curate_app.permissions import discover

            discover.init_permissions()
