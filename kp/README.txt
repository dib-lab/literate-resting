Mount snap-XXXX as /data-full; then run.


cd /root
rm -fr literate-resting khmer-protocols
git clone https://github.com/ged-lab/literate-resting.git
git clone https://github.com/ged-lab/khmer-protocols.git -b acceptance

cd khmer-protocols/mrnaseq
/root/literate-resting/scan.sh 1-quality.txt.sh 2-diginorm.txt.sh
