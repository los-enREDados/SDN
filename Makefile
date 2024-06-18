LATEX           := pdflatex --synctex=1 -file-line-error
TOPOLOGY_FILE   := src/mytopo.py
TOPOLOGY_NAME   := mytopo
CONTROLLER_IP   := 127.0.0.1
CONTROLLER_PORT := 6633
NSWITCHES       := 4
IPERF           := iperf3
PORT            := 8080
IP              := 10.0.0.1
PROT            := TCP
PROTFLAGS       :=
SWITCHID        := 3
LOG_FILE = log.txt

# IPERFFLAGS      := 
ifeq (${IPERF}, iperf)
	IPERFFLAGS += -e
else
	IPERFFLAGS += -V
endif

ifeq (${PROT}, TCP)
	PROTFLAGS += 
else
	PROTFLAGS += -u
endif


.PHONY: informe

install:
	cd pox/ext/; ln -s ../../src/firewall.py || true
	cd pox/ext/; ln -s ../../src/translator.py || true

cambiarID:
	sed -i 's/IPDELSWITCHCONELFIREWALL = [0-9]/IPDELSWITCHCONELFIREWALL = ${SWITCHID}/' src/firewall.py

run: cambiarID
	pox/pox.py firewall forwarding.l2_learning log.level --DEBUG samples.pretty_log log --file=${LOG_FILE}


mininet:
	mn --custom ${TOPOLOGY_FILE}  --topo ${TOPOLOGY_NAME},${NSWITCHES}  --controller remote,ip=${CONTROLLER_IP},port=${CONTROLLER_PORT}

create-server:
	${IPERF} -s -p ${PORT}

send-data:
	${IPERF} -c ${IP} ${IPERFFLAGS} -p ${PORT} ${PROTFLAGS}

informe:
	$(LATEX) --shell-escape  informe/informe.tex

