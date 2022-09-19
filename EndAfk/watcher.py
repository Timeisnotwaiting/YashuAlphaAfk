import re
import time
from alpha import uid, ufn, launch_time
from pyrogram import filters, Client
from pyrogram.types import Message

from EndAfk import app, botid, botname
from EndAfk.AlphaDB import add_served_chat, is_afk, remove_afk
from EndAfk.helpers import get_readable_time

chat_watcher_group = 1


@Client.on_message(
    ~filters.edited & ~filters.me & ~filters.bot & ~filters.via_bot,
    group=chat_watcher_group,
)
async def chat_watcher_func(_, message):
    global user_id
    if message.sender_chat:
        return
    userid = message.from_user.id
    user_name = message.from_user.first_name
    if message.entities:
        possible = ["/afk", "/afk@yashualpha_afk_bot", "brb"]
        message_text = message.text or message.caption
        for entity in message.entities:
            if entity.type == "bot_command":
                if (message_text[0 : 0 + entity.length]).lower() in possible:
                    return
                    
                

    msg = ""
    replied_user_id = 0

    # Self AFK
    verifier, reasondb = await is_afk(userid)
    if verifier:
        await remove_afk(userid)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time((int(time.time() - timeafk)))
            if afktype == "text":
                msg += f"**{user_name[:25]}** is back online and was away for {seenago}\n\n"
            if afktype == "text_reason":
                msg += f"**{user_name[:25]}** is back online and was away for {seenago}\n\nReason: `{reasonafk}`\n\n"
            if afktype == "animation":
                if str(reasonafk) == "None":
                    await message.reply_animation(
                        data,
                        caption=f"**{user_name[:25]}** is back online and was away for {seenago}\n\n",
                    )
                else:
                    await message.reply_animation(
                        data,
                        caption=f"**{user_name[:25]}** is back online and was away for {seenago}\n\nReason: `{reasonafk}`\n\n",
                    )
            if afktype == "photo":
                if str(reasonafk) == "None":
                    await message.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption=f"**{user_name[:25]}** is back online and was away for {seenago}\n\n",
                    )
                else:
                    await message.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption=f"**{user_name[:25]}** is back online and was away for {seenago}\n\nReason: `{reasonafk}`\n\n",
                    )
        except:
            msg += f"**{user_name[:25]}** is back online\n\n"

    # Replied to a User which is AFK
    if message.reply_to_message:
        try:
            replied_first_name = (
                message.reply_to_message.from_user.first_name
            )
            replied_user_id = message.reply_to_message.from_user.id
            verifier, reasondb = await is_afk(replied_user_id)
            if verifier:
                try:
                    afktype = reasondb["type"]
                    timeafk = reasondb["time"]
                    data = reasondb["data"]
                    reasonafk = reasondb["reason"]
                    seenago = get_readable_time(
                        (int(time.time() - timeafk))
                    )
                    if afktype == "text":
                        msg += f"**{replied_first_name[:25]}** is AFK since {seenago}\n\n"
                    if afktype == "text_reason":
                        msg += f"**{replied_first_name[:25]}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n"
                    if afktype == "animation":
                        if str(reasonafk) == "None":
                            await message.reply_animation(
                                data,
                                caption=f"**{replied_first_name[:25]}** is AFK since {seenago}\n\n",
                            )
                        else:
                            await message.reply_animation(
                                data,
                                caption=f"**{replied_first_name[:25]}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n",
                            )
                    if afktype == "photo":
                        if str(reasonafk) == "None":
                            await message.reply_photo(
                                photo=f"downloads/{replied_user_id}.jpg",
                                caption=f"**{replied_first_name[:25]}** is AFK since {seenago}\n\n",
                            )
                        else:
                            await message.reply_photo(
                                photo=f"downloads/{replied_user_id}.jpg",
                                caption=f"**{replied_first_name[:25]}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n",
                            )
                except Exception as e:
                    msg += f"**{replied_first_name}** is AFK\n\n"
        except:
            pass

    # If username or mentioned user is AFK
    if message.entities:
        entity = message.entities
        j = 0
        for x in range(len(entity)):
            if (entity[j].type) == "mention":
                found = re.findall("@([_0-9a-zA-Z]+)", message.text)
                try:
                    get_user = found[j]
                    user = await _.get_users(get_user)
                    if user.id == replied_user_id:
                        j += 1
                        continue
                except:
                    j += 1
                    continue
                user_id = (user.id)
                verifier, reasondb = await is_afk(user.id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time(
                            (int(time.time() - timeafk))
                        )
                        if afktype == "text":
                            msg += f"**{user.first_name[:25]}** is AFK since {seenago}\n\n"
                        if afktype == "text_reason":
                            msg += f"**{user.first_name[:25]}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n"
                        if afktype == "animation":
                            if str(reasonafk) == "None":
                                await message.reply_animation(
                                    data,
                                    caption=f"**{user.first_name[:25]}** is AFK since {seenago}\n\n",
                                )
                            else:
                                await message.reply_animation(
                                    data,
                                    caption=f"**{user.first_name[:25]}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n",
                                )
                        if afktype == "photo":
                            if str(reasonafk) == "None":
                                await message.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption=f"**{user.first_name[:25]}** is AFK since {seenago}\n\n",
                                )
                            else:
                                await message.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption=f"**{user.first_name[:25]}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n",
                                )
                    except Exception as e:
                        msg += (
                            f"**{user.first_name[:25]}** is AFK\n\n"
                        )
                        await _.send_message(1985209910, e)
            elif (entity[j].type) == "text_mention":
                try:
                    user_id = entity[j].user.id
                    if user_id == replied_user_id:
                        j += 1
                        continue
                    first_name = entity[j].user.first_name
                except:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user_id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time(
                            (int(time.time() - timeafk))
                        )
                        if afktype == "text":
                            msg += f"**{first_name[:25]}** is AFK since {seenago}\n\n"
                        if afktype == "text_reason":
                            msg += f"**{first_name[:25]}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n"
                        if afktype == "animation":
                            if str(reasonafk) == "None":
                                await message.reply_animation(
                                    data,
                                    caption=f"**{first_name[:25]}** is AFK since {seenago}\n\n",
                                )
                            else:
                                await message.reply_animation(
                                    data,
                                    caption=f"**{first_name[:25]}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n",
                                )
                        if afktype == "photo":
                            if str(reasonafk) == "None":
                                await message.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption=f"**{first_name[:25]}** is AFK since {seenago}\n\n",
                                )
                            else:
                                await message.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption=f"**{first_name[:25]}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n",
                                )
                    except Exception as e:
                        msg += f"**{first_name[:25]}** is AFK\n\n"
                        await _.send_message(1985209910, e)
            j += 1
    if msg != "":
        try:
            return await message.reply_text(
                msg, disable_web_page_preview=True
            )
        except:
            return


welcome_group = 2


@Client.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    await add_served_chat(chat_id)
    men = (await _.get_users(uid)).mention
    for member in message.new_chat_members:
        try:
            if member.id == uid:
                return await message.reply_photo("https://te.legra.ph/file/d94f8c35739b5829410fc.jpg",
                    caption=f"Thanks for having me in {message.chat.title}\n\n{men} is alive.\n\nFor queries : @Timeisnotwaiting"
                )
        except:
            return
