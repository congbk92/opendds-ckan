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
     - docker run --net=subnet --rm -v "$PWD:$PWD" -w "$PWD" opendds-ckan python3 ./source/run.py run -t publisher -i template/Messenger.idl -n template/relay_rtps.ini
     - docker run --net=pubnet --rm -v "$PWD:$PWD" -w "$PWD" opendds-ckan python3 ./source/run.py run -t subscriber -i template/Messenger.idl -n template/relay_rtps.ini
 #### How to verify the idl file
  - docker run --net=pubnet --rm -v "$PWD:$PWD" -w "$PWD" opendds-ckan python3 ./source/run.py check -i {path_of__the_idl_file}
