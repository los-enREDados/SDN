'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''



log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]

''' Add your global variables here ... '''



class Firewall (EventMixin):
    
    def __init__ (self):
        self.firewall_switch_dpid = 1
        self.i = 0
        self.listenTo(core.openflow)


    def _handle_ConnectionUp (self, event):
        ''' Add your logic here ... '''
        if self.firewall_switch_dpid != event.dpid:
            return
        
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

        my_match = of.ofp_match(
            nw_proto=1, dl_type=0x800
        )
        flow_mod = of.ofp_flow_mod(match=my_match)
        event.connection.send(flow_mod)




def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
