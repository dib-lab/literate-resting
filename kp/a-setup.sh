mkdir /mnt/data
ln -fs /mnt/data /data

cd /data-full
for i in *001.fastq.gz
do
   gunzip -c $i | head -100000 | gzip > /data/$i
done
