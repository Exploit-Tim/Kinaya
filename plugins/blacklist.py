# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.

# port to userbot from uniborg by @keselekpermen69


import io
import re

from pyAyiin import cmdHelp
from pyAyiin.decorator import ayiinCmd, ayiinHandler
from pyAyiin.database.blFilters import (
    addToBlacklist,
    getChatBlacklist,
    rmFromBlacklist,
    updateToBlacklist
)
from pyAyiin.decorator import ayiinCmd, ayiinHandler
from pyAyiin.utils import eor

from . import cmd


def check_for_blacklist(chat_id, trigger):
    all_filters = getChatBlacklist(chat_id)
    for keywords in all_filters:
        keyword = keywords[1]
        if trigger == keyword:
            return True
    return False


@ayiinHandler(incoming=True)
async def on_new_message(event):
    # TODO: exempt admins from locks
    name = event.raw_text
    snips = getChatBlacklist(event.chat_id)
    if snips:
        for snip in snips:
            pattern = r"( |^|[^\w])" + re.escape(snip[2]) + r"( |$|[^\w])"
            if re.search(pattern, name, flags=re.IGNORECASE):
                try:
                    await event.delete()
                except Exception:
                    await eor(
                        event,
                        "**Saya memerlukan hak admin untuk melakukan tindakan ini!**",
                        time=8
                    )
                    rmFromBlacklist(event.chat_id, snip[2])
                break
    else:
        return


@ayiinCmd(pattern="addbl(?: |$)(.*)")
async def on_add_black_list(addbl):
    text = addbl.pattern_match.group(1)
    to_blacklist = list(
        {trigger.strip() for trigger in text.split("\n") if text.strip()}
    )
    for trigger in to_blacklist:
        cek = check_for_blacklist(addbl.chat_id, trigger.lower())
        if cek:
            updateToBlacklist(addbl.chat_id, addbl.chat.title, trigger.lower())
        else:
            addToBlacklist(addbl.chat_id, addbl.chat.title, trigger.lower())
    await eor(
        addbl,
        f"Berhasil: `{text}` Memasukan Daftar Kata Terlarang di sini."
    )


@ayiinCmd(pattern="listbl(?: |$)(.*)")
async def on_view_blacklist(listbl):
    all_blacklisted = getChatBlacklist(listbl.chat_id)
    if all_blacklisted:
        OUT_STR = f"Daftar Kata Terlarang Di {all_blacklisted[0][1]} :\n\n"
        for trigger in all_blacklisted:
            OUT_STR += f"`{trigger[2]}`\n"
        if len(OUT_STR) > 4096:
            with io.BytesIO(str.encode(OUT_STR)) as out_file:
                out_file.name = "blacklist.text"
                await listbl.client.send_file(
                    listbl.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption="Blacklist Dalam Obrolan Ini",
                    reply_to=listbl,
                )
                await listbl.delete()
    else:
        OUT_STR = "Tidak Ada Daftar Kata Terlarang Yang Ditemukan Di Sini"
    await eor(listbl, OUT_STR)


@ayiinCmd(pattern="rmbl(?: |$)(.*)")
async def on_delete_blacklist(rmbl):
    text = rmbl.pattern_match.group(1)
    to_unblacklist = list(
        {trigger.strip() for trigger in text.split("\n") if trigger.strip()}
    )
    successful = sum(
        bool(rmFromBlacklist(rmbl.chat_id, trigger.lower()))
        for trigger in to_unblacklist
    )
    if not successful:
        await rmbl.edit(f"**{text}** `Tidak Ada Di Blacklist`")
    else:
        await rmbl.edit(f"Berhasil Menghapus `{text}` dari Kata Terlarang.")


cmdHelp.update(
    {
        "blacklist": f"**Plugin : **`blacklist`\
        \n\n  »  **Perintah :** `{cmd}listbl`\
        \n  »  **Kegunaan : **Melihat daftar blacklist yang aktif di obrolan.\
        \n\n  »  **Perintah :** `{cmd}addbl` <kata>\
        \n  »  **Kegunaan : **Memasukan pesan ke blacklist 'kata blacklist'.\
        \n\n  »  **Perintah :** `{cmd}rmbl` <kata>\
        \n  »  **Kegunaan : **Menghapus kata blacklist.\
    "
    }
)
