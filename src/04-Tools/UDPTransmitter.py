import socket
import argparse
import threading

def send_udp_packet(message, server_address):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Send data
        print(f"Sending: {message}")
        sock.sendto(message.encode(), server_address)
        
        # Receive response
        print("Waiting for response...")
        data, server = sock.recvfrom(4096)
        print(f"Received: {data.decode()}")
    finally:
        print("Closing sending socket")
        sock.close()

def receive_messages(sock):
    while True:
        data, server = sock.recvfrom(4096)
        print(f"Received: {data.decode()}")

def main():
    parser = argparse.ArgumentParser(description='Send a UDP packet to the server.')
    parser.add_argument('args', nargs='*', help='Velocity and alpha values followed by an optional debug flag')

    args = parser.parse_args().args
    
    server_address = ('192.168.10.100', 4210)
    
    debug_mode = False
    velocity = None
    alpha = None
    
    if len(args) == 1 and args[0] == 'debug':
        debug_mode = True
    elif len(args) == 2:
        velocity = float(args[0])
        alpha = int(args[1])
    elif len(args) == 3 and args[2] == 'debug':
        velocity = float(args[0])
        alpha = int(args[1])
        debug_mode = True
    else:
        print("Enter velocity and alpha to send:")
        try:
            while True:
                velocity = float(input("Velocity (float): "))
                alpha = int(input("Alpha (int): "))
                message = f"V={velocity} Alpha={alpha}"
                send_udp_packet(message, server_address)
        except KeyboardInterrupt:
            print("\nProgram terminated.")
        return

    if debug_mode:
        # Create a UDP socket for receiving messages
        receive_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receive_sock.bind(('0.0.0.0', 4096))

        # Start a thread to receive messages
        receive_thread = threading.Thread(target=receive_messages, args=(receive_sock,))
        receive_thread.daemon = True
        receive_thread.start()

        send_udp_packet("debug", server_address)
    
    if velocity is not None and alpha is not None:
        message = f"V={velocity} Alpha={alpha}"
        send_udp_packet(message, server_address)

    if debug_mode or (velocity is None or alpha is None):
        print("Enter velocity and alpha to send:")
        
        try:
            while True:
                velocity = float(input("Velocity (float): "))
                alpha = int(input("Alpha (int): "))
                message = f"V={velocity} Alpha={alpha}"
                send_udp_packet(message, server_address)
        except KeyboardInterrupt:
            print("\nProgram terminated.")

if __name__ == "__main__":
    main()
