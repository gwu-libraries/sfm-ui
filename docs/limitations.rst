==============================
 Limitations and Known Issues
==============================

To make sure you have the best possible experience with SFM, you should be aware of the limitations and known issues:

* Twitter REST harvesters can become congested when there are too many long-running harvests using too few unique credentials (`Ticket 472 <https://github.com/gwu-libraries/sfm-ui/issues/472>`_)
* Better monitoring and logging for harvesting and exporting is needed (`Ticket #303 <https://github.com/gwu-libraries/sfm-ui/issues/303>`_ and `Ticket #229 <https://github.com/gwu-libraries/sfm-ui/issues/229>`_)
* Collections are not portable between SFM instances (`Ticket #326 <https://github.com/gwu-libraries/sfm-ui/issues/326>`_)
* SFM is not secure.  It does not currently run with HTTPS and enforcement of authorizations is not consistent in the UI (`Ticket #362 <https://github.com/gwu-libraries/sfm-ui/issues/362>`_).
* Web harvester (Heritrix) does not handle deduping (`Ticket #438 <https://github.com/gwu-libraries/sfm-ui/issues/438>`_)
* Huge exports are not segmented into multiple files (`Ticket #454 <https://github.com/gwu-libraries/sfm-ui/issues/454>`_)
* Because of the need to link a Heritrix container and a web harvester container, the web harvester cannot be scaled with ``docker-compose scale command`` (`Ticket 408 <https://github.com/gwu-libraries/sfm-ui/issues/408>`_)
* Changes to the hostname of server (e.g., from the reboot of an AWS EC2 instance) are not handled (`Ticket 435 <https://github.com/gwu-libraries/sfm-ui/issues/435>`_)

We are planning to address these in future releases. In the meantime, there are work-arounds for many of these issues. For a complete list of tickets, see https://github.com/gwu-libraries/sfm-ui/issues

In addition, you should be aware of the following:

* Access to the Weibo API is limited, so make sure you understand what can be collected.
* SFM does not currently provide a web interface for “replaying” the collected social media or web content.
* ELK is only experimental.  Scaling and administration of ELK have not been considered.
