Messaging
=========

.. _messaging-rabbitmq:

RabbitMQ
--------

RabbitMQ is used as a message broker.

The RabbitMQ managagement console is exposed at ``http://<your docker host>:15672/``.
The username is ``sfm_user``. The password is the value of ``RABBITMQ_DEFAULT_PASS``
in ``secrets.env``.

Publishers/consumers
--------------------

* The hostname for RabbitMQ is ``mq`` and the port is 5672.
* It cannot be guaranteed that the RabbitMQ docker container will be up and ready when
  any other container is started. Before starting, wait for a connection to be available
  on port 5672 on ``rabbit``. See `appdeps.py <https://github.com/gwu-libraries/appdeps>`_
  for docker application dependency support.
* Publishers/consumers may not assume that the requisite exchanges/queues/bindings
  have previously been created. They must declare them as specified below.

Exchange
--------

``sfm_exchange`` is a durable topic exchange to be used for all messages. All
publishers/consumers must declare it.::

    #Declare sfm_exchange
    from kombu import Connection

    exchange = Exchange(name="sfm_exchange,
                        type="topic", durable=True)
    exchange(channel).declare()

Queues
------

All queues must be declared durable.::

    #Declare harvester queue
    from kombu import Queue
    queue = Queue(name="harvester",
                  exchange=exchange,
                  channel=channel,
                  durable=True)
    queue.declare()
    queue.bind_to(exchange=exchange,
                  routing_key="harvest.status.*.*")
