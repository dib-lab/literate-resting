#! /bin/bash
set -x
set -e

for i in [1-3]*.rst
do

  DIR=docker-$(basename $i .rst)
  mkdir $DIR
  ~/dev/literate-resting/scan.py -x -o ${DIR}/$i.sh $i

  cat <<EOF > $DIR/Dockerfile
FROM ubuntu:14.04

EOF
done
