import time
import random
from pyrogram import filters, Client
from pyrogram.types import Message

from EndAfk import app, botname
from EndAfk.AlphaDB import add_afk, is_afk, remove_afk
from EndAfk.helpers import get_readable_time
from EndAfk.AlphaDB import is_blocked

ALL = ["https://te.legra.ph/file/742022ffd79d376351e6a.jpg",
       "https://te.legra.ph/file/f041db01b67b7f63dabac.jpg",
       "https://te.legra.ph/file/6ac89607d1ae49f2925d5.jpg",
       "https://te.legra.ph/file/7d447f788ab041b09e4df.jpg",
       "https://te.legra.ph/file/a852fa05ee2028140bfaa.jpg",
       "https://te.legra.ph/file/8fae53963345e2717d584.jpg",
       "https://te.legra.ph/file/48c697e01be32f1be52b6.jpg",
       "https://te.legra.ph/file/97b649726692afe356e7d.jpg",
       "https://te.legra.ph/file/3209c0c839b9645ce76a1.jpg",
       "https://te.legra.ph/file/12e26c7790ad8cb3eddb9.jpg",
       "https://te.legra.ph/file/9d0d7e44b308799ceeeef.jpg",
       "https://te.legra.ph/file/3edd1d0e149fabaaaaed1.jpg",
       "https://te.legra.ph/file/ffa92bc1c46be1474b98a.jpg",
       "https://te.legra.ph/file/f68fb4388f863a9327b36.jpg",
       "https://te.legra.ph/file/3458f5af883d4374e936d.jpg",
       "https://te.legra.ph/file/7b158da804ed25cf0443e.jpg",
       "https://te.legra.ph/file/2bcd5e231bbb7a7b560d4.jpg",
       ]

JAI_HIND = ["https://te.legra.ph/file/b1acd8c8330cc0a7872e3.jpg",
            "https://te.legra.ph/file/0670cee472e6c47b021f9.jpg",
            "https://te.legra.ph/file/08cb5b62e96c7a5942301.jpg",
            "https://te.legra.ph/file/26f7b3959efe9c77dbf8b.jpg",
            "https://te.legra.ph/file/e3a602f78109b4c537cd5.jpg",
            "https://te.legra.ph/file/cd460e3c655a5838803c7.jpg",
            "https://te.legra.ph/file/0825940622e72930245df.jpg",
            "https://te.legra.ph/file/b37a59ccd2e7f37b39080.jpg"
           ]


@Client.on_message(filters.command(["afk"]))
async def active_afk(_, message: Message):
    devil = random.choice(JAI_HIND)
    blocked = await is_blocked(message.from_user.id)
    if blocked:
        return
    if message.sender_chat:
        return
    user_id = message.from_user.id
    try:
        await message.delete()
    except:
        pass
    await message.reply_photo(
        devil, caption=f"{message.from_user.first_name} is now away from keyboard ...!"
    )

    verifier, reasondb = await is_afk(user_id)
    if verifier:
        await remove_afk(user_id)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time((int(time.time() - timeafk)))
            if afktype == "text":
                return await message.reply_text(
                    f"**{message.from_user.first_name}** is back online and was away for {seenago}",
                    disable_web_page_preview=True,
                )
            if afktype == "text_reason":
                return await message.reply_text(
                    f"**{message.from_user.first_name}** is back online and was away for {seenago}\n\nReason: `{reasonafk}`",
                    disable_web_page_preview=True,
                )
            if afktype == "animation":
                if str(reasonafk) == "None":
                    return await message.reply_animation(
                        data,
                        caption=f"**{message.from_user.first_name}** is back online and was away for {seenago}",
                    )
                else:
                    return await message.reply_animation(
                        data,
                        caption=f"**{message.from_user.first_name}** is back online and was away for {seenago}\n\nReason: `{reasonafk}",
                    )
            if afktype == "photo":
                if str(reasonafk) == "None":
                    return await message.reply_photo(
                        photo=f"downloads/{user_id}.jpg",
                        caption=f"**{message.from_user.first_name}** is back online and was away for {seenago}",
                    )
                else:
                    return await message.reply_photo(
                        photo=f"downloads/{user_id}.jpg",
                        caption=f"**{message.from_user.first_name}** is back online and was away for {seenago}\n\nReason: `{reasonafk}`",
                    )
        except Exception as e:
            return await message.reply_text(
                f"**{message.from_user.first_name}** is back online",
                disable_web_page_preview=True,
            )
    if len(message.command) == 1 and not message.reply_to_message:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(message.command) > 1 and not message.reply_to_message:
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "text_reason",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    elif (
        len(message.command) == 1
        and message.reply_to_message.animation
    ):
        _data = message.reply_to_message.animation.file_id
        details = {
            "type": "animation",
            "time": time.time(),
            "data": _data,
            "reason": None,
        }
    elif (
        len(message.command) > 1
        and message.reply_to_message.animation
    ):
        _data = message.reply_to_message.animation.file_id
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        details = {
            "type": "animation",
            "time": time.time(),
            "data": _data,
            "reason": _reason,
        }
    elif len(message.command) == 1 and message.reply_to_message.photo:
        await _.download_media(
            message.reply_to_message, file_name=f"{user_id}.jpg"
        )
        details = {
            "type": "photo",
            "time": time.time(),
            "data": None,
            "reason": None,
        }
    elif len(message.command) > 1 and message.reply_to_message.photo:
        await _.download_media(
            message.reply_to_message, file_name=f"{user_id}.jpg"
        )
        _reason = message.text.split(None, 1)[1].strip()
        details = {
            "type": "photo",
            "time": time.time(),
            "data": None,
            "reason": _reason,
        }
    elif (
        len(message.command) == 1 and message.reply_to_message.sticker
    ):
        if message.reply_to_message.sticker.is_animated:
            details = {
                "type": "text",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
        else:
            await _.download_media(
                message.reply_to_message, file_name=f"{user_id}.jpg"
            )
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": None,
            }
    elif (
        len(message.command) > 1 and message.reply_to_message.sticker
    ):
        _reason = (message.text.split(None, 1)[1].strip())[:100]
        if message.reply_to_message.sticker.is_animated:
            details = {
                "type": "text_reason",
                "time": time.time(),
                "data": None,
                "reason": _reason,
            }
        else:
            await _.download_media(
                message.reply_to_message, file_name=f"{user_id}.jpg"
            )
            details = {
                "type": "photo",
                "time": time.time(),
                "data": None,
                "reason": _reason,
            }
    else:
        details = {
            "type": "text",
            "time": time.time(),
            "data": None,
            "reason": None,
        }

    await add_afk(user_id, details)
 
