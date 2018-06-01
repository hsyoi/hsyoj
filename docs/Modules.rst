=======
Modules
=======
HSYOJ is consisted of these modules:

* hsyoj-server
* hsyoj-client
* hsyoj-judge
* hsyoj-common
* hsyoj-web

+--------+-----+
| Client | Web |
+--------+-----+
|    Server    |
+--------------+
|     Judge    |
+--------------+


hsyoj-server
------------
hsyoj-server is a message queue.

It listen two ports(default 6140 and 6141).

One port(6140) for communicate with judge machines,
and the other port(6141) is used to communicate with clients.

The two ports is managed by ZeroMQ,
and use ROUTER mode to implement load balancing.

hsyoj-server also manage the database.

hsyoj-judge
-----------
hsyoj-judge is used to judge the code submitted by users.

It connect to hsyoj-server and wait for tasks to be provided.

hsyoj-client
------------
hsyoj-client is a client for HSYOJ.

It can judge code at locale so
network connection is not neccessary.

All functions:

For students:

* Explore the problems
* View your own information
* Submit code
* Judge code at locale

For teachers:

* View any students' information
* Add a contest
* Add homework
* Manage problems
* Create and manage teams

hsyoj-web
---------
hsyoj-web is a module provide functions similar to hsyoj-client
but run inside a web browser so it can work at any computer with a web browser.

hsyoj-common
------------
hsyoj-common provide a few functions needed by multi-modules.

All functions include:

* An interface to compile any supported program language to an executable file
* Judge code and return the results
* Define all error status

common.judge
~~~~~~~~~~~~

  .. automodule:: common.judge
     :members:

common.compiler
~~~~~~~~~~~~~~~

  .. automodule:: common.compiler
     :members:
