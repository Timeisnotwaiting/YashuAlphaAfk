from EndAfk import SUDOERS
from EndAfk.AlphaDB import *
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command(["block", "unblock"]) & ~filters.edited & ~filters.forwarded)
async def bloblo(_, m: Message):
    if m.from_user.id not in SUDOERS:
        return
    replied = m.reply_to_message
    text = m.text.split(None, 1)[1]
    if replied and len(m.command) == 1:
        try:
            a = replied.from_user.id
        except:
            await m.reply("either anonymous or channel, are already blocked")
        a_fn = replied.from_user.first_name
        reason = "Might be misused"
    elif replied and len(m.command) > 1:
        a = replied.from_user.id
        a_fn = replied.from_user.first_name
        reason = text
    elif len(m.command) >= 2:
        if str(text)[0] == "@":
            try:
                a = (await _.get_users(text)).id
            except:
                await m.reply("/block or /unblock [username]")

        
