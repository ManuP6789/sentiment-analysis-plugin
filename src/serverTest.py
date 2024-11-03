import socket
import threading
import utils
import sys

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
            sys.stdout.flush()
            
            # Prepare the XML payload for the plugin
            # xml_data = '<transcript> <u speaker="0"><w start="0.419" end="0.579">Alright,</w><w start="0.759" end="1.039">so</w><w start="1.36" end="1.56">hows</w><w start="1.6" end="1.92">everything</w><w start="1.96" end="2.34">going?</w></u> </transcript>'
            # xml_data = '<transcript>'
            xml_data = '''
                <transcript>
                    <u speaker="1">
                        <w start="0.5" end="0.8">Hello,</w>
                        <w start="0.9" end="1.2">how</w>
                        <w start="1.3" end="1.5">are</w>
                        <w start="1.6" end="1.8">you?</w>
                    </u>
                    <u speaker="2">
                        <w start="2.0" end="2.3">I'm</w>
                        <w start="2.4" end="2.6">doing</w>
                        <w start="2.7" end="3.0">well,</w>
                        <w start="3.1" end="3.3">thanks!</w>
                    </u>
                </transcript>
            '''
            # Send data to the plugin
            utils.send_data(client_socket, plugin_id, xml_data)
            print(f"Sent XML data to client {plugin_id}")
            sys.stdout.flush()

            # Receive processed XML from the client
            _, processed_data = utils.recv_all(client_socket)
            print(f"Received processed data: {processed_data}")
            sys.stdout.flush()
            
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
