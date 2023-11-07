#!/bin/bash

BASE_PATH="/openvpn"
OVPN_DATA="$BASE_PATH/conf"

echo
echo "---------------------------------------------"
echo "Nombre de cliente: "
read CLIENTNAME
echo "---------------------------------------------"

docker run -v $OVPN_DATA:/etc/openvpn --rm -it kylemanna/openvpn easyrsa build-client-full $CLIENTNAME

echo "---------------------------------------------"
echo "    Guardando configuracion de cliente"
echo "---------------------------------------------"

# Si no existe un directorio para clientes, se crea
if [ ! -d $BASE_PATH/clients ] ; then
  mkdir $BASE_PATH/clients
fi

docker run -v $OVPN_DATA:/etc/openvpn --rm kylemanna/openvpn ovpn_getclient $CLIENTNAME > "$BASE_PATH/clients/$CLIENTNAME.ovpn"

echo "---------------------------------------------"
echo "    Fin"
echo "---------------------------------------------"
