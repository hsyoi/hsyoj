===============================
Message Transfer Protocol (MTP)
===============================
HSYOJ uses ZeroMQ to transfer data.
And all data is saved in json.

So the frames is like this: ::

  +-----------+
  | Socket ID |
  +-----------+
  |    b''    |
  +-----------+
  |   JSON    |
  +-----------+

The json inside is structured as this:

.. code:: json

  {
    'header': {
      'type': str,
      'socket_id': str,
    },
    'metadata': {
    },
    'content': {
    }
  }

The type is one of the following types:

* LOGIN:

  .. code:: json

    {
      'header': {
        'type': str,
        'socket_id': str,
      },
      'metadata': {
      },
      'content': {
        'username': str,
        'password': str,
      }
    }

* JUDGE:

  .. code:: json

    {
      'header': {
        'type': str,
        'socket_id': str,
      },
      'metadata': {
        'judge_id': str,  # Generate by server
        'problem_id': str,
      },
      'content': {
        'language': str,
        'source_code': str,
        'stdio': bool,
        // Following content is not needed for client
        // Server will fill it by problem_id
        'i_name': str,
        'o_name': str,
        't_limit': float,
        'm_limit': float,
        'O2': bool,
        'test_cases': List[List[str, str]],
      }
    }

* RESULT:

  .. code:: json

    {
      'header': {
        'type': str,
        'socket_id': str,
      },
      'metadata': {
        'judge_id': str,
      },
      'content': {
        'socores': float,
        'result': List[int],
      }
    }

* GET:

  .. code:: json

    {
      'header': {
        'type': str,
        'socket_id': str,
      },
      'metadata': {
        // One of ['user', 'problem', 'record']
        'name': str,
      },
      'content': {
      }
    }

* DATA:

  .. code:: json

    {
      'header': {
        'type': str,
        'socket_id': str,
      },
      'metadata': {
        'name': str,
      },
      'content': {
        'problems': List[Problem],
        'userinfo': User,
        'records': List[Record],
      }
    }
