#!/usr/bin/env python3

import shutil

def hash_(_str):
    return hashlib.md5(_str.encode()).hexdigest()
