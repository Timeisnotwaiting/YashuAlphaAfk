from pyrogram import Client, filters
from pyrogram.types import Message
ALPHA = [1985209910]

@Client.on_message(filters.command("info") & filters.user(ALPHA))
async def info(_, m):
    if len(m.command) == 2:
        lel = int(m.text.split(None, 1)[1])
        if str(lel)[0] == "-":
            id = lel
        else:
            omfoo = "-" + str(lel)
            id = int(omfoo)

    getter = await _.get_chat(id)
    try:
        username = getter.username
    except:
        username = "None"
    try:
        link = getter.invite_link
    except:
        link = "None"
    await m.reply(f"Group name :- {getter.title}\n\nInvite link :- {link}\n\nUsername :- @{username}")
