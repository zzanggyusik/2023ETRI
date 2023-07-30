import json
import zmq

with open("./server_config.json") as config_file:
    config = json.load(config_file)
    
keys = list(config["client_config"].keys())
#print(config["client_config"][keys[0]])



context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f'tcp://*:8888')

while True:
    msg = socket.recv_string()
    print(f"Received: {msg}")
    socket.send_string("hihihihihi")
