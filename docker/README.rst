Create docker containers from khmer-protocols ctb branch
--------------------------------------------------------

::

   ./extract-from-github.py https://github.com/dib-lab/khmer-protocols/tree/ctb/mrnaseq
   cd ./output/
   bash build.sh

This will create docker images 'eel-pond/1-quality:ctb', etc. ('ctb' from
the branch, 'eel-pond' from literate-resting.json in the mrnaseq/ subdir,
'1-quality' from the .rst filename.)

Configure data volumes
----------------------

Load the data to be assembled::

   docker create -v /mnt --name kp-test-data ubuntu:14.04 /bin/true
   docker run --rm --volumes-from kp-test-data -it diblab/kp-base bash

then on the docker machine::

   mkdir /mnt/data
   cd /mnt/data
   curl -O https://s3.amazonaws.com/public.ged.msu.edu/mrnaseq-subset.tar
   tar xf mrnaseq-subset.tar
   rm mrnaseq-subset.tar

Run the three khmer-protocols docker images
-------------------------------------------

::

     docker run --volumes-from kp-test-data -it eel-pond/1-quality:ctb
     docker run --volumes-from kp-test-data -it eel-pond/2-diginorm:ctb
     docker run --volumes-from kp-test-data -it eel-pond/3-big-assembly:ctb

Assembly will be on 'kp-test-data' data volume under
/mnt/work/trinity_out_dir/Trinity.fasta; you can access it like so::

     docker cp kp-test-data:/mnt/work/trinity_out_dir/Trinity.fasta .

