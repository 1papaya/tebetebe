#!/usr/bin/env python3

import shutil
import socket
import hashlib

def hash_(_str):
    return hashlib.md5(_str.encode()).hexdigest()

def find_open_port():
    # Thanks to this gist! https://gist.github.com/jdavis/4040223

    sock = socket.socket()
    sock.bind(('', 0))

    _, port = sock.getsockname()

    return port
