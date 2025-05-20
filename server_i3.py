#!/usr/bin/env python

from server import JamVendorServer, main
import asyncio
import i3ipc


class JamVendorServer_i3wm(JamVendorServer):
    i3: i3ipc.Connection

    def __init__(self):
        super().__init__()
        self.i3 = i3ipc.Connection()
        self.window_class_to_move = None

    async def check(self):
        await super().check()
        if (
            self.window_class_to_move is not None
            and self.i3.get_tree().find_classed(self.window_class_to_move)
        ):
            print("move!!!!")
            self.i3.command(
                f'[class="{self.window_class_to_move}"] move to workspace Game'
            )
            self.window_class_to_move = None

    async def start_game(self, game):
        self.i3.command("workspace Game")
        await super().start_game(game)
        self.window_class_to_move = self.games[game]["window-class"]


if __name__ == "__main__":
    asyncio.run(main(JamVendorServer_i3wm()))
