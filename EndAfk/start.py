import time
import random
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from .afk import ALL
from EndAfk import app, boot, botname
from EndAfk.helpers import get_readable_time
from EndAfk import SUDOERS
from EndAfk.AlphaDB import is_blocked

alpha = random.choice(ALL)

photo = "https://te.legra.ph/file/6867230d65dd500797f63.jpg"

upl = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="➕ Add me to a Group",
                        url=f"https://t.me/yashualpha_afk_bot?startgroup=true",
                    ),
                ]
            ]
        )

@Client.on_message(filters.command("start") & filters.private)
async def start(_, message: Message):
    blocked = await is_blocked(message.from_user.id)
    if blocked:
        return await message.reply("you've been blocked try: ask @Timeisnotwaiting")
    first_name = message.from_user.first_name
    await message.reply_photo(alpha,
       caption=f"Hey {first_name}! I'm Afk Bot by @YashuAlpha. \n\nTry: replying afk to some media else stickers to make it more reasonable !\n\nFor help - @Timeisnotwaiting", reply_markup=upl)


@Client.on_message(filters.command("ping") & filters.user(SUDOERS))
async def ping(_, message: Message):
    bot_uptime = int(time.time() - boot)
    Uptime = get_readable_time(bot_uptime)
    await _.send_message(
       message.chat.id,
       f"End is alive. \n\n Uptime - {Uptime}")
