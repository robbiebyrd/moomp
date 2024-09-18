from lupa.lua54 import LuaRuntime

from models.character import Character
from utils.db import connect_db

connect_db()


def script():
    lua = LuaRuntime()
    char = Character.objects(name='Wizard').first()
    func = lua.eval('''
    function(o)
        o.name="CRAZY"
        return o
    end
    ''')
    print(func(char.to_mongo()))
