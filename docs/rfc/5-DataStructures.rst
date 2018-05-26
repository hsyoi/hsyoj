===============
Data Structures
===============
Data structures stored in database
are definded in models.py files.

See Problem, User, Record
for more information.

.. py:class:: Problem

   .. py:attribute:: id
   .. py:attribute:: title
   .. py:attribute:: time_limit
   .. py:attribute:: memory_limit

   .. py:attribute:: submissions
   .. py:attribute:: accpected

   .. py:method:: __str__(self) -> str

      .. code:: python

         "%s: %s" % (self.id, self.title)
.. py:class:: User

   .. py:attribute:: username
   .. py:attribute:: password
   .. py:attribute:: phone_number
   .. py:attribute:: email
   .. py:attribute:: register_time

   .. py:method:: __str__(self) -> str

      .. code:: python

         "%s: %s" % (self.id, self.username)
.. py:class:: Record

   .. py:attribute:: user
   .. py:attribute:: problem
   .. py:attribute:: code
   .. py:attribute:: submit_time
   .. py:attribute:: running_time
