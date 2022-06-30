import zmq
import gevent
from gevent import subprocess
import json


# Connecting to port
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()

    #  Decode and jsonify message
    message = json.loads(message.decode("utf-8"))

    try:
        if message["command_type"] == "os":
            # Starting to do command
            p1 = subprocess.Popen([message["command_name"]] + message["parameters"], stdout=subprocess.PIPE)
            
            # Waiting to finish the process
            gevent.wait([p1], timeout=2)
            
            # Getting the result of command
            result = p1.stdout.read()

            # See if process done or not
            if p1.poll() is not None:
                print(f'uname: {result}')
            else:
                print('uname: job is still running')
            
            # Close the command operation
            p1.stdout.close()
            
            # Send the result to client
            socket.send_json({"given_os_command":message["command_name"] + ' ' + ' '.join(message["parameters"]),"result":result.decode("utf-8")})

        elif message["command_type"] == "compute":

            # Function for compute and sending result to client
            def do_thing(compute):
                print(eval(compute))
                socket.send_json({"given_math_expression": compute,"result": eval(compute)})
                
        
            # Add function to queue of gevent library
            gevent.joinall([gevent.spawn(do_thing, message["expression"])])

    # Cofigure exeption for sending errors to client
    except Exception as e:
        
        socket.send_string(str(e))
