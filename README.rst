=====
HSYOJ
=====
Online Judge for NO.1 Middle School Affiliated to CCNU

:Website: https://gitlab.com/hsyoj/hsyoj

Status
======
HSYOJ is still heavily under development,
it may take a long time to be completed.

Requirements
============
Recommend (No test for older version, but may run as well):

* Python >= 3.6
* Django >= 2.0
* Sphinx >= 1.7

Getting Start
=============
0. Install Git_ and Python_,
   see the websites for more information.

   .. _Git: git-scm.com
   .. _Python: www.python.org
#. Clone this repository

   `$ git clone "https://gitlab.com/hsyoj/hsyoj.git"`
#. Enter the repository directory

   `$ cd hsyoj`
#. Create python virtual environment

   `$ python -m venv .venv`

   `$ source .venv/bin/activate`
#. Install requirements

   `$ pip install -r requirements.txt`
#. Initialize the database

   `$ python manage.py migrate`

   To import the sample problems:

   `$ python manage.py loaddata problems`
#. Run the server

   `$ python manage.py runserver`

Contributing
============
Please see file "CONTRIBUTING".

Licence
=======
The HSYOJ is licenced under the AGPL licence,
see the file "LICENCE_" for more information.

.. _LICENCE: LICENSE
