=====================================================
A test for dockerizing protocols via literate-resting
=====================================================

Adding commands to the Dockerfile
---------------------------------

(Look at the source code.)

.. docker::

   # this command will end up in the Dockerfile used to build the docker
   # containers.


Adding commands to the Docker CMD script
----------------------------------------

The following commands (including the invisible ones; see the source)
will be added to the Docker container's CMD script,
``literate-resting-test.rst.sh``.

.. ::

   echo 'Hello, world'

This command:
::

   echo 'Howdy, there.

Displaying commands that are *not* added to the CMD script
----------------------------------------------------------

The following command is *visible* in the tutorial but is *not* added to
the CMD script::

   echo 'No dice, guv.'
