import socket
import threading
import utils

HOST = 'localhost'
PORT = 9990
ID_BYTES = utils.ID_BYTES

class PluginServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(5)
        print(f"Server started at {HOST}:{PORT}")
    
    def handle_client(self, client_socket, address):
        print(f"Connected to {address}")

        try:
            # Read the plugin ID
            plugin_id = int.from_bytes(client_socket.recv(ID_BYTES), byteorder='big', signed=False)
            print(f"Plugin ID received: {plugin_id}")
            
            # Prepare the XML payload for the plugin
            xml_data = "<Transcript><Utterance start='0' end='2'>Hello</Utterance><Utterance start='3' end='5'>World</Utterance></Transcript>"

            # Send data to the plugin
            utils.send_data(client_socket, plugin_id, xml_data)
            print(f"Sent XML data to client {plugin_id}")

            # Receive processed XML from the client
            _, processed_data = utils.recv_all(client_socket)
            print(f"Received processed data: {processed_data}")
            
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()

    def start(self):
        while True:
            client_socket, address = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, address)).start()

if __name__ == "__main__":
    server = PluginServer()
    server.start()