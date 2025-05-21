#!usr/bin/python3

import socket
import threading
import time
import pyfiglet
    
print(pyfiglet.figlet_format("PORT SCANNER"))

open_ports = []
lock = threading.Lock()

def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown"

def scan_port(target, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        if result == 0:
            service = get_service_name(port)
            with lock:
                open_ports.append((port, service))


def scan_ports(target, start_port, end_port):
    threads = []
    print(f"\nScanning target: {target} ({socket.gethostbyname(target)})")
    print("-" * 50)

    start_time = time.time()

    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target, port))
        t.start()
        threads.append(t)

#join threads that run 

    for t in threads:
        t.join()

#for time 
    end_time = time.time()
    total_time = end_time - start_time

#print open port 
    if open_ports:
        open_ports.sort()
        print("{:<8} {:<15} {:<10}".format("Port", "Service", "Status"))
        print("-" * 50)
        for port, service in open_ports:
            print("{:<8} {:<15} {:<10}".format(port, service, "Open"))
    else:
        print("No open ports found in the specified range.")

    print("-" * 50)
    print("Scan completed in {:.3f} seconds".format(total_time))

#main function

if __name__ == "__main__":

    target = input("Enter IP address or domain: ").strip()

    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("Invalid domain or IP.")
        exit()

    try:
        start_port = int(input("Enter start port: "))
        end_port = int(input("Enter end port: "))

        if start_port < 0 or end_port > 65535 or start_port > end_port:
            raise ValueError

        scan_ports(ip, start_port, end_port)

    except ValueError:
        print("Please enter a valid port range (0–65535).")
