This is an initial stab at khmer acceptance testing, based on khmer
protocols/eel pond.  To run, execute the following commands on
ami-c17ec8a8.  Note that the branch of khmer under test is specified
in mrnaseq/1-quality.txt.

---

mkdir /mnt/data
ln -fs /mnt/data /data
cd /data
curl -O http://athyra.idyll.org/~t/mrnaseq-subset.tar
tar xvf mrnaseq-subset.tar

cd /root
rm -fr literate-resting khmer-protocols
git clone https://github.com/ged-lab/literate-resting.git
git clone https://github.com/ged-lab/khmer-protocols.git -b acceptance

cd khmer-protocols/mrnaseq
/root/literate-resting/scan.sh 1-quality.txt
/root/literate-resting/scan.sh 2-diginorm.txt
/root/literate-resting/scan.sh 3-big-assembly.txt

bash 1-quality.txt.sh
bash 2-diginorm.txt.sh
bash 3-big-assembly.txt.sh

---

Successful completion can be checked by hand in two ways.

FIRST, you should see stats output from this command::

   /usr/local/share/khmer/sandbox/assemstats3.py 500 /mnt/work/trinity_out_dir/Trinity.fasta

that looks roughly like this::

   ** cutoff: 500
   N       sum     max     filename
   76      134259  4452    /mnt/work/trinity_out_dir/Trinity.fasta

SECOND the command ::

   grep "zinc transporter" trinity.x.mouse /mnt/blast/trinity.x.mouse

should show more than 20 matches.
