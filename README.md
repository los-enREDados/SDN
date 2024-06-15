# SDN
## Instalar
Una vez clonado se tiene que correr el siguiente comando:
```console
git submodule update --init --recursive
```
Luego para el setup correr:
```console
make install 
```

## Ejecuccion de firewall
Para abrir pox y levantar el firewall correr:
```console
make run
```

### Modificacion de policies
Las policies se encuentran en el archivo `policies.json` y tienen el siguiente formato:
```json
    {
        "src_ip": "0.0.0.0",
        "dst_ip": "0.0.0.0",
        "src_port": 0,
        "dst_port": 0,
        "protocol": "protocol",
        "banned_tuples": ["0.0.0.0","0.0.0.0"]
    }

```
Estas se pueden crear complejas como por ejemplo:
```json
    {
        "src_ip": "10.0.0.1",
        "src_port": 80,
        "protocol": "TCP"
    }

```
Que bloquearia los paquetes provenientes del la direccion 10.0.0.1 envias utilizando el protocolo TCP en el puerto 80.


#### Aclaraciones
- utilizar `banned_tuples` sin ningun otra condicion. Esto es requisito ya que poner otras condiciones en banned_tuples es inecesario ya que el proposito es bloquear todo tipo de comunicacion entre dos hosts

- Considerar que si se quiere bloquear un puerto sea de src tiene que seguir dos formatos:
    <ol>
    <li>  <b>Sin especificar protocolo:</b> esto bloquea el puerto deseado en los protocolos UDP o TCP   
    <li>  <b>Especificando el protocolo:</b> esto bloquea solamente el puerto en el protocolo especificado. Notar que este puerto tiene que ser TCP o UDP para que tenga sentido logico. 
    </ol>

## Probar con mininet
### Prender OpenVS switch
Mininet necesita que el daemon de OpenVS switch esté encendido para funcionar.
En caso de que no esté encendido, se tiene que encender.
#### En systemdD
```console
systemctl start ovsdb-server
```
#### En OpenRC
```console
rc-service ovsdb-server start
```

### Correr mininet
Para probar abrir mininet (requiere permisos de root):

```console
sudo make mininet
```

Luego dentro de mininet abrir las terminales (utilizando xterm) de los hosts correspondientes


```console
xterm h1 h2 h3
```

> las ips por default son hn = 10.0.0.n como por ejemplo h1 = 10.0.0.1


### Probar conexiones
#### Server
```console
iperf -s -p <port> 
```
>Simula un servidor el cual acepta conexiones. Agregar la flag `-u` al final para testear con UDP enves de TCP

#### Cliente
```console
iperf -c <ip_addr> -e -p <port> 
```
> Simula un cliente el cual se conecta y intenta enviar paquetes al servidor hosteado en la (ip,port) correspondiente. Agregar la flag `-u` para testear con UDP enves de TCP.
