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
