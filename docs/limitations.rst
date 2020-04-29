==============================
 Limitations and Known Issues
==============================

To make sure you have the best possible experience with SFM, you should be aware of the limitations and known issues:

* Changes to the hostname of server (e.g., from the reboot of an AWS EC2 instance) are not handled (`Ticket 435 <https://github.com/gwu-libraries/sfm-ui/issues/435>`_). See also `Troubleshooting <https://sfm.readthedocs.io/en/latest/troubleshooting.html>`_

* The README file when downloaded and opened in Notepad (Early versions of Windows 10 or below) lacks linebreaks since Notepad cannot read the linebreaks specified within the code.
  This issue was fixed by Microsoft in the Windows 10 version 1809 (October 2018) of Notepad and the file opens up in the expected format (`Ticket 1002 <https://github.com/gwu-libraries/sfm-ui/issues/1002>`_).

  If you are using early versions of Windows 10 or below use Windows WordPad to open the README file since it renders the file in the correct format with appropriate linebreaks.

For a complete list of tickets, see https://github.com/gwu-libraries/sfm-ui/issues

In addition, you should be aware of the following:

* Access to the Weibo API is limited, so make sure you understand what can be collected.
* SFM does not currently provide a web interface for "replaying" the collected social media or web content.
