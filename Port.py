import socket
import time
from datetime import datetime
from tqdm import tqdm

Green = '\033[92m'
Red = '\033[91m'
Reset = '\033[0m'

def is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
        return True
    except socket.error:
        return False

def local_port_scanner(start_port=1, end_port=1024, host='127.0.0.1', ipv6=False): # 0/65535
    open_ports = []
    total_ports = end_port - start_port + 1
    start_time = time.time()
    
    print(f"Starting scan on {host} from port {start_port} to {end_port}...")
    print(f"Scan started at: {datetime.now().strftime('%H:%M:%S')}\n")
    
    socket_family = socket.AF_INET6 if ipv6 else socket.AF_INET

    with tqdm(total=total_ports, desc="Progress", unit="port", bar_format='{l_bar}{bar}| Scanning port {n_fmt}/{total_fmt}') as pbar:
        for port in range(start_port, end_port + 1):
            sock = socket.socket(socket_family, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
                print(f"\rPort {port}: {Red}OPEN{Reset}", end='')
            sock.close()
            pbar.update(1)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print("\n\nScan completed.")
    print(f"Total time taken: {int(elapsed_time // 3600)}:{int((elapsed_time % 3600) // 60)}:{int(elapsed_time % 60)}")
    
    if open_ports:
        print("Open ports found:")
        for port in open_ports:
            print(f"- Port {port}")
    else:
        print("There are 0 open ports found.")
    
    input("\nPress Enter to exit.")

while True:
    target_host = input("Enter 'localhost' to scan localhost or enter an IP address to scan: ")
    if target_host.lower() == 'localhost':
        local_port_scanner()
        break
    else:
        use_ipv6 = input("Use IPv6? (yes/no): ").strip().lower()
        if use_ipv6 == 'yes' and not is_valid_ipv6_address(target_host):
            print(f"{Red}The IP address you entered isn't a valid IPv6 address.{Reset}")
            continue
        elif use_ipv6 == 'no' and is_valid_ipv6_address(target_host):
            print(f"{Red}The IP address you entered is a IPv6 address. Please choose yes.{Reset}")
            continue
        local_port_scanner(host=target_host, ipv6=(use_ipv6 == 'yes'))
        break
