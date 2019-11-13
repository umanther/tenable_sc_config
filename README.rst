=================
tenable_sc_config
=================
|license-img|

Purpose
=======
A tool to create & load a config .ini file for connecting to a Tenable.SC instance

Usage
=====
- Running the config.py file as a the main file will create a blank ini file (with notes)
- Importing the package will attempt to load the default filename

  - If the default file is found: loads the file and returns an object containing the results
  - If the default file is not found: returns None as the object

Source
------
Github_

.. |license-img| image:: https://img.shields.io/github/license/umanther/tenable_sc_config?style=plastic
.. _Github: https://github.com/umanther/tenable_sc_config