#!/bin/bash

# Adapt this path for your needs
BASE_PATH="/openvpn"
OVPN_DATA="$BASE_PATH/data"
USER_LIST="$BASE_PATH/listusers.txt"

function listclients () {
    echo "Listing current clients"
    docker-compose run --rm openvpn ovpn_listclients > ${USER_LIST}
}


function addclient () {
    echo "### Generate client cert"
    read -p "Enter the user's name:" CLIENTNAME

    # if user exists, delete it.
    if [[ $(cat ${USER_LIST} | grep -c ${CLIENTNAME}) -ne 0 ]]; then
        docker-compose run --rm openvpn ovpn_revokeclient ${CLIENTNAME} remove
    fi
    # Generate certificates
    docker run -v $OVPN_DATA:/etc/openvpn --rm -it kylemanna/openvpn easyrsa build-client-full ${CLIENTNAME} nopass
}

function CREATE_OVPN_FILE () {
    echo "# Retrieve config"
    if [[ ! -d ${BASE_PATH}/clients ]]; then mkdir ${BASE_PATH}/clients; fi
    docker run -v ${OVPN_DATA}:/etc/openvpn --rm kylemanna/openvpn ovpn_getclient ${CLIENTNAME} > "${BASE_PATH}/clients/${CLIENTNAME}.ovpn"
    echo "# Wrote config to folder clients"
}

function restart () {
    docker restart openvpn
}

function email () {
    cat listusers.txt
    read -p "Name of client's OVPN to send?"  NAME
    read -p "Email to send the OVPN file to?:"  EMAIL

    dpkg -l | grep mpack || sudo apt install mpack

    if ! [[ -z ${EMAIL} ]]; then mpack -s subject "${BASE_PATH}/clients/${NAME}.ovpn" ${EMAIL}; fi
}