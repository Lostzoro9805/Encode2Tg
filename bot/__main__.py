#    This file is part of the Compressor distribution.
#    Copyright (c) 2021 Danish_00
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
# License can be found in
# <https://github.com/1Danish-00/CompressorQueue/blob/main/License> .


from . import *
from .devtools import *

LOGS.info("Starting...")


######## Connect ########


try:
    bot.start(bot_token=BOT_TOKEN)
except Exception as er:
    LOGS.info(er)


####### GENERAL CMDS ########


@bot.on(events.NewMessage(pattern="/start"))
async def _(e):
    await start(e)


@bot.on(events.NewMessage(pattern="/ping"))
async def _(e):
    await up(e)


@bot.on(events.NewMessage(pattern="/help"))
async def _(e):
    await help(e)


@bot.on(events.NewMessage(pattern="/restart"))
async def _(e):
    await restart(e)


@bot.on(events.NewMessage(pattern="/cancelall"))
async def _(e):
    await clean(e)


@bot.on(events.NewMessage(pattern="/showthumb"))
async def _(e):
    await getthumb(e)


@bot.on(events.NewMessage(pattern="/clear"))
async def _(e):
    await clearqueue(e)


######## Callbacks #########


@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"stats(.*)")))
async def _(e):
    await stats(e)


@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"pres(.*)")))
async def _(e):
    await pres(e)


@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"skip(.*)")))
async def _(e):
    await skip(e)


@bot.on(events.callbackquery.CallbackQuery(data=re.compile("ihelp")))
async def _(e):
    await ihelp(e)


@bot.on(events.callbackquery.CallbackQuery(data=re.compile("beck")))
async def _(e):
    await beck(e)


########## Direct ###########


@bot.on(events.NewMessage(pattern="/eval"))
async def _(e):
    await eval(e)


@bot.on(events.NewMessage(pattern="/bash"))
async def _(e):
    await bash(e)


@bot.on(events.NewMessage(pattern="/status"))
async def _(e):
    await status(e)


@bot.on(events.NewMessage(pattern="/parse"))
async def _(e):
    await discap(e)


@bot.on(events.NewMessage(pattern="/reset"))
async def _(e):
    await reffmpeg(e)


@bot.on(events.NewMessage(pattern="/get"))
async def _(e):
    await check(e)


@bot.on(events.NewMessage(pattern="/set"))
async def _(e):
    await change(e)


@bot.on(events.NewMessage(pattern="/queue"))
async def _(e):
    await listqueue(e)


@bot.on(events.NewMessage(pattern="/encodequeue"))
async def _(e):
    await listqueuep(e)


@bot.on(events.NewMessage(pattern="/groupenc"))
async def _(e):
    await allowgroupenc(e)


@bot.on(events.NewMessage(pattern="/logs"))
async def _(e):
    await getlogs(e)


########## AUTO ###########


@bot.on(events.NewMessage(incoming=True))
async def _(e):
    await thumb(e)


@bot.on(events.NewMessage(incoming=True))
async def _(e):
    await encod(e)

