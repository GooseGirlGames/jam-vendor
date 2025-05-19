#!/usr/bin/env python

import asyncio
import websockets
import subprocess
import os
import signal

lock = asyncio.Lock()


class JamVendorServer:

    def __init__(self):
        self.process = None

    def start(self, cmd):
        self.process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid
        )

    def kill(self):
        if self.process is not None:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)

    async def handler(self, websocket):
        async for message in websocket:
            message = message.strip()
            if message.startswith("launch "):
                game = message.split(" ")[-1]
                print(game)
                self.kill()
                # self.start("cd ~/Games/df && wine Dwarf\\ Fortress.exe")
            if message.startswith("quit"):
                self.kill()

    # TODO somehow run this once every 10 seconds, asynchrounously so as not to
    # block the message handling
    async def check(self):
        time = self.get_idle_time()
        if time > 1000 * 60 * 2:
            self.kill()

    def get_idle_time(self):
        p = subprocess.Popen("xprintidle", stdout=subprocess.PIPE)
        p.wait(0.1)
        if p.stdout:
            return int(p.stdout.read().strip())
        return 0


async def main():
    server = JamVendorServer()
    async with websockets.serve(server.handler, "127.0.0.1", 1312):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
