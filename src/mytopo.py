from mininet.node import Host, OVSSwitch

from mininet.topo import Topo
from mininet.link import TCLink


class MyTopo(Topo):
    def __init__(self, cant_switches=4):
        Topo.__init__(self)
        # Add hosts and switches
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

        # Primer parte: h1 y h2 conectados al primer switch
        s1 = self.addSwitch('s1')
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        
        # Segunda parte: todos los switches linearmente conectados
        prev_switch = s1
        for i in range(2, cant_switches+1): 
            switch = self.addSwitch('s{i}'.format(i=i))
            self.addLink(prev_switch, switch)
            prev_switch = switch


        # Tercer parte: h3 conectado al ultimo switch
        self.addLink(h3, prev_switch)

        """
        h1                          
          \\                       
            s1 -- s2 -- ... -- sn -- h3
          /                       
        h2                          
        """

topos = {'mytopo': MyTopo}


