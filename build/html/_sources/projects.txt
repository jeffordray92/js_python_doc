Projects package
================

.. toctree::
   :maxdepth: 2

projects.forms module
---------------------

The **projects.forms.py** file handles user input in relation to **Project** app processes.

.. automodule:: projects.forms

.. autoclass:: ProjectAddForm
    :members: init_project, 
              init_pm_tool, 
              create_project,
              skip_setup,

.. autoclass:: ProjectEditForm

projects.models module
----------------------

The **projects.models.py** file is responsible for storing and creating **Project**-related object instances.

.. automodule:: projects.models
   :members:

projects.utils module
---------------------

The :py:mod:`utils` module contains all the necessary functions to setup the project and its necessary tools.

submodules
----------

.. toctree::
   :maxdepth: 2

   projects.exceptions
   projects.templatetags
   projects.validators

.. automodule:: projects.utils
   :members:
  