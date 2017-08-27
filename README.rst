=============================
django-djue
=============================

.. image:: https://badge.fury.io/py/djue.svg
    :target: https://badge.fury.io/py/djue

.. image:: https://travis-ci.org/brmc/djue.svg?branch=master
    :target: https://travis-ci.org/brmc/djue

.. image:: https://codecov.io/gh/brmc/djue/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/brmc/djue

Generate vue.js components, stores, and routes from your django forms, models, and urls

Documentation
-------------

The full documentation is at https://djue.readthedocs.io.

Quickstart
----------

Install django-djue::

    pip install djue

Add it to your `INSTALLED_APPS`:

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

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
