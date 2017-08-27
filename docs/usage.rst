=====
Usage
=====

To use django-djue in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'djue.apps.DjueConfig',
        ...
    )

Add django-djue's URL patterns:

.. code-block:: python

    from djue import urls as djue_urls


    urlpatterns = [
        ...
        url(r'^', include(djue_urls)),
        ...
    ]
