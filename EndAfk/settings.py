from pyrogram import Client, filters
from EndAfk.AlphaDB import toggle_cc, check_cc, is_blocked
from pyrogram.types import CallbackQuery as CBQ, InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM

id = None


IMG = "https://te.legra.ph/file/b6688358e580edc06f999.jpg"

@Client.on_message(filters.command("settings"))
async def settings(_, m):
    global id
    if str(m.chat.id)[0] != "-":
        return
    if await is_blocked(m.from_user.id):
        return
    id = m.from_user.id
    y = await check_cc(m.chat.id)
    x = True if y else False
    mk = [
        [
        IKB("Commands Clean", callback_data="cc_answer"),
        IKB("{}".format("Enabled ✅" if x else "Disabled ❌"), callback_data="cc_toggle")
        ],
        [
        IKB("Close 🔙", callback_data="close")
        ]
    ]
    await m.reply_photo(IMG, caption=f"⚙️ AFK Bot settings\n\n🏘️ Group :- {m.chat.title}\n\n🆔 Group id :- <code>{m.chat.id}</code>\n\nChoose from below options !", reply_markup=IKM(mk))
    
@Client.on_callback_query(filters.regex("cc_answer"))
async def cc_ans(_, q):
    await q.answer("What's this ?\n\nIf this mode is enabled, Command messages will be deleted automatically.\n\nFor this, bot must be admin with delete messages right !", show_alert=True)
    
@Client.on_callback_query(filters.regex("cc_toggle"))
async def cc_tog(_, q):
    z = await _.get_chat_member(q.message.chat.id, q.from_user.id)
    if not z.status in ["creator", "administrator"]:
        return await q.answer("Only admins can make changes !", show_alert=True)
    await toggle_cc(q.message.chat.id)
    y = await check_cc(q.message.chat.id)
    x = True if y else False
    mk = [
        [
        IKB("COMMANDS CLEAN", callback_data="cc_answer"),
        IKB("{}".format("Enabled ✅" if x else "Disabled ❌"), callback_data="cc_toggle")
        ],
        [
        IKB("Close 🔙", callback_data="close")
        ]
    ]
    try:
        await q.answer()
        await q.edit_message_reply_markup(reply_markup=IKM(mk))
    except Exception as e:
        await q.message.reply(e)

@Client.on_callback_query(filters.regex("close"))
async def close(_, q):
    global id
    await q.answer()
    if q.from_user.id != id:
        return
    await q.message.delete()
