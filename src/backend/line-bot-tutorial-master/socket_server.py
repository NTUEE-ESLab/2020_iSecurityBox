########################################
#               SOCKET                 #
########################################
import sys
import socket
import ipaddress
import argparse

def start_server(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((ip, port))
        print(f"Start a socket server at {ip}. Port {port}...")
    except socket.error as e:
        raise e
    
    while True:
        print('Listening to any client...')
        server.listen(0)
        client, address = server.accept()
        while True:
            print(str(address) + " connected")
            try:
                while True:
                    client.send(b"Welcome to my server = =...")
                    card_id = client.recv(8).decode('utf-8')
                    print(card_id)
            except:
                break
            
        client.close()


def read_args():
    parser = argparse.ArgumentParser(description='Wlecome to Linebot socket server.')
    parser.add_argument("ip", type=str, help="Enter the ip address of your host.")
    parser.add_argument("-P", "--port", type=int, default=8888, help="Port to be used.")
    ip_addr = parser.parse_args().ip
    port = parser.parse_args().port

    if not ip_addr or not isinstance(ip_addr, str):
        raise ValueError("Expected ip address <str>!")
    
    try:
        ipaddress.ip_address(ip_addr)
    except ValueError:
        print("Invalid ip address!")
        exit()
    
    return ip_addr, port

if __name__ == '__main__':
    host, port = read_args()
    start_server(host, port)