async def something():
    for i in itertools.count():
        try:
            if not WORKING and QUEUE:
                # user = int(OWNER.split()[0])
                file = list(QUEUE.keys())[0]
                name, user = QUEUE[list(QUEUE.keys())[0]]
                e = await bot.send_message(user, "`▼ Downloding Queue Files ▼`")
                if LOG_CHANNEL:
                    log = int(LOG_CHANNEL)
                    op = await bot.send_message(
                        log,
                        f"`Currently Downloading A Queued Video…`",
                    )
                s = dt.now()
                try:
                    dl = "downloads/" + name
                    down = await download_file(
                        message=file,
                        file_name=dl,
                    )
                except Exception as r:
                    er = traceback.format_exc()
                    LOGS.info(r)
                    LOGS.info(er)
                    WORKING.clear()
                    QUEUE.pop(list(QUEUE.keys())[0])
                    await save2db()
                es = dt.now()
                kk = dl.split("/")[-1]
                aa = kk.split(".")[-1]
                rr = "encode"
                bb = kk.replace(f".{aa}", " compressed.mkv")
                out = f"{rr}/{bb}"
                thum = "thumb.jpg"
                dtime = ts(int((es - s).seconds) * 1000)
                hehe = f"{out};{dl};{list(QUEUE.keys())[0]}"
                wah = code(hehe)
                nn = await e.edit(
                    "`Encoding Files…` \n**⏳This Might Take A While⏳**",
                    buttons=[
                        [Button.inline("📂", data=f"pres{wah}")],
                        [Button.inline("STATS", data=f"stats{wah}")],
                        [Button.inline("CANCEL PROCESS", data=f"skip{wah}")],
                    ],
                )
                if LOG_CHANNEL:
                    wak = await op.edit(
                        f"[{sender.first_name}](tg://user?id={user}) `Is Currently Encoding A Queued Video…`",
                        buttons=[
                            [Button.inline("📁", data=f"pres{wah}")],
                            [Button.inline("CHECK PROGRESS", data=f"stats{wah}")],
                            [Button.inline("CANCEL PROCESS", data=f"skip{wah}")],
                        ],
                    )
                cmd = ffmpeg.format(dl, out)
                process = await asyncio.create_subprocess_shell(
                    cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                er = stderr.decode()
                try:
                    if process.returncode != 0:
                        if len(stderr) > 4095:
                            yo = await app.send_message(user, "Uploading Error logs…")
                            out_file = "ffmpeg_error.txt"
                            with open("ffmpeg_error.txt", "w") as file:
                                file.write(str(stderr.decode()))
                                wrror = await yo.reply_document(
                                    document=out_file,
                                    force_document=True,
                                    quote=True,
                                    caption="`ffmpeg error`",
                                )
                            yo.delete()
                            os.remove(out_file)
                        else:
                            wrror = await nn.reply(stderr.decode())
                        nnn = await wrror.reply(
                            f"🔺 **Encoding of** `{bb2}` **Failed!**"
                        )
                        try:
                            os.remove(dl)
                        except Exception:
                            await nnn.reply("**Reason:** Download Cancelled!")
                        try:
                            await nn.delete()
                            await wak.delete()
                        except Exception:
                            pass
                        QUEUE.pop(list(QUEUE.keys())[0])
                        await save2db()
                        continue
                except BaseException:
                    er = traceback.format_exc()
                    LOGS.info(er)
                    LOGS.info(stderr.decode)
                ees = dt.now()
                time.time()
                try:
                    await nn.delete()
                    await wak.delete()
                except Exception:
                    pass
                tex = "`▲ Uploading ▲`"
                nnn = await app.send_message(chat_id=e.chat_id, text=tex)
                fname = out.split("/")[1]
                pcap = await custcap(name, fname)
                ds = await upload2(app, e.chat_id, out, nnn, thum)
                await nnn.delete()
                if LOG_CHANNEL:
                    chat = int(LOG_CHANNEL)
                    await ds.copy(chat_id=chat)
                org = int(Path(dl).stat().st_size)
                com = int(Path(out).stat().st_size)
                pe = 100 - ((com / org) * 100)
                per = str(f"{pe:.2f}") + "%"
                eees = dt.now()
                x = dtime
                xx = ts(int((ees - es).seconds) * 1000)
                xxx = ts(int((eees - ees).seconds) * 1000)
                try:
                    a1 = await info(dl, e)
                    a2 = await info(out, e)
                    text = ""
                    if rlsgrp:
                        text += f"**Source:** `[{rlsgrp}]`"
                    text += f"\n\nMediainfo: **[Before]({a1})**//**[After]({a2})**"
                    dp = await ds.reply(
                        text,
                        disable_web_page_preview=True,
                        quote=True,
                    )
                    if LOG_CHANNEL:
                        await dp.copy(chat_id=chat)
                except Exception:
                    pass
                dk = await ds.reply(
                    f"**Encode Stats:**\n\nOriginal Size : {hbs(org)}\nEncoded Size : {hbs(com)}\nEncoded Percentage : {per}\n\nDownloaded in {x}\nEncoded in {xx}\nUploaded in {xxx}",
                    disable_web_page_preview=True,
                    quote=True,
                )
                if LOG_CHANNEL:
                    await dk.copy(chat_id=chat)
                QUEUE.pop(list(QUEUE.keys())[0])
                await save2db()
                os.system("rm -rf thumb2.jpg")
                os.remove(dl)
                os.remove(out)
            else:
                await asyncio.sleep(3)
        except Exception as err:
            er = traceback.format_exc()
            LOGS.info(er)
            LOGS.info(err)


########### Start ############

LOGS.info("Bot has started.")
with bot:
    bot.loop.run_until_complete(startup())
    bot.loop.run_until_complete(something())
    bot.loop.run_forever()
