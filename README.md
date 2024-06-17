# SDN
## Instalar
Una vez clonado, se debe ejecutar el siguiente comando:
```console
git submodule update --init --recursive
```
Luego, para la configuración inicial, ejecutar:
```console
make install
```

## Ejecución del firewall
Para abrir POX y levantar el firewall, ejecutar:
```console
make run
```

### Modificación de políticas
Las políticas se encuentran en el archivo `policies.json` y tienen el siguiente formato:
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
Estas se pueden configurar de manera compleja, por ejemplo:
```json
{
    "src_ip": "10.0.0.1",
    "src_port": 80,
    "protocol": "TCP"
}
```
Esto bloquearía los paquetes provenientes de la dirección 10.0.0.1 utilizando el protocolo TCP en el puerto 80.

#### Aclaraciones
- Utilizar `banned_tuples` sin ninguna otra condición. Esto es un requisito, ya que añadir otras condiciones en `banned_tuples` es innecesario dado que el propósito es bloquear toda comunicación entre dos hosts.
- Tener en cuenta que si se desea bloquear un puerto, si es de origen (`src`), debe seguir dos formatos:
    <ol>
    <li> <b>Sin especificar protocolo:</b> esto bloquea el puerto deseado en los protocolos UDP o TCP.</li>
    <li> <b>Especificando el protocolo:</b> esto bloquea únicamente el puerto en el protocolo especificado. Notar que este puerto tiene que ser TCP o UDP para que tenga sentido lógico.</li>
    </ol>

## Probar con Mininet
### Encender OpenvSwitch
Mininet requiere que el daemon de OpenvSwitch esté activo para funcionar. Si no está activo, debe encenderse.

#### En systemd
```console
systemctl start ovsdb-server
```
#### En OpenRC
¡El orden es importante!
```console
rc-service ovsdb-server start
```
Y luego:
```console
rc-service ovs-vswitchd start
```

### Ejecutar Mininet
Para abrir Mininet (requiere permisos de root):

```console
sudo make mininet
```

Dentro de Mininet, abrir las terminales (usando xterm) de los hosts correspondientes:

```console
xterm h1 h2 h3
```

> Las IPs por defecto son de la forma hn = 10.0.0.n, por ejemplo h1 = 10.0.0.1.

Si se desea cambiar la cantidad de switches:

```console
sudo make mininet NSWITCHES=n
```

### Probar conexiones
Nota: Existen iperf 2.0 e iperf 3.0. Las instrucciones están disponibles para ambos.

#### Servidor
Iperf 2.0:
```console
iperf -s -p <port>
```
Iperf 3.0:
```console
iperf3 -s -p <port>
```
> Simula un servidor que acepta conexiones. Agregar la bandera `-u` al final para probar con UDP en lugar de TCP.

#### Cliente
Iperf 2.0:
```console
iperf -c <ip_addr> -e -p <port>
```
Iperf 3.0:
```console
iperf3 -c <ip_addr> -p <port>
```
> Simula un cliente que se conecta e intenta enviar paquetes al servidor alojado en la (ip, puerto) correspondiente. Agregar la bandera `-u` para probar con UDP en lugar de TCP.