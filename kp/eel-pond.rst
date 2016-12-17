This is an initial stab at khmer acceptance testing, based on khmer
protocols/eel pond.  To run, execute the following commands on an AWS
m1.xlarge machine running the ubuntu-trusty-14.04-amd64-server-* 
Amazon Machine Image (AMI) which is one of the featured AMIs. This was
last tested using "ubuntu-trusty-14.04-amd64-server-20140927 (ami-98aa1cf0)"

For more info on khmer, see github.com/dib-lab/khmer, and
khmer.readthedocs.org/.

For more info on khmer-protocols, see github.com/dib-lab/khmer-protocols,
and khmer-protocols.readthedocs.org/.

---

Note that the branch of khmer under test is specified in
mrnaseq/1-quality.txt in the khmer-protocols repository; CTB suggests
that to run an acceptance test against a specific version of khmer, we
create a new branch of khmer-protocols on github.com/dib-lab that
specifies the right version in mrnaseq/1-quality.txt, and then put '-b
branchname' in the clone command below.

---

Do that sudo you do so well::

   sudo apt-get update && sudo apt-get install -y git-core

Next, ::
   
   cd /home/ubuntu
   rm -fr literate-resting eel-pond
   git clone https://github.com/dib-lab/literate-resting.git
   git clone https://github.com/dib-lab/eel-pond.git -b literate-resting
   
   cd eel-pond
   
   ## vim 1-quality.rst # change version number on line 49 to match the release to test

   ~/literate-resting/scan.py 0-install-aws.rst
   for i in [1-3]-*.rst
   do
      /home/ubuntu/literate-resting/scan.py $i || break
   done
   
   ### START MONITORING (in another SSH session)

   bash 0-install-aws.rst.sh
   for i in [1-3]-*.rst.sh
   do
      bash $i |& tee ${i%%.rst.sh}.out || break
   done

---

To run system monitoring::

   sar -u -r -d -o times.dat 1

   sar -d -p -f times.dat > disk.txt
   sar -u -f times.dat > cpu.txt
   sar -r -f times.dat > ram.txt
   gzip *.txt

See github.com/ctb/sartre/ for parsing tools for sar output.
