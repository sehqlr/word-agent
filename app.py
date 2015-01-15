#!/usr/bin/env python3
import sys

from modules.backend import Segment, r_server

if __name__ == "__main__":
    if sys.argv[1] == "gtk":
        from modules.gtk import Controller
        app = Controller()
    else:
        from modules.web import app

    app.run()
