from sys import argv
import zmq
import json

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# Loads json file from command argument
with open(argv[1]) as f:
    data = json.load(f)

# Sending json to the server
socket.send_json(data)

#  Get the reply
message = socket.recv()

print(message.decode("utf-8"))