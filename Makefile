install:
	cd pox/ext/; ln -s ../../src/firewall.py

run:
	pox/pox.py firewall forwarding.l2_learning log.level --DEBUG samples.pretty_log

TOPOLOGY_FILE   := src/mytopo.py
TOPOLOGY_NAME   := mytopo
CONTROLLER_IP   := 127.0.0.1
CONTROLLER_PORT := 6633

mininet:
	mn --custom ${TOPOLOGY_FILE}  --topo ${TOPOLOGY_NAME}  --controller remote,ip=${CONTROLLER_IP},port=${CONTROLLER_PORT}


