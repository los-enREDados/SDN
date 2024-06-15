TOPOLOGY_FILE   := src/mytopo.py
TOPOLOGY_NAME   := mytopo
CONTROLLER_IP   := 127.0.0.1
CONTROLLER_PORT := 6633
NSWITCHES       := 4
IPERF           := iperf
SERVERPORT      := 8080
IPSERVER        := 10.0.0.1


install:
	cd pox/ext/; ln -s ../../src/firewall.py || true
	cd pox/ext/; ln -s ../../src/translator.py || true

run:
	pox/pox.py firewall forwarding.l2_learning log.level --DEBUG samples.pretty_log


mininet:
	mn --custom ${TOPOLOGY_FILE}  --topo ${TOPOLOGY_NAME},${NSWITCHES}  --controller remote,ip=${CONTROLLER_IP},port=${CONTROLLER_PORT}

create-server:
	${IPERF} -s -p ${SERVERPORT}

send-data:
	${IPERF} -c ${IPSERVER} -e -p ${SERVERPORT} 

