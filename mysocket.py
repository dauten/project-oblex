import asyncio
import datetime
import random
import websockets
import json

USERS = set()

async def con(websocket, path):
    try:
        async for message in websocket:
            print("got a message")
            #for every reply (aka ping)...
            data = json.loads(message)
            if data['action'] == 'ping':
                #forward it to everyone
                print("returning ping")
            if USERS:       # asyncio.wait doesn't accept an empty list
                await asyncio.wait([user.send(message) for user in USERS])
    except Exception as e:
        print("Error reading from socket..\n\n")

async def pro(websocket, path):
    while True:
        try:
            board = json.loads(open("board.json", "r").read())
            large = json.loads(open("large.json", "r").read())

            tokens = [] #a token is a 5 tuple, like ("dwarf", 3, 4, 1, 1) or ("tree", 9, 10, 2, 3)
            for each in board["objects"]:
                tokens.append([each["filename"][:-4], each["row"]-1, each["column"]-1, 1, 1 ])
            for each in large["terrain"]:
                tokens.append([each["filename"][:-4], each["tlx"]-1, each["tly"]-1, each["height"], each["width"] ])
            print("sending message")
            tokens = str(tokens).replace("[", "").replace("]", "")
            await websocket.send(tokens)
        except Exception as e:
            print("Error reading File, continueing...\n\n")

        await asyncio.sleep(.5)


async def time(websocket, path):
    USERS.add(websocket)
    con_task = asyncio.ensure_future(
    con(websocket, path)
    )
    pro_task = asyncio.ensure_future(
    pro(websocket, path)
    )

    done, pending = await asyncio.wait(
    [con_task, pro_task],
    return_when=asyncio.FIRST_COMPLETED
    )
    for task in pending:
        task.cancel()


start_server = websockets.serve(time, '192.168.1.86', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
