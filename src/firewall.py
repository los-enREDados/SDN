'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

IPDELSWITCHCONELFIREWALL = 3

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
        self.firewall_switch_dpid = IPDELSWITCHCONELFIREWALL
        self.policies = []
        self.read_policies(POLICIES)
        self.listenTo(core.openflow)

    def read_policies (self, filename):
        with open(filename) as f:
            json_file = json.load(f)
            policies = json_file["policies"]
            matches = []
            for p in policies:
                matches = self.create_match_from(p)
                for match in matches:
                    self.policies.append(match)
    
        
    def create_match_from(self,policy):  
        doneProcessingMatches = []
        toBeProcessedMatches  = []

        match = of.ofp_match()
        
        match.dl_type = pkt.ethernet.IP_TYPE
        

        if "banned_tuples" in policy:
            a = IPAddr(policy["banned_tuples"][0])
            b = IPAddr(policy["banned_tuples"][1])

            if "src_ip" in policy or "dst_ip" in policy:
                raise Exception("Cannot ban both src and dst ip while banning a tuple")
            
            matchPair = match.clone()

            matchPair.nw_src = a 
            matchPair.nw_dst = b 

            match.nw_src = b
            match.nw_dst = a

            toBeProcessedMatches.append(matchPair)

        toBeProcessedMatches.append(match)

        i = 0
        while True:
            if i + 1 > len(toBeProcessedMatches):
                break

            currentMatch = toBeProcessedMatches[i].clone()
            i = i + 1

            if currentMatch.nw_src == None and "src_ip" in policy:
                currentMatch.nw_src = IPAddr(policy["src_ip"])

            if currentMatch.nw_dst == None and "dst_ip" in policy:
                currentMatch.nw_dst = IPAddr(policy["dst_ip"])

            if currentMatch.nw_proto == None and "protocol" in policy:
                currentMatch.nw_proto = protToNumber[policy["protocol"]]

            if currentMatch.tp_src == None and "src_port" in policy:
                # Puse protocolo != UDP/TCP
                # None -> Baneas con TCP y UDP
                if currentMatch.nw_proto == None:
                    currentMatch, twinMatch = self.unespecified_protocol(policy, currentMatch, is_src = True)
                    toBeProcessedMatches.append(twinMatch)
                    
                elif currentMatch.nw_proto != protToNumber["TCP"] and currentMatch.nw_proto != protToNumber["UDP"]:
                    raise Exception("Cannot ban TCP/UDP port whilst using non TCP/UDP protocol.") 
                # Puse UDP/TCP -> Baneas solo el que te dijeron
                currentMatch.tp_src = int(policy["src_port"])

            if currentMatch.tp_dst == None and "dst_port" in policy:
                if currentMatch.nw_proto == None:
                    currentMatch, twinMatch = self.unespecified_protocol(policy, currentMatch, is_src = False)
                    toBeProcessedMatches.append(twinMatch)
                
                elif currentMatch.nw_proto != protToNumber["TCP"] and currentMatch.nw_proto != protToNumber["UDP"]:
                    raise Exception("Cannot ban TCP/UDP port whilst using non TCP/UDP protocol.")
                currentMatch.tp_dst = int(policy["dst_port"])
                
            doneProcessingMatches.append(currentMatch)


        return doneProcessingMatches
        
    def unespecified_protocol(self, policy, match, is_src = True):
        matchPair = match.clone()
        matchPair.nw_proto = protToNumber["UDP"]
        if is_src:
            matchPair.tp_src = int(policy["src_port"])
        else:
            matchPair.tp_dst = int(policy["dst_port"])
        # matches.append(matchPair)
        match.nw_proto = protToNumber["TCP"]
        return match, matchPair
        
    def _handle_ConnectionUp(self, event):
        ''' Add your logic here ... '''
        if self.firewall_switch_dpid != event.dpid:
            return
        
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

        # High priority rules to drop packets based on policies
        for policy in self.policies:
            log.debug("Installing policy: %s", policy)
            flow_mod = of.ofp_flow_mod(match=policy)
            # No action means drop the packet
            event.connection.send(flow_mod)


    def _handle_PacketIn(self, event):
        if self.firewall_switch_dpid != event.dpid:
            return
        eth = event.parsed # MAC
        if eth.type != pkt.ethernet.IP_TYPE:
            return
        for policy in self.policies:
            if self.match_policy(policy, eth):
                log.debug("Packet from %s -> %s dropped with policy: %s",eth.next.srcip,eth.next.dstip,policy)
                return


    def match_policy(self, match, eth):
        ip = eth.next
        if ip:
            if match.nw_src:
                if match.nw_src != ip.srcip:
                    return False
            if match.nw_dst:
                if match.nw_dst != ip.dstip:
                    return False
            transport = ip.next
            if transport:
                if match.nw_proto:
                    if match.nw_proto != ip.protocol:
                        return False
                if match.tp_src:
                    if match.tp_src != transport.srcport:
                        return False
                if match.tp_dst:
                    if match.tp_dst != transport.dstport:
                        return False
        return True
            

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
