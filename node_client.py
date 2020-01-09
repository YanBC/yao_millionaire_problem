import asyncio
import websockets
import argparse

from millionaires import Millionaire

async def compare(url):
    async with websockets.connect(url) as websocket:
        name = input("what's your name?\n")

        owned = input(f"Hello {name}, how many millions are your worth?\n")
        owned = int(owned)

        me = Millionaire(owned)

        # send pubkey
        await websocket.send(me.get_pub_key_pem())

        # receive ciphertext
        ciphertext_str = await websocket.recv()
        ciphertext = int(ciphertext_str)

        # send prime and batch_z
        p_and_batch_z = me.get_batch_z(ciphertext)
        await websocket.send(str(p_and_batch_z))

        # receive result
        result = await websocket.recv()
        print(f"{name}, {result}")



def option_parser():
    p = argparse.ArgumentParser()
    p.add_argument('url', help='peer url')
    return p.parse_args()


if __name__ == '__main__':
    opts = option_parser()

    asyncio.get_event_loop().run_until_complete(compare(opts.url))