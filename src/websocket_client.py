import asyncio
import websockets
import socket

# socket server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.50.161', 8765))
server.listen(10)

async def hello(uri):
    # wait for socket client
    while True:
        conn, addr = server.accept()
        print("connectd to: ", str(addr))
        try:
            while True:
                receive_message = str(conn.recv(1024), encoding='utf-8')
                sent_message = ""

                async with websockets.connect(uri) as websocket:
                    await websocket.send(receive_message)
                    print(f"card sent to web server: {receive_message}")
                    sent_message = await websocket.recv()
                    # print(f"(client) open? {sent_message}")
                
                conn.sendall(sent_message.encode())
        finally:
            conn.close()

asyncio.get_event_loop().run_until_complete(
    hello('ws://esys-final-server.herokuapp.com/0.0.0.0:80'))
# asyncio.get_event_loop().run_until_complete(
#     hello('ws://127.0.0.1:8000'))
