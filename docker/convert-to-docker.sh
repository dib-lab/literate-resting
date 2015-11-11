#! /bin/bash
set -x
set -e

rm -f docker-build.sh

for i in [1-3]*.rst
do

  DIR=docker-$(basename $i .rst)
  rm -fr ${DIR}
  mkdir ${DIR}
  DOCKERCMDS=$(~/dev/literate-resting/scan-tag.py docker $i -o -)
  ~/dev/literate-resting/scan.py -x -o ${DIR}/$i.sh $i
  chmod +x ${DIR}/$i.sh

  cat <<EOF > ${DIR}/Dockerfile
FROM kp-base
${DOCKERCMDS}
COPY $i.sh /home
ENTRYPOINT ["/home/$i.sh"]
EOF

  echo docker build -t kp/$(basename $i .rst) ${DIR} >> docker-build.sh

done
