================
 Administration
================

----------------
 Admin Interace
----------------

Designated users have access to SFM UI's `Django Admin interface <LINK>`_ by selecting Welcome > Admin on the top
right of the screen. This interface will allow adding, deleting, or changing database records for SFM UI. Some
of the most salient uses for this capability are given below.

Managing groups
===============
To allow for multiple users to control a collection set:
1. Create a new group.
2. Add users to the group. (This is done from the user's admin page, not the group's admin page.)
3. Assign the collection set to the group. This is done from the collection set detail page or from the collection
set admin page.

Deleting items
==============
Records can be deleted using the Admin Interface. It is recommended to minimize deletion; in particular, collections
should be turned off and seeds made inactive.

Note the following when deleting:
* Cascades delete, i.e., when a record is deleted any other records that depend on it will also be deleted. Before
the deletion is performed, you will be informed what dependent records will be deleted.
* When deleting collection sets, collections, harvests, WARCs, and exports *the corresponding files will be deleted*.
Thus, if you delete a collection set *all* data and metadata will be deleted. **Be careful.**

Allowing access to Admin Interface
==================================
To allow a user to have access to the Admin Interface, give the user Staff status or Superuser status. This is done
from the user's admin page.