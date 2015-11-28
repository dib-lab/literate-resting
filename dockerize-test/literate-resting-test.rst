=====================================================
A test for dockerizing protocols via literate-resting
=====================================================

To run this, do::

   ./extract-from-github.py https://github.com/dib-lab/literate-resting/tree/master/dockerize-test/ -o test
   cd test && ./build.sh

from within the root directory of the `literate-resting repo
<https://github.com/dib-lab/literate-resting/>`__.

You should end up with a docker image named ``diblab/literate-resting-test``


Adding commands to the Dockerfile
---------------------------------

(Look at the source code.)

.. docker::

   # this comment will end up in the Dockerfile used to build the docker
   # containers; you could also put commands here.


Adding commands to the Docker CMD script
----------------------------------------

.. shell start

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

.. shell stop
