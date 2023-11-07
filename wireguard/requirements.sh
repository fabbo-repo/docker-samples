#!/bin/bash

# Docker y docker-compose:
apt install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
apt install -y docker docker-compose


mkdir -p /wiregurard/config
mkdir -p /wiregurard/lib/modules
sudo chown -R fabbo:/wiregurard
docker-compose up -d

# Revisar estado vpn
# docker exec -it wireguard wg