# Copyright (c) 2016, Matt Layman

from handroll.commands.build import BuildCommand
from handroll.commands.watch import WatchCommand

COMMANDS = [
    BuildCommand(),
    WatchCommand(),
]
