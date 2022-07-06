from EndAfk import db

blockdb = db.blocked

async def block(a: int):
    is_blocked = await blockdb.find_one({"a": a})
    if is_blocked:
        return
    await blockdb.insert_one({"a": a})

async def unblock(a: int):
    is_blocked = await blockdb.find_one({"a": a})
    if not is_blocked:
        return
    await blockdb.delete_one({"a": a})

async def is_blocked(a: int): 
    is_blocked = await blockdb.find_one({"a": a})
    if is_blocked:
        return True
    else:
        return False

async def list_blocked():
    _list = await blockdb.find({"a": {"$gt": 0}})
    try:
        return _list
    except:
        return []
