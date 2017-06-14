# core_curate_app

core_curate_app is a Django app.

# Quick start

1. Add "core_curate_app" to your INSTALLED_APPS setting like this:

  ```python
  INSTALLED_APPS = [
      ...
      'core_curate_app',
  ]
  ```

  2. Include the core_dashboard_app URLconf in your project urls.py like this::

  ```python
  url(r'^curate/', include('core_curate_app.urls')),
  ```

