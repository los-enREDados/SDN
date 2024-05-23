from mininet import Mininet
from mininet.node import Host, OVSSwitch

from mininet.topo import Topo
from mininet.link import TCLink


class MyTopo(Topo):
    def __init__(self, cant_switches=5):
        Topo.__init__(self)
        # Add hosts and switches
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        # Primer parte: h1 y h2 conectados al primer switch
        s1 = self.addSwitch('s1')
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        
        # Segunda parte: todos los switches linearmente conectados
        prev_switch = s1
        for i in range(2, cant_switches): 
            switch = self.addSwitch('s{i}'.format(i=i))
            self.addLink(prev_switch, switch)
            prev_switch = switch


        # Tercer parte: h3 y h4 conectados al ultimo switch
        self.addLink(h3, switch)
        self.addLink(h4, switch)

        # Dejo este comentario por si necesitamos ponerle perdida, se hace asi        
        # self.addLink(cliente2, switch, cls=TCLink, loss=10)
        """
        h1                          h3
          \                       /
            s1 -- s2 -- ... -- sn
          /                       \
        h2                          h4
        """

topos = {'mytopo': (lambda: MyTopo())}


def main():
    red = Mininet(topo=MyTopo(5), link=TCLink)

    # Inicia la red y ejecuta un comando.
    red.start()
    red.pingAll()
    red.stop()


if __name__ == '__main__':
    main()