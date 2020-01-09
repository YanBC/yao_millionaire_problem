import asyncio
import websockets
import signal
import functools
import os
import argparse
from ast import literal_eval

from millionaires import Millionaire


def ask_exit(signame):
    global loop
    print("got signal %s: exit" % signame)
    loop.stop()


async def challenge(websocket, path):
    if path == '/':
        global srv_millionaire

        # receive peer public key
        peer_pubKey = await websocket.recv()

        # generate ciphertext
        ciphertext = srv_millionaire.get_ciphertext(peer_pubKey)
        await websocket.send(str(ciphertext))

        # get peer generated prime and batch_z
        prime_and_batch_z_str = await websocket.recv()
        p, batch_z = literal_eval(prime_and_batch_z_str)

        # check if peer is richer
        if srv_millionaire.peer_is_richer(p, batch_z):
            result = 'You are richer than me'
        else:
            result = 'I am richer than you'
        await websocket.send(result)
        
    else:
        error_msg = 'Illegel path'
        await websocket.send((error_msg))


def option_parser():
    p = argparse.ArgumentParser()
    p.add_argument('millions', type=int, help='number of millions you own')
    p.add_argument('--ip', default='', help='ip address; Default to wild card address')
    p.add_argument('--port', default=16233, type=int, help='port number; Default to 16233')
    return p.parse_args()


if __name__ == '__main__':
    opts = option_parser()
    srv_millionaire = Millionaire(opts.millions)

    start_server = websockets.serve(challenge, opts.ip, opts.port)

    loop = asyncio.get_event_loop()
    for signame in ('SIGINT', 'SIGTERM', 'SIGTSTP'):
        loop.add_signal_handler(getattr(signal, signame), functools.partial(ask_exit, signame))

    print(f"Server is running at port {opts.port}, press Ctrl+C to interrupt.")
    # print("pid %s: send SIGINT or SIGTERM or SIGTSTP to exit." % os.getpid())
    try:
        loop.run_until_complete(start_server)
        loop.run_forever()
    finally:
        loop.close()