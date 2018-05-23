===============
Data Structures
===============
The data stored in database is also json.

All types of data structures are:

* record:

  .. code:: json

    {
      'user': str
      'submit_time': float
      'code': str
      'result': list[result]
    }

* user:

  .. code:: json

    {
      'username': str
      'password': str
      'register_time': float
      'records': list[record]
    }

* problem

  .. code:: json

    {
      'problem_id': int
      'time_limit': float
      'memory_limit': float
      'optimize': bool
    }
