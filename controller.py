import socketio
import asyncio

# Initialize Socket.IO client
sio = socketio.AsyncClient()
connected = False
reconnect_attempts = 0
max_reconnect_attempts = 5
reconnect_delay = 5  # Seconds

# Events
@sio.event
async def connect():
    global connected 
    connected = True
    print("Connected to the bot!")
    await sio.emit('chop')
    print("Initial chop command emitted")
    # Start continuous 'chop' emission
    asyncio.create_task(emit_chop_continuously())

@sio.event
async def disconnect():
    global connected, reconnect_attempts
    connected = False
    print("Disconnected from the bot.")
    reconnect_attempts += 1
    if reconnect_attempts <= max_reconnect_attempts:
        print(f"Attempting to reconnect... (Attempt {reconnect_attempts}/{max_reconnect_attempts})")
        await reconnect()
    else:
        print(f"Maximum reconnect attempts ({max_reconnect_attempts}) reached. Exiting.")
        await sio.disconnect()

# Async reconnection function
async def reconnect():
    global connected
    await asyncio.sleep(reconnect_delay)
    try:
        await sio.connect('http://localhost:3000')  # Replace with your server's address
        print("Reconnected to the bot!")
    except Exception as e:
        print(f"Reconnect attempt failed: {e}")

# Function to continuously emit 'chop' command every 9 seconds
async def emit_chop_continuously():
    await asyncio.sleep(5)  # Initial delay before starting continuous emission
    while connected:
        await sio.emit('chop')
        print("Emitted chop command")
        await sio.sleep(9)  # Wait for 9 seconds before the next emission

# Main function to connect the client
async def main():
    try:
        await sio.connect('http://localhost:3000')
        await sio.wait()  # Keep client listening for commands
    except Exception as e:
        print(f"Failed to connect: {e}")
        await reconnect()

# Run the main function
asyncio.run(main())
