# -*- coding: utf-8 -*-

from flask_script import Manager
from ws.main import app, socketio

manager = Manager(app)
manager.add_command('runws', socketio.run(app, port=5006, debug=True))

if __name__ == '__main__':
    manager.run()