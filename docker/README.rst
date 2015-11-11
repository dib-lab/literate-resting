on local::

   docker create -v /mnt/data --name kp-test-data ubuntu:14.04 /bin/true

   docker run --volumes-from kp-test-data -it ubuntu:14.04 bash

on docker machine::

   apt-get install curl
   cd /mnt/data
   curl -O https://s3.amazonaws.com/public.ged.msu.edu/mrnaseq-subset.tar
   tar xf mrnaseq-subset.tar
   rm mrnaseq-subset.tar
