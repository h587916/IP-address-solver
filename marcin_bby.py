import ipaddress
import tkinter as tk
from tkinter import scrolledtext

def to_binary(ip):
    return '.'.join(format(int(octet), '08b') for octet in ip.split('.'))

def calculate_network_details(ip_list):
    results = ""
    networks = [ipaddress.ip_network(ip, strict=False) for ip in ip_list]

    for i, network in enumerate(networks):
        try:
            original_ip, subnet = ip_list[i].split('/')
        except ValueError as e:
            results += f"Ugyldig IP-nettverk {ip_list[i]}: {e}\n\n"
            continue

        original_ip_binary = to_binary(original_ip)
        mask_binary = to_binary(str(network.netmask))

        results += f"IP-nettverk: {ip_list[i]}\n"
        results += f"  IP-adresse (binær): {original_ip_binary}\n"
        results += f"  Subnettmaske (binær): {mask_binary}\n"

        # Nettverksadresse
        net_address_binary = to_binary(str(network.network_address))
        results += f"  Nettverksadresse (binær): {net_address_binary}\n"
        results += f"  Nettverksadresse: {network.network_address}\n"

        # Broadcastadresse
        broadcast_address_binary = to_binary(str(network.broadcast_address))
        results += f"  Broadcastadresse (binær): {broadcast_address_binary}\n"
        results += f"  Broadcastadresse: {network.broadcast_address}\n"

        # Antall mulige verter og IP-område
        num_hosts = network.num_addresses - 2
        results += f"  Antall mulige verter: {num_hosts}\n"
        if num_hosts > 0:
            first_host = network.network_address + 1
            last_host = network.broadcast_address - 1
            results += f"  Brukbar vert IP-område: {first_host} til {last_host}\n"
        else:
            results += "  Ingen brukbare verter i dette nettverket.\n"

        # Finne overlappende nettverk
        overlapping_networks = [ip_list[j] for j, other_network in enumerate(networks) if i != j and network.overlaps(other_network)]
        if overlapping_networks:
            results += f"  Adresser i samme nettverk: {', '.join(overlapping_networks)}\n"
        else:
            results += "  Ingen andre IP-adresser i samme nettverk.\n"
        results += "\n"

    return results

def submit_action():
    ip_list = ip_entry.get("1.0", tk.END).strip().split('\n')
    results = calculate_network_details(ip_list)
    result_window = tk.Toplevel(root)
    result_window.title("Resultater")
    result_text = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=80, height=40)
    result_text.insert(tk.INSERT, results)
    result_text.pack()

root = tk.Tk()
root.title("IP Nettverksberegner")

tk.Label(root, text="Skriv inn IP-adresser (én per linje):").pack()
ip_entry = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
ip_entry.pack()

submit_button = tk.Button(root, text="Submit", command=submit_action)
submit_button.pack()

root.mainloop()
