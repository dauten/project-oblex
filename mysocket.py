import asyncio
import datetime
import random
import websockets
import json

USERS = set()


async def time(websocket, path):
    USERS.add(websocket)
    while True:
        try:
            board = json.loads(open("board.json", "r").read())
            large = json.loads(open("large.json", "r").read())

            tokens = [] #a token is a 5 tuple, like ("dwarf", 3, 4, 1, 1) or ("tree", 9, 10, 2, 3)
            for each in board["objects"]:
                tokens.append([each["filename"][:-4], each["row"]-1, each["column"]-1, 1, 1 ])
            for each in large["terrain"]:
                tokens.append([each["filename"][:-4], each["tlx"]-1, each["tlx"]-1, each["height"], each["width"] ])

            tokens = str(tokens).replace("[", "").replace("]", "")
            await websocket.send(tokens)
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
            print("Error reading File, continueing...\n\n")

        await asyncio.sleep(.5)

start_server = websockets.serve(time, 'auten.space', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
