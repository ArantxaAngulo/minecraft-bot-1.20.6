import socketio
import time

# Initialize Socket.IO server
sio = socketio.Client()

# Events
@sio.event
def connect():
    print("Connected to the bot!")
    sio.emit('chop')
@sio.event
def disconnect():
    print("Disconnected from the bot.")

# Connect to the Socket.IO server running on localhost: 3000
sio.connect('http://localhost:3000')
sio.wait() # Keep client listening for commands

# Trigger the chop command
#while True:
    #command = input("Type 'chop' to chop trees (or 'exit' to quit): ")
    #if command.lower() == 'chop':
# sio.emit('chop')
    #elif command.lower() == 'exit':
        #break
@sio.event
def chop(data):
    print("Emitted chop")
    sio.emit('chop')  # Emit 'chop' event with provided data


# sio.disconnect()
sio.wait()