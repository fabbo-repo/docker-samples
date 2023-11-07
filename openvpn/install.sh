#!/bin/bash

# Si no existe un directorio para openvn, se crea
if [ ! -d /openvpn ] ; then
  mkdir /openvpn
fi

# Si no existe un directorio para conf, se crea
if [ ! -d /openvpn/conf ] ; then
  mkdir /openvpn/conf
fi

echo "Usuario non-root del sistema: "
read NONROOTUSER
# Permisos de usuario non-root
chown -R $NONROOTUSER: /openvpn

./setup.sh
docker-compose up -d openvpn

# Generar certificado para clientes
./createClient.sh

# Obtener configuracion de clientes:
# docker exec -it openvpn ovpn_getclient $CLIENTNAME > $CLIENTNAME.ovpn

# Eliminar certificado de cliente:
# - Manteniendo los archivos crt, key y req.
# docker-compose run --rm openvpn ovpn_revokeclient $CLIENTNAME
# - Eliminando los archivos crt, key y req.
# docker-compose run --rm openvpn ovpn_revokeclient $CLIENTNAME remove