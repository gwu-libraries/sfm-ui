============
 Monitoring
============

There are several mechanisms for monitoring (and troubleshooting) SFM.

For more information on troubleshooting, see :doc:`troubleshooting`.

--------------
 Monitor page
--------------

To reach the monitoring page, click "Monitor" on the header of any page in SFM UI.

The monitor page provides status and queue lengths for SFM components, including
harvesters and exporters.

The status is based on the most recent status reported back by each harvester
or exporter (within the last 3 days). A harvester or exporter reports its status
when it begins a harvest or export. It also reports its status when it completes
the harvest or exporter. Harvesters will also provide status updates periodically
during a harvest.

Note that if there are multiple instances of a harvester or exporter (created with
`docker-compose scale`), each instance will be listed.

The queue length lists the number of harvest or export requests that are waiting.
A long queue length can indicate that additional harvesters or exporters are needed
to handle the load (see :ref:`docker-scaling`) or that there is a problem with the
harvester or exporter.

The queue length for SFM UI is also listed. This is a queue of status update messages
from harvesters or exporters. SFM UI uses these messages to update the
records for harvests and exports. Any sort of a queue here indicates a problem.

------
 Logs
------

It can be helpful to peek at the logs to get more detail on the work being performed
by a harvester or exporter.

Docker logs
===========
The logs for harvesters and exporters can be accessed using Docker's `log` commands.

First, determine the name of the harvester or exporter using ``docker ps``. In general,
the name will be something like `sfm_twitterrestharvester_1`.

Second, get the log with ``docker logs <name>``.

Add `-f` to follow the log. For example,
``docker logs -f sfm_twitterrestharvester_1``.

Add `--tail=<number of lines` to get the tail of the log. For example,
``docker logs --tail=100 sfm_twitterrestharvester_1``.

Side note: To follow the logs of all services, use ``docker-compose logs -f``.

Twitter Stream Harvester logs
=============================
Since the Twitter Stream Harvester runs multiple harvests on the same host, accessing its
logs are a bit different.

First, determine the name of the Twitter Stream Harvester and the container id using
``docker ps``.  The name will probably be `sfm_twitterstreamharvester_1` and the container
id will be something like `bffcae5d0603`.

Second, determine the harvest id. This is available from the harvest's detail page.

Third, get the stdout log with ``docker exec -t <name> cat /sfm-data/containers/<container id>/log/<harvest id>.out.log``.
To get the stderr log, substitute `.err` for `.out`.

To follow the log, use `tail -f` instead of `cat`. For example,
``docker exec -t sfm_twitterstreamharvester_1 tail -f /sfm-data/containers/bffcae5d0603/log/d4493eed5f4f49c6a1981c89cb5d525f.err.log``.

-----------------------------
 RabbitMQ management console
-----------------------------

The RabbitMQ Admin is usually available on port 15672. For example, `http://localhost:15672/ <http://localhost:15672/>`_.
