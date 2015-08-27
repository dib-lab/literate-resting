First, the sudo::

   sudo chmod a+rwxt /mnt
   sudo apt-get -y install git-core

Then, the khmer protocols stuff::

   cd /home/ubuntu
   rm -fr literate-resting khmer-protocols
   git clone https://github.com/dib-lab/literate-resting.git
   git clone https://github.com/dib-lab/khmer-protocols.git -b ctb

   cd khmer-protocols/metagenomics

Then::

   for i in [1-4]-*.rst
   do
      /home/ubuntu/literate-resting/scan.py $i
   done
   
### START MONITORING HERE ###

And finally::

   for i in [1-4]-*.rst.sh
   do
      bash $i
   done
