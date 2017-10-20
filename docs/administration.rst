================
 Administration
================

Designated users have access to SFM UI's `Django Admin interface <https://docs.djangoproject.com/en/1.8/ref/contrib/admin/>`_
by selecting Welcome > Admin on the top
right of the screen. This interface will allow adding, deleting, or changing database records for SFM UI. Some
of the most salient uses for this capability are given below.

---------------
Managing groups
---------------
To allow for multiple users to control a collection set:

1. Create a new group.
2. Add users to the group. (This is done from the user's admin page, not the group's admin page.)
3. Assign the collection set to the group. This is done from the collection set detail page or from the collection
   set admin page.

------------------------
Deactivating collections
------------------------
Deactivating a collection indicates that you have completed collecting data for that collection. Deactivated collections
will be removed from some of the lists in SFM UI and will not appear in the harvest status emails.

Collections can be deactivated using the "Deactivate" button on the collection detail page.

Note:

* A deactivated collection can be re-activated from the collection detail page. A deactivated collection must be
  re-activated before it can be edited or turned on.
* A collection set is considered deactivated when it has no active collections. It will also be removed from some of the
  lists in SFM UI and not appear in harvest status emails.

-------------------
Sharing collections
-------------------
Changing the visibility of a collection to "Other users" will allow the collection to be viewed by all SFM users.

The visibility of a collection can be changed by editing the collection.

Note:
* A collection set is shared when it has a shared collection.
* Shared collection sets will be listed on a separate tab of the collection set list page.

--------------
Deleting items
--------------
Records can be deleted using the Admin Interface. It is recommended to minimize deletion; in particular, collections
should be turned off and seeds made inactive.

Note the following when deleting:

* Cascades delete, i.e., when a record is deleted any other records that depend on it will also be deleted. Before
  the deletion is performed, you will be informed what dependent records will be deleted.
* When deleting collection sets, collections, harvests, WARCs, and exports *the corresponding files will be deleted*.
  Thus, if you delete a collection set *all* data and metadata will be deleted. **Be careful.**

------------------
Moving collections
------------------
Collections can be moved from one collection set to another. This is done by changing the collection set for the
collection in the Admin Interface.

Note the following when moving collections:

* The collections files are moved as well, as the directory structure includes the collection set's identifier.
* The path for WARC files in WARC records are updated.
* Make sure harvesting is turned off and all harvests and exports are completed before moving.
* Previous exports will become unavailable after the move.

----------------------------------
Allowing access to Admin Interface
----------------------------------
To allow a user to have access to the Admin Interface, give the user Staff status or Superuser status. This is done
from the user's admin page.