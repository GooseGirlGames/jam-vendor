#!/usr/bin/env python

import asyncio
import json
import websockets
import subprocess
import os
import signal


class LaunchedApp:
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
        self.process_lock = asyncio.Lock()

    def __del__(self):
        pass

    async def start(self):
        async with self.process_lock:
            print("Starting App.")
            self.process = subprocess.Popen(
                self.cmd,
                shell=True,
                preexec_fn=os.setsid,
            )

    async def kill(self):
        async with self.process_lock:
            if self.process is not None:
                print("Killing App.")
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)


class JamVendorServer:

    app: LaunchedApp | None

    def __init__(self):
        self.app = None
        with open("games.json", "r") as f:
            self.games = json.loads(f.read())
            print(f"Found {len(self.games.keys())} games!")

    def get_cmd(self, game_name):
        if game_name not in self.games.keys():
            return None
        game = self.games[game_name]
        return f"cd {game['launch-dir']} && {game['launch-command']}"

    async def start_game(self, game):
        cmd = self.get_cmd(game)
        if cmd:
            self.app = LaunchedApp(cmd)
            await self.app.start()
        else:
            print(f"Can't find '{game}' :(")

    async def kill_game(self):
        if self.app:
            await self.app.kill()
            self.app = None

    async def on_closed(self):
        print("Game was closed")

    async def handler(self, websocket):
        async for message in websocket:
            message = message.strip()
            if message.startswith("launch "):
                game = message.split(" ")[-1]
                print(game)
                if self.app:
                    await self.kill_game()
                await self.start_game(game)
            if message.startswith("quit") and self.app:
                await self.kill_game()

    async def check_loop(self):
        while True:
            await self.check()
            await asyncio.sleep(1)

    async def check(self):
        if self.app:
            idle_time_ms = self.get_idle_time()
            print(f"Running check.  Time is {idle_time_ms / 1000} seconds")
            if idle_time_ms > 1000 * 10:
                await self.app.kill()

    def get_idle_time(self):
        p = subprocess.Popen("xprintidle", stdout=subprocess.PIPE)
        p.wait(0.1)
        if p.stdout:
            return int(p.stdout.read().strip())
        return 0


async def main(server):
    asyncio.create_task(server.check_loop())
    async with websockets.serve(server.handler, "127.0.0.1", 1312):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main(JamVendorServer()))
