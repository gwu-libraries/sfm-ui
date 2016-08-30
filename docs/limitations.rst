==============================
 Limitations and Known Issues
==============================

To make sure you have the best possible experience with SFM, you should be aware of the limitations and known issues:

* Better monitoring and logging for harvesting and exporting is needed (`Ticket #303 <https://github.com/gwu-libraries/sfm-ui/issues/303>`_ and `Ticket #229 <https://github.com/gwu-libraries/sfm-ui/issues/229>`_)
* Long-running Twitter searchs may block other harvest requests (`Ticket #320 <https://github.com/gwu-libraries/sfm-ui/issues/320>`_)
* Collections are not portable between SFM instances (`Ticket #326 <https://github.com/gwu-libraries/sfm-ui/issues/326>`_)
* Harvest and export failures are not apparent in UI (`Ticket #310 <https://github.com/gwu-libraries/sfm-ui/issues/357>`_)
* SFM is not secure.  It does not currently run with HTTPS and enforcement of authorizations is not consistent in the UI.

We are planning to address these in future releases.  For a complete list of tickets, see https://github.com/gwu-libraries/sfm-ui/issues

In addition, you should be aware of the following:

* Access to the Weibo API is limited, so make sure you understand what can be collected.
* SFM does not currently provide a web interface for “replaying” the collected social media or web content.
* ELK is only experimental.  Scaling and administration of ELK have not been considered.
