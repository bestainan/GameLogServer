#-*- coding: utf8 -*-
from rklib.core import app

def generate():
    engine = app.get_storage_engine("mysql")
    lastrowid = engine.master_execute("UPDATE sequence SET id=LAST_INSERT_ID(id+1)")
    return str(int(lastrowid))

def get_count():
    engine = app.get_storage_engine("mysql")
    lastrowid = engine.master_get("SELECT * FROM sequence")
    return str(int(lastrowid['id']))

def reset():
    engine = app.get_storage_engine("mysql")
    lastrowid = engine.master_execute("UPDATE sequence SET id=1000000000")
    return str(int(lastrowid))