# -*- coding: utf-8 -*-
import os
import json
import random
import logger
from logger import storage


_roles = logger.roles


def ver_roles():
    if os.path.exists(_roles):
        with open(_roles) as f:
            role = json.loads(f.read())
            f.close()
            storage.roles = role
    return storage.roles


def commit_roles():
    if os.path.exists(_roles):
        with open(_roles, 'w') as f:
            f.write(json.dumps(storage.roles, indent=4))
            f.close()
