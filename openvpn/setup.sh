#!/bin/bash

echo "---------------------------------------------"
echo "    Configuracion de servidor OpvenVPN"
echo "---------------------------------------------"

BASE_PATH="/openvpn"
OVPN_DATA="$BASE_PATH/conf"
echo "IP/dominio del servidor: "
read SERVER_NAME

docker run -v $OVPN_DATA:/etc/openvpn --rm kylemanna/openvpn ovpn_genconfig -u udp://$SERVER_NAME

docker run -v $OVPN_DATA:/etc/openvpn --rm -it kylemanna/openvpn ovpn_initpki

echo "---------------------------------------------"
echo "    Fin"
echo "---------------------------------------------"