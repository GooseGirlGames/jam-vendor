#!/usr/bin/env python

from server import JamVendorServer, main
import asyncio
import i3ipc


class JamVendorServer_i3wm(JamVendorServer):
    i3: i3ipc.Connection
    visual_active = False

    def __init__(self):
        super().__init__()
        self.i3 = i3ipc.Connection()
        self.window_class_to_move = None
        asyncio.run(self.start_visual())

    async def start_visual(self):
        self.visual_active = True
        await self.start("glxgears")
        self.window_class_to_move = "glxgears"

    async def check(self):
        await super().check()
        if (
            self.window_class_to_move is not None
            and self.i3.get_tree().find_titled(self.window_class_to_move)
        ):
            print("move!!!!")
            self.i3.command(
                f'[title="{self.window_class_to_move}"] move to workspace Game'
            )
            if self.visual_active:
                selector = f'[title="{self.window_class_to_move}"]'
                self.i3.command(f"{selector} floating enable")
                self.i3.command(f"{selector} move position 0 0")
            self.window_class_to_move = None

    async def kill(self):
        await super().kill()
        if not self.visual_active:
            await self.start_visual()

    async def start_game(self, game):
        self.i3.command("workspace Game")
        await super().start_game(game)
        self.visual_active = False
        self.window_class_to_move = self.games[game]["window-class"]


if __name__ == "__main__":
    asyncio.run(main(JamVendorServer_i3wm()))
