import socketio
import time
import threading

# Initialize Socket.IO server
sio = socketio.Client()
connected = False

# Events
@sio.event
def connect():
    global connected 
    connected = True
    print("Connected to the bot!")
    sio.emit('chop')
    print("Initial chop command emitted")
    # Start continuous 'chop' emission in a background thread after connect
    chop_thread = threading.Thread(target=emit_chop_continuously)
    chop_thread.start()
@sio.event
def disconnect():
    connected = False
    print("Disconnected from the bot.")
    attempt_reconnect()

def attempt_reconnect():
    retries = 5
    while retries > 0:
        try:
            sio.connect('http://localhost:3000')  # Reconnect to the server
            print("Reconnected successfully!")
            break
        except Exception as e:
            print(f"Reconnect attempt failed: {e}")
            retries -= 1
            time.sleep(5)  # Wait 5 seconds before trying again

# Function to continuously emit 'chop' command every 3 seconds
def emit_chop_continuously():
    time.sleep(5)  # Delay before starting continuous emission
    while connected:
        sio.emit('chop', {'action': 'chop'})
        print("Emitted chop command")
        time.sleep(5)  # Wait for 3 seconds before the next emission

# Connect to the Socket.IO server running on localhost: 3000
sio.connect('http://localhost:3000')
sio.wait() # Keep client listening for commands


#@sio.event
#def chop(data):
    #print("Emitted chop")
    #sio.emit('chop')  # Emit 'chop' event with provided data

# sio.disconnect()
#sio.wait()