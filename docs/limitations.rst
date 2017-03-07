==============================
 Limitations and Known Issues
==============================

To make sure you have the best possible experience with SFM, you should be aware of the limitations and known issues:

* SFM is does not currently run with HTTPS (`Ticket #361 <https://github.com/gwu-libraries/sfm-ui/issues/361>`_).
* Because of the need to link a Heritrix container and a web harvester container, the web harvester cannot be scaled with ``docker-compose scale command`` (`Ticket 408 <https://github.com/gwu-libraries/sfm-ui/issues/408>`_)
* Changes to the hostname of server (e.g., from the reboot of an AWS EC2 instance) are not handled (`Ticket 435 <https://github.com/gwu-libraries/sfm-ui/issues/435>`_)

We are planning to address these in future releases. In the meantime, there are work-arounds for many of these issues. For a complete list of tickets, see https://github.com/gwu-libraries/sfm-ui/issues

In addition, you should be aware of the following:

* The current implementation of web harvesting is not optimal and requires significant additional work or reconsideration.
  In particular: (1) It does not scale: under normal collecting scenarios, web harvesting can lag far behind social
  media collecting. (2) It is not reliable: Heritrix requires more fiddling and testing.
* Access to the Weibo API is limited, so make sure you understand what can be collected.
* SFM does not currently provide a web interface for “replaying” the collected social media or web content.
* ELK is only experimental.  Scaling and administration of ELK have not been considered.
