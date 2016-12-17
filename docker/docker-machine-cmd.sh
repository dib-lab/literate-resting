docker-machine create --driver amazonec2 --amazonec2-access-key ${AWS_KEY} --amazonec2-secret-key ${AWS_SECRET} --amazonec2-vpc-id ${VPC_ID} --amazonec2-zone b --amazonec2-instance-type m3.xlarge --amazonec2-root-size 50 aws01

#   docker-machine start aws04
#   docker-machine status aws04
#   docker-machine regenerate-certs aws04
#   eval $(docker-machine env aws04)

#   aws ec2 describe-subnets