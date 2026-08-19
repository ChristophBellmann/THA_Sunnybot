import socket

class UDPTransceiver:
    def __init__(self):
        self.udp_ip = "192.168.10.100"
        self.udp_port = 4210
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, data):
        try:
            self.sock.sendto(data.encode('utf-8'), (self.udp_ip, self.udp_port))
            print(f"Data sent: {data}")
        except Exception as e:
            print(f"Failed to send data: {e}")