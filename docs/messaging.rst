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
    channel.exchange_declare(exchange="sfm_exchange",
                             type="topic", durable=True)

Queues
------

All queues must be declared durable.::

    #Declare harvester queue
    channel.queue_declare(queue="harvester",
                          durable=True)

Example
-------

Creating a connection and channel, then declaring an exchange and queue and binding
the exchange to the queue.::

    #Create a connection
    credentials = pika.PlainCredentials(username, password)
    parameters = pika.ConnectionParameters(host=host, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    #Create a channel
    channel = connection.channel()
    #Declare sfm_exchange
    channel.exchange_declare(exchange="sfm_exchange",
                             type="topic", durable=True)
    #Declare harvester queue
    channel.queue_declare(queue="sfm_exchange",
                          durable=True)
    #Bind
    channel.queue_bind(exchange="sfm_exchange",
                       queue="sfm_exchange", routing_key="sfm_exchange")

    channel.close()
