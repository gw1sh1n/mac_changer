#!/usr/bin/env python

import subprocess
import argparse
import re

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="The interface whose MAC you want to change")
    parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC address")
    options = parser.parse_args()

    message = "\n\n[-] Please specify both the interface and new MAC address\n"
    example = "\nExample: python mac_changer.py -i eth0 -m 00:11:22:33:44:55\n"

    if not options.interface:
        parser.error(message + example)
    elif not options.new_mac:
        parser.error(message + example)
    return options


def change_mac(interface, new_mac):
    print("[+} Attempting to change MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"([0-9a-fA-F]{2}:){5}([0-9a-fA-F]){2}", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address")

options = get_arguments()
interface = options.interface
new_mac = options.new_mac

old_mac = get_current_mac(interface)
print("\nCurrent MAC = " + str(old_mac))

change_mac(interface, new_mac)
current_mac = get_current_mac(interface)
success_message = "[+] MAC address was successfully changed to " + str(current_mac) + "\n"
failure_message = "[-] MAC address was not changed.\n"
if current_mac == old_mac:
    print(failure_message)
elif current_mac == options.new_mac:
    print(success_message)
else:
    print(failure_message)


