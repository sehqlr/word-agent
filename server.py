#!/usr/bin/env python3
from app import app

import cherrypy

if __name__ == '__main__':

    # Mount the application
    cherrypy.tree.graft(app, "/")

    # Unsubscribe the default server
    cherrypy.server.unsubscribe()

    # Instantiate a new server object
    server = cherrypy._cpserver.Server()

    # Configure the server object
    server.socket_host = "0.0.0.0"
    server.socket_port = 8880
    server.thread_pool = 30

    server.subscribe()

    # Start the server engine (Option 1 & 2)
    cherrypy.engine.start()
    cherrypy.engine.block()
