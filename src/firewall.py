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
from pox.lib.addresses import IPAddr
from collections import namedtuple
from translator import protToNumber
import pox.lib.packet as pkt
import os
import json
''' Add your imports here ... '''



log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]

''' Add your global variables here ... '''

"""
Cosas que se pueden bloquear:
- Puerto destino y origen
- Numero de host origen y destino
- Protocolo
- Bannear hosts completamente (no se puede comunicar entre ellos)

Estructura json entonces:
{
    "rules": [
        {
            "src_ip": "
            "dst_ip": "
            "src_port": "
            "dst_port": "
            "protocol": "
            "banned_tuples": []
        }
}

"""

POLICIES = "policies.json"



class Firewall (EventMixin):
    
    def __init__ (self):
        self.firewall_switch_dpid = 1
        self.policies = []
        self.read_policies(POLICIES)
        self.listenTo(core.openflow)

    def read_policies (self, filename):
        with open(filename) as f:
            json_file = json.load(f)
            policies = json_file["policies"]
            for p in policies:
                matches = self.create_match_from(p)
                print(matches)
                for match in matches:
                    self.policies.append(match)
    
        
    def create_match_from(self,policy):  
        matches = []
        match = of.ofp_match()
        match.dl_type = pkt.ethernet.IP_TYPE

        print("policy: ", policy)
        if "banned_tuples" in policy:
            print(policy["banned_tuples"])
            a = IPAddr(policy["banned_tuples"][0])
            b = IPAddr(policy["banned_tuples"][1])

            if "src_ip" in policy or "dst_ip" in policy:
                raise Exception("Cannot ban both src and dst ip while banning a tuple")
            
            matchPair = match.clone()

            matchPair.nw_src = a 
            matchPair.nw_dst = b 

            match.nw_dst = b
            match.nw_src = a

            matches.append(matchPair)

        else:
            if "src_ip" in policy:
                match.nw_src = IPAddr(policy["src_ip"])

            if "dst_ip" in policy:
                match.nw_dst = IPAddr(policy["dst_ip"])

            if "protocol" in policy:
                match.nw_proto = protToNumber[policy["protocol"]]

            if "src_port" in policy:
                # Puse protocolo != UDP/TCP
                # None -> Baneas con TCP y UDP
                if match.nw_proto == None:
                    matchPair = match.clone()
                    matchPair.nw_proto = protToNumber["UDP"]
                    matchPair.tp_src = int(policy["src_port"])
                    matches.append(matchPair)
                    match.nw_proto = protToNumber["TCP"]
                

                elif match.nw_proto != protToNumber["TCP"] and match.nw_proto != protToNumber["UDP"]:
                    print("proto %s", match.nw_proto)
                    raise Exception("Cannot ban TCP/UDP port whilst using non TCP/UDP protocol.") 
                # Puse UDP/TCP -> Baneas solo el que te dijeron
                match.tp_src = int(policy["src_port"])

            if "dst_port" in policy:
                match.tp_dst = int(policy["dst_port"])


        matches.append(match)
        return matches
    
        

    def _handle_ConnectionUp (self, event):
        ''' Add your logic here ... '''
        if self.firewall_switch_dpid != event.dpid:
            return
        
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

        for policy in self.policies:
            print(policy)
            flow_mod = of.ofp_flow_mod(match=policy)
            event.connection.send(flow_mod)
        
        print("Total rules installed: ", len(self.policies))



def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
