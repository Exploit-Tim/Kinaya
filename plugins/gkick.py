# Ported by X_ImFine
# Recode by @mrismanaziz

from telethon.tl.functions.contacts import BlockRequest, UnblockRequest

from pyAyiin import ayiin, cmdHelp
from pyAyiin.decorator import ayiinCmd

from . import cmd


@ayiinCmd(pattern="gkick(?: |$)(.*)")
async def gspide(rk):
    lazy = rk
    rkp = await lazy.edit('**Memproses...**')
    me = await rk.client.get_me()
    await rkp.edit("`Memproses Global Kick Jamet Goblok!`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    await rk.get_chat()
    a = b = 0
    if rk.is_private:
        user = rk.chat
        reason = rk.pattern_match.group(1)
    try:
        user, reason = await ayiin.getUserFromEvent(rk)
    except BaseException:
        pass
    try:
        if not reason:
            reason = "Private"
    except BaseException:
        return await rkp.edit("**Gagal Global Kick! Pengguna tidak dikenal.**")
    if user:
        if user.id in ayiin._devs:
            return await rkp.edit("**Jangan Ngadi Ngadi itu CODER aing`")
        try:
            await rk.client(BlockRequest(user))
            await rk.client(UnblockRequest(user))
        except BaseException:
            pass
        testrk = [
            d.entity.id
            for d in await rk.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for i in testrk:
            try:
                await rk.client.edit_permissions(i, user, view_messages=False)
                await rk.client.edit_permissions(i, user, send_messages=True)
                a += 1
                await rkp.edit(f"`Memproses Global Kick Jamet Goblok! Gkicked di {a} Group Chats..`"
                )

            except BaseException:
                b += 1
    else:
        await rkp.edit("**Mohon Balas Ke Pesan Penggunanya**")

    return await rkp.edit(
        f"**Berhasil GKicked** [{user.first_name}](tg://user?id={user.id}) **di {a} Group Chats**"
    )


cmdHelp.update(
    {
        "gkick": f"**Plugin : **`gkick`\
        \n\n  »  **Perintah :** `{cmd}gkick` <alasan>\
        \n  »  **Kegunaan : **kick pengguna secara global dari semua Administrasi Grup di mana Anda berada.\
    "
    }
)
