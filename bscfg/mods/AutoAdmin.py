import bs
import logger
import json
import handleRol
from logger import storage

stats = logger.pStats
# Gives Admin To Rank 1


def admin(val):
    fi = open(stats, 'r')
    pats = json.loads(fi.read())
    for pb_id in pats:
        rank_check = pats[pb_id]["rank"]
        if int(rank_check) == int(val):
            key1 = list(pats.keys())
            for i in key1:
                if pats[i]["rank"] == val:
                    storage.roles['admins'].append(i)
    handleRol.commit_roles()

    bs.screenMessage("Admins Updated", color=(0, 1, 0))

# Gives Vip To Rank 2


def vip(val):
    fi = open(stats, 'r')
    pats = json.loads(fi.read())
    for pb_id in pats:
        rank_check = pats[pb_id]["rank"]
        if int(rank_check) == int(val):
            key1 = list(pats.keys())
            for i in key1:
                if pats[i]["rank"] == val:
                    storage.roles['vips'].append(i)

    handleRol.commit_roles()
    bs.screenMessage("Vips Updated", color=(0, 1, 0))
