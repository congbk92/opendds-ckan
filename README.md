# opendds-ckan

## Build opendds-ckan docker
 - docker build -t opendds-ckan .

### How to run an example:
 - Create a network for the publisher
    - docker network create pubnet
 - Create a network for the subscriber
    - docker network create subnet
  - Create a container for the relay, connect it to both networks, and start it
     - docker create --name=relay --rm -ti --net=pubnet -w /opt/OpenDDS/tools/rtpsrelay objectcomputing/opendds:relay ./RtpsRelay -DCPSConfigFile rtps.ini
     - docker network connect subnet relay
     - docker start relay
     - docker run --net=pubnet opendds-ckan python3 ./source/run.py public
     - docker run --net=subnet opendds-ckan
