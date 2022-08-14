from pyrogram import Client, filters
from pyrogram.types import Message
from EndAfk.AlphaDB.blocked import is_blocked

@Client.on_message(filters.command("report"))
async def report(_, m):
    if await is_blocked(m.from_user.id):
        return
    if len(m.command) <= 1:
        return await m.reply("<code>/report < query> </code>")
    query = m.text.split(None, 1)[1]
    try:
        await _.send_message(1985209910, query)
        await m.reply("reported to @Timeisnotwaiting...\n\nTo know more ... Can DM them..")
    except:
        await m.reply("report failed")
