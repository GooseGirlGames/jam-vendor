#!/usr/bin/env python

import asyncio
import websockets
import subprocess
import os
import signal

lock = asyncio.Lock()

process = None


def start(cmd):
    return subprocess.Popen(
        cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid
    )


def kill(pro):
    if pro is not None:
        os.killpg(os.getpgid(pro.pid), signal.SIGTERM)


async def handler(websocket):
    global process
    async for message in websocket:
        message = message.strip()
        if message.startswith("launch "):
            game = message.split(" ")[-1]
            kill(process)
            process = start("cd ~/Games/df && wine Dwarf\\ Fortress.exe")
        if message.startswith("quit"):
            kill(process)


async def main():
    async with websockets.serve(handler, "127.0.0.1", 1312):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
