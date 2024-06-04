install:
	cd pox/ext/; ln -s ../../src/firewall.py

run:
	pox/pox.py firewall forwarding.l2_learning log.level --DEBUG samples.pretty_log
