import socketio
import time

# Initialize Socket.IO server
sio = socketio.Client()

# Events
@sio.event
def connect():
    print("Connected to the bot!")
@sio.event
def disconnect():
    print("Disconnected from the bot.")

# Connect to the Socket.IO server running on localhost: 3000
sio.connect('http://localhost:3000')

# Trigger the chop command
#while True:
    #command = input("Type 'chop' to chop trees (or 'exit' to quit): ")
    #if command.lower() == 'chop':
sio.emit('chop')
    #elif command.lower() == 'exit':
        #break

# sio.disconnect()
sio.wait()