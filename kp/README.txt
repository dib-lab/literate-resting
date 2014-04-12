This is an initial stab at khmer acceptance testing, based on khmer
protocols/eel pond.  To run, execute the following commands on an AWS
m1.xlarge machine running AMI ami-c17ec8a8.

For more info on khmer, see github.com/ged-lab/khmer, and
khmer.readthedocs.org/.

For more info on khmer-protocols, see github.com/ged-lab/khmer-protocols,
and khmer-protocols.readthedocs.org/.

---

Note that the branch of khmer under test is specified in
mrnaseq/1-quality.txt in the khmer-protocols repository; CTB suggests
that to run an acceptance test against a specific version of khmer, we
create a new branch of khmer-protocols on github.com/ged-lab that
specifies the right version in mrnaseq/1-quality.txt, and then put '-b
branchname' in the clone command below.

---

Run this on an Ubuntu 12.04 LTS system as root:

apt-get update
apt-get -y install screen git curl gcc make g++ python-dev unzip default-jre \
        pkg-config libncurses5-dev r-base-core r-cran-gplots python-matplotlib\
        sysstat && shutdown -r now

## After reboot:

mkdir /mnt/data
ln -fs /mnt/data /data
cd /data
curl -O http://athyra.idyll.org/~t/mrnaseq-subset.tar
tar xvf mrnaseq-subset.tar

cd /root
rm -fr literate-resting khmer-protocols
git clone https://github.com/ged-lab/literate-resting.git
#git clone https://github.com/ged-lab/khmer-protocols.git -b release-test
git clone https://github.com/ged-lab/khmer-protocols.git -b bench

cd khmer-protocols/mrnaseq

for i in [1-8]-*.txt
do
   bash /root/literate-resting/scan.sh $i
done

### START MONITORING

for i in [1-8]-*.txt.sh
do
   bash $i
done

---

Successful completion can be checked by hand in two ways, after running::

   bash /root/literate-resting/scan.sh acceptance-3-big-assembly.txt
   bash acceptance-3-big-assembly.txt.sh

FIRST, you should see stats output from this command::

   /usr/local/share/khmer/sandbox/assemstats3.py 500 /mnt/work/trinity_out_dir/Trinity.fasta

that looks roughly like this::

   ** cutoff: 500
   N       sum     max     filename
   76      134259  4452    /mnt/work/trinity_out_dir/Trinity.fasta

SECOND the command ::

   grep "zinc transporter" trinity.x.mouse /mnt/blast/trinity.x.mouse

should show more than 20 matches.

---

To run system monitoring::

   sar -u -r -d -o times.dat 1

   sar -d -p -f times.dat > disk.txt
   sar -u -f times.dat > cpu.txt
   sar -r -f times.dat > ram.txt
   gzip *.txt

See github.com/ctb/sartre/ for parsing tools for sar output.
