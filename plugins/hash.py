# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing hash and encode/decode commands. """
from subprocess import PIPE
from subprocess import run as runapp

import pybase64

from pyAyiin import cmdHelp
from pyAyiin.decorator import ayiinCmd

from . import cmd


@ayiinCmd("hash (.*)")
async def gethash(hash_q):
    """For .hash command, find the md5, sha1, sha256, sha512 of the string."""
    hashtxt_ = hash_q.pattern_match.group(1)
    with open("hashdis.txt", "w+") as hashtxt:
        hashtxt.write(hashtxt_)
    md5 = runapp(["md5sum", "hashdis.txt"], stdout=PIPE, check=True)
    md5 = md5.stdout.decode()
    sha1 = runapp(["sha1sum", "hashdis.txt"], stdout=PIPE, check=True)
    sha1 = sha1.stdout.decode()
    sha256 = runapp(["sha256sum", "hashdis.txt"], stdout=PIPE, check=True)
    sha256 = sha256.stdout.decode()
    sha512 = runapp(["sha512sum", "hashdis.txt"], stdout=PIPE, check=True)
    runapp(["rm", "hashdis.txt"], stdout=PIPE, check=True)
    sha512 = sha512.stdout.decode()
    ans = (
        "Text: `"
        + hashtxt_
        + "`\nMD5: `"
        + md5
        + "`SHA1: `"
        + sha1
        + "`SHA256: `"
        + sha256
        + "`SHA512: `"
        + sha512[:-1]
        + "`"
    )
    if len(ans) > 4096:
        with open("hashes.txt", "w+") as hashfile:
            hashfile.write(ans)
        await hash_q.client.send_file(
            hash_q.chat_id,
            "hashes.txt",
            reply_to=hash_q.id,
            caption="**It's too big, sending a text file instead.**",
        )
        runapp(["rm", "hashes.txt"], stdout=PIPE, check=True)
    else:
        await hash_q.reply(ans)


@ayiinCmd("base64 (en|de) (.*)")
async def endecrypt(query):
    """For .base64 command, find the base64 encoding of the given string."""
    if query.pattern_match.group(1) == "en":
        lething = str(pybase64.b64encode(
            bytes(query.pattern_match.group(2), "utf-8")))[2:]
        await query.reply("**Encoded:** `" + lething[:-1] + "`")
    else:
        lething = str(
            pybase64.b64decode(
                bytes(query.pattern_match.group(2), "utf-8"), validate=True
            )
        )[2:]
        await query.reply("**Decoded:** `" + lething[:-1] + "`")


cmdHelp.update(
    {
        "hash": f"**Plugin : **`hash`\
        \n\n  »  **Perintah :** `{cmd}hash`\
        \n  »  **Kegunaan : **Untuk menemukan md5, sha1, sha256, sha512 dari string tersebut saat ditulis ke dalam file txt.\
    "
    }
)


cmdHelp.update(
    {
        "base64": f"**Plugin : **`base64`\
        \n\n  »  **Perintah :** `{cmd}base64` [en atau de]\
        \n  »  **Kegunaan : **Temukan pengkodean base64 dari string yang diberikan atau pecahkan kodenya.\
        \n\n  •  **NOTE : en = encode , de = decode\
    "
    }
)
