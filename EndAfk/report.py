from pyrogram import Client, filters
from pyrogram.types import Message
from EndAfk.AlphaDB.blocked import is_blocked
from config import OWNER

@Client.on_message(filters.command("report"))
async def report(_, m):
    if not m.from_user:
        return
    if await is_blocked(m.from_user.id):
        return
    if len(m.command) <= 1:
        return await m.reply("<code>/report < QUERY > </code>")
    query = m.text.split(None, 1)[1]
    q = f"#REPORT\n\n@{m.from_user.username if m.from_user.username else None} ({m.from_user.id})\n\n{query}"
    try:
        await _.send_message({OWNER}, q)
        await m.reply("reported to @{OWNER}\n\nTo know more... Can DM them !..")
    except:
        await m.reply("report failed...\n\nDM @{OWNER}")
