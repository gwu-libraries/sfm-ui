=====================
 Writing a harvester
=====================

--------------
 Requirements
--------------

* Implement the :doc:`messaging_spec` for harvesting social media content.
  This describes the messages that must be consumed and produced by a harvester.
* Write harvested social media to a `WARC <http://iipc.github.io/warc-specifications/>`_,
  following all relevant guidelines and best practices. The message for announcing the
  creation of a WARC is described in the Messaging Specification. The WARC file must be
  written to `<base path>/<harvest year>/<harvest month>/<harvest day>/<harvest hour>/`,
  e.g., `/data/test_collection_set/2015/09/12/19/`. (Base path is provided in the harvest start
  message.) Any filename may be used but it must end in `.warc` or `.warc.gz`. It is recommended
  that the filename include the harvest id (with file system unfriendly characters removed) and
  a timestamp of the harvest.
* Extract urls for related content from the harvested social media content, e.g., a photo included
  in a tweet. The message for publishing the list of urls is described in the Messaging Specification.
* Document the harvest types supported by the harvester. This should include the identifier of the
  type, the API methods called, the required parameters, the optional parameters, what is included
  in the summary, and what urls are extracted. See the `Flickr
  Harvester <https://github.com/gwu-libraries/sfm-flickr-harvester#harvest-start-messages>`_ as an example.
* The `smoke tests <https://github.com/gwu-libraries/sfm-docker/tree/master/smoke_tests>`_
  must be able to prove that a harvester is up and running. At the very least, the
  smoke tests should check that the queues required by a harvester have been created. (See
  `test_queues() <https://github.com/gwu-libraries/sfm-docker/blob/master/smoke_tests/test_mq.py>`_.)
* Be responsible for its own state, e.g., keeping track of the last tweet harvested from a user timeline.
  See `sfmutils.state_store <https://github.com/gwu-libraries/sfm-utils/blob/sfm_t46-twitter_harvester/sfmutils/state_store.py>`_
  for re-usable approaches to storing state.
* Create all necessary exchanges, queues, and bindings for producing and consuming messages
  as described in :doc:`messaging`.
* Provide master and production Docker images for the harvester on `Docker Hub <https://hub.docker.com/>`_.
  The master image should have the `master` tag and contain the latest code from the master branch.
  (Setup an `automated build <https://docs.docker.com/docker-hub/builds/>`_ to simplify updating the master image.)
  There must be a version specific production images, e.g., `1.3.0` for each release. For example, see the Flickr
  Harvester's `dockerfiles <https://github.com/gwu-libraries/sfm-flickr-harvester/tree/master/docker>`_
  and `Docker Hub repo <https://hub.docker.com/r/gwul/sfm-flickr-harvester/>`_.

-------------
 Suggestions
-------------

* See `sfm-utils <https://github.com/gwu-libraries/sfm-utils>`_ for re-usable harvester
  code. In particular, consider subclassing BaseHarvester.
* Create a development Docker image. The development Docker images links in the code outside
  of the container so that a developer can make changes to the running code. For example, see
  the `Flickr harvester development image <https://github.com/gwu-libraries/sfm-flickr-harvester/tree/master/docker/dev>`_.
* Create a development `docker-compose.yml`. This should include the development Docker image
  and only the additional images that the harvester depends on, e.g., a Rabbit container. For
  example, see the `Flickr harvester development docker-compose.yml <https://github.com/gwu-libraries/sfm-flickr-harvester/blob/master/docker/dev.docker-compose.yml>`_.
* When possible, use existing API libraries.
* Consider write integration tests that test the harvester in an integration test environment.
  (That is, an environment that includes the other services that the harvester depends on.)
  For example, see the Flickr Harvester's `integration tests <https://github.com/gwu-libraries/sfm-flickr-harvester/blob/master/tests/test_flickr_harvester.py>`_.
* See the `Twitter harvester unit tests <https://github.com/gwu-libraries/sfm-twitter-harvester/blob/master/tests/__init__.py>`_
  for a pattern on configuring API keys in unit and integration tests.

-------
 Notes
-------

* Harvesters can be written in any programming language.
* Changes to gwu-libraries/* repos require pull requests. Pull requests are welcome
  from non-GWU developers.