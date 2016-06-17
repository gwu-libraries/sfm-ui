==============================
 Limitations and Known Issues
==============================

To make sure you have the best possible experience with SFM, you should be aware of the limitations and known issues:

* Exporting social media data from WARC files is slow (`Ticket #340 <https://github.com/gwu-libraries/sfm-ui/issues/340>`_)
* Better monitoring and logging for harvesting and exporting is needed (`Ticket #303 <https://github.com/gwu-libraries/sfm-ui/issues/303>`_ and `Ticket #229 <https://github.com/gwu-libraries/sfm-ui/issues/229>`_)
* Twitter search doesn’t quite work right and may block other harvest requests (`Ticket #320 <https://github.com/gwu-libraries/sfm-ui/issues/320>`_)
* Collections are not portable between SFM instances (`Ticket #326 <https://github.com/gwu-libraries/sfm-ui/issues/326>`_)
* Web harvester (Heritrix) failing on large crawls (`Ticket #321 <https://github.com/gwu-libraries/sfm-ui/issues/321>`_)
* Harvest and export failures are not apparent in UI (`Ticket #310 <https://github.com/gwu-libraries/sfm-ui/issues/310>`_)
* SFM is not secure.  It does not currently run with HTTPS and enforcement of authorizations is not consistent in the UI.

We are planning to address these in future releases.  For a complete list of tickets, see https://github.com/gwu-libraries/sfm-ui/issues

In addition, you should be aware of the following:

* Access to the Weibo API is limited, so make sure you understand what can be collected.
* SFM does not currently provide a web interface for “replaying” the collected social media or web content.
* ELK is only experimental.  Scaling and administration of ELK have not been considered.
