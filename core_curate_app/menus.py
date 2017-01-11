""" Add Curate in main menu
"""

from django.core.urlresolvers import reverse
from menu import Menu, MenuItem

# FIXME: CHECK AUTHENTICATION !
Menu.add_item(
    "main", MenuItem("Curator", reverse("core_curate_index"))
)
