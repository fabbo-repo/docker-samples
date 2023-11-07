[Documentacion](https://github.com/pi-hole/docker-pi-hole/blob/master/README.md)

En caso de conflicto con el puerto 53, ejecutar:
~~~
sudo systemctl stop systemd-resolved
~~~
~~~
sudo nano /etc/systemd/resolved.conf
~~~
Modifica estas lineas (estan comentadas):
> DNS=8.8.8.8\
> DNSSTubeListener=no
~~~
sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf
~~~