## Public IPv4 address
 54.169.179.151

## Public IPv4 DNS
 ec2-54-169-179-151.ap-southeast-1.compute.amazonaws.com

## Private IPv4 addresses
 172.31.16.15

## Private IPv4 DNS
 ip-172-31-16-15.ap-southeast-1.compute.internal


# SSH - Access
use pmi-key-pair.pem if want to access PMI instance

## access key
update permission file before use. Example chmod 600 pmi-key-pair.pem

## example
ssh -i pmi-key-pair.pem ubuntu@54.169.179.151