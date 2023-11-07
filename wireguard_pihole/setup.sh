#!/bin/bash

echo "----------------------------------------------"
echo "             Wireguard con Pihole"
echo "----------------------------------------------"

mkdir "wireguard"; chmod 777 -R "wireguard"
mkdir "pihole"; chmod 777 -R "pihole"
mkdir "dnsmasq.d"; chmod 777 -R "dnsmasq.d"
docker-compose up -d
ufw allow 51820