#!/usr/bin/env python

from server import JamVendorServer, main, LaunchedApp
import asyncio
import i3ipc


class JamVendorServer_i3wm(JamVendorServer):
    i3: i3ipc.Connection
    visual: LaunchedApp | None
    info: LaunchedApp | None

    def __init__(self):
        super().__init__()
        self.i3 = i3ipc.Connection()
        self.window_class_to_move = None
        asyncio.run(self.start_visual())

    async def start_visual(self):
        self.visual = LaunchedApp("glxgears")
        await self.visual.start()
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
            if self.visual:
                selector = f'[title="{self.window_class_to_move}"]'
                self.i3.command(f"{selector} floating enable")
                self.i3.command(f"{selector} move position 0 0")
            self.window_class_to_move = None
        if not self.visual and self.app and self.app.process:
            print("meow")
            try:
                if self.app.process.poll() is not None:
                    await self.kill_game()
                    await self.start_visual()
            except ProcessLookupError:
                if self.info:
                    await self.info.kill()
                await self.start_visual()

    async def kill_game(self):
        await super().kill_game()
        if self.info:
            await self.info.kill()
        if not self.visual:
            await self.start_visual()

    async def start_game(self, game):
        self.i3.command("workspace Game")
        await super().start_game(game)
        self.visual = None
        self.window_class_to_move = self.games[game]["window-class"]
        self.info = LaunchedApp("firefox https://example.com/")
        await self.info.start()


if __name__ == "__main__":
    asyncio.run(main(JamVendorServer_i3wm()))
