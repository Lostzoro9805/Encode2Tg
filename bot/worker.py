#    This file is part of the CompressorQueue distribution.
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
# License can be found in <
# https://github.com/1Danish-00/CompressorQueue/blob/main/License> .

import shutil
import time
from pathlib import Path

import psutil

from .funcn import *
from .util import custcap, dynamicthumb, get_readable_file_size, parse
from .worker import *


async def getlogs(event):
    if str(event.sender_id) not in OWNER and event.sender_id != DEV:
        return await event.delete()
    await event.client.send_file(event.chat_id, file=LOG_FILE_NAME, force_document=True)


async def save2db():
    if DATABASE_URL:
        y = json.dumps(QUEUE)
        queue.delete_many({})
        queue.insert_one({"queue": y})


async def save2db2(mara, para):
    if DATABASE_URL:
        y = json.dumps(para)
        mara.delete_many({})
        mara.insert_one({"queue": [y, "0"]})


async def version2(event):
    if str(event.sender_id) not in OWNER:
        return await event.delete()
    temp = ""
    try:
        temp = event.text.split(" ", maxsplit=1)[1]
    except Exception:
        pass
    if temp:
        VERSION2.clear()
        VERSION2.append(temp)
        await event.reply(f"**Added V2 Tag Successfully!\nV2 Reason:** `{temp}`")
    else:
        VERSION2.clear()
        await event.reply("**Removed V2 Tag Successfully!**")


async def discap(event):
    if str(event.sender_id) not in OWNER:
        return await event.delete()
    ttx = Path("cap.txt")
    if ttx.is_file():
        os.remove(ttx)
        await event.reply("**Successfully Enabled Parse By Caption**")
    else:
        file = open(ttx, "w")
        file.close()
        await event.reply("**Successfully Disabled Parse By Caption**")


async def clean(event):
    if str(event.sender_id) not in OWNER and event.sender_id != DEV:
        return await event.delete()
    await event.reply("**Cleared Queued, Working Files and Cached Downloads!**")
    WORKING.clear()
    QUEUE.clear()
    if DATABASE_URL:
        queue.delete_many({})
    os.system("rm -rf downloads/*")
    os.system("rm -rf encode/*")
    for proc in psutil.process_iter():
        processName = proc.name()
        processID = proc.pid
        print(processName, " - ", processID)
        if processName == "ffmpeg":
            os.kill(processID, signal.SIGKILL)
    return


async def upload2(bot, from_user_id, filepath, reply, thum, caption):
    await reply.edit("🔺Uploading🔺")
    u_start = time.time()
    s = await bot.send_document(
        document=filepath,
        chat_id=from_user_id,
        force_document=True,
        thumb=thum,
        caption=caption,
        progress=progress_for_pyrogram,
        progress_args=(bot, "Uploading 👘", reply, u_start),
    )
    return s


async def restart(event):
    if str(event.sender_id) not in OWNER:
        return await event.delete()
    try:
        rst = await event.reply("`Trying To Restart`")
        await asyncio.sleep(1)
        await rst.edit("`Restarting Please Wait…`")
        os.system("kill -9 -1")
    except Exception as err:
        await event.reply("Error Occurred")
        LOGS.info(str(err))


async def listqueue(event):
    if str(event.sender_id) not in OWNER:
        return await event.delete()
    if not QUEUE:
        yo = await event.reply("Nothing In Queue")
        await asyncio.sleep(3)
        await yo.delete()
        return await event.delete()
    try:
        if WORKING:
            i = 0
        else:
            i = 1
        x = ""
        while i < len(QUEUE):
            y, yy = QUEUE[list(QUEUE.keys())[i]]
            x += f"{i}. {y}\n"
            i = i + 1
        x += "\n**To remove an item from queue use** /clear <queue number>"
    except Exception:
        x = "No Pending Item in Queue 😒"
    yo = await event.reply(x)
    await asyncio.sleep(10)
    await event.delete()
    await yo.delete()


async def listqueuep(event):
    if str(event.sender_id) not in OWNER:
        return await event.delete()
    if not QUEUE:
        yo = await event.reply("Nothing In Queue")
        await asyncio.sleep(3)
        await yo.delete()
        return await event.delete()
    try:
        if WORKING:
            i = 0
        else:
            i = 1
        x = ""
        while i < len(QUEUE):
            y, yy = QUEUE[list(QUEUE.keys())[i]]
            y = await qparse(y)
            x += f"{i}. {y}\n"
            i = i + 1
        x += "\n**Queue based on auto-generated filename if you you want the actual queue use the command** /queue "
    except Exception:
        x = "No Pending Item in Queue 😒"
    yo = await event.reply(x)
    await asyncio.sleep(10)
    await event.delete()
    await yo.delete()


async def reffmpeg(event):
    if str(event.sender_id) not in OWNER:
        return await event.delete()
    try:
        os.system(f"rm -rf ffmpeg.txt")
        file = open("ffmpeg.txt", "w")
        file.write(str(FFMPEG) + "\n")
        file.close()
        await save2db2(ffmpegdb, FFMPEG)
        await event.reply(f"**Changed FFMPEG Code to**\n\n`{FFMPEG}`")
    except Exception as err:
        await event.reply("Error Occurred")
        LOGS.info(str(err))


async def change(event):
    if str(event.sender_id) not in OWNER:
        return await event.delete()
    try:
        temp = ""
        try:
            temp = event.text.split(" ", maxsplit=1)[1]
        except Exception:
            pass
        if not temp:
            await event.reply(
                f"Setting ffmpeg failed\n**Try:**\n/set `(raw ffmpeg code Without brackets using the format specified in repo)`"
            )
            return
        os.system(f"rm -rf ffmpeg.txt")
        file = open("ffmpeg.txt", "w")
        file.write(str(temp) + "\n")
        file.close()
        await save2db2(ffmpegdb, temp)
        await event.reply(f"**Changed FFMPEG Code to**\n\n`{temp}`")
    except Exception as err:
        await event.reply("Error Occurred")
        LOGS.info(str(err))


async def check(event):
    if str(event.sender_id) not in OWNER and event.sender_id != DEV:
        return await event.delete()
    with open("ffmpeg.txt", "r") as file:
        ffmpeg = file.read().rstrip()
    await event.reply(f"**Current FFMPEG Code Is**\n\n`{ffmpeg}`")


async def allowgroupenc(event):
    if str(event.sender_id) not in OWNER:
        return await event.delete()
    if GROUPENC:
        GROUPENC.clear()
        yo = await event.reply("**Turned off Successfully**")
        await asyncio.sleep(10)
        await yo.delete()
        await event.delete()
    else:
        GROUPENC.append(1)
        yo = await event.reply(
            "**Group Encoding Turned on Successfully**\n__Persists till bot reboots!__"
        )
        await asyncio.sleep(10)
        await yo.delete()
        await event.delete()


async def getthumb(event):
    if str(event.sender_id) not in OWNER and event.sender_id != DEV:
        return await event.delete()
    tbcheck = Path("thumb2.jpg")
    if tbcheck.is_file():
        thum = "thumb2.jpg"
    else:
        thum = "thumb.jpg"
    await event.client.send_file(
        event.chat_id,
        file=thum,
        force_document=False,
        caption="**Your Current Thumbnail.**",
    )


async def rmfilter(event):
    if str(event.sender_id) not in OWNER:
        return await event.delete()
    try:
        fl = "filter.txt"
        os.remove(fl)
        if DATABASE_URL:
            filterz.delete_many({})
        await event.reply("`Filters Deleted!`")
    except Exception:
        await event.reply("❌ No Filters Found To Delete")


async def vfilter(event):
    if str(event.sender_id) not in OWNER:
        return await event.delete()
    try:
        olif = Path("filter.txt")
        if olif.is_file():
            with open("filter.txt", "r") as file:
                fil = file.read()
                fil1 = fil.split("\n")[0]
                fil2 = fil.split("\n")[1]
                fil3 = fil.split("\n")[2]
                file.close()
            await event.reply(
                f"Bot Will Automatically:\n\n **Remove:-** `{fil1}`\n **Tag Files as:-** `{fil2}`\n **Tag Type as:-** `{fil3}`"
            )
        else:
            await event.reply("`❌ No Filters Found!`")
    except Exception:
        await event.reply(
            "An Error Occurred\n Filter was wrongly set check accepted  format with /filter"
        )


async def filter(event):
    if str(event.sender_id) not in OWNER:
        return await event.delete()
    try:
        temp = ""
        try:
            temp = event.text.split(" ", maxsplit=1)[1]
        except Exception:
            pass
        if not temp:
            await event.reply(
                f"Setting filter failed\n**Try:**\n/filter `(whattoremove)`\n`(filetag)`\n`(typetag)`"
            )
            return
        os.system(f"rm -rf filter.txt")
        file = open("filter.txt", "w")
        file.write(str(temp))
        file.close()
        await save2db2(filterz, temp)
        await event.reply(f"**Changed filters to**\n\n`{temp}`")
    except Exception as err:
        await event.reply("Error Occurred")
        LOGS.info(str(err))


async def clearqueue(event):
    if str(event.sender_id) not in OWNER and event.sender_id != DEV:
        return await event.delete()
    temp = ""
    try:
        temp = event.text.split(" ", maxsplit=1)[1]
    except Exception:
        pass
    if temp:
        try:
            temp = int(temp)
            try:
                q, file = QUEUE[list(QUEUE.keys())[temp]]
                QUEUE.pop(list(QUEUE.keys())[temp])
                yo = await event.reply(f"{q} has been removed from queue")
                await save2db()
            except Exception:
                yo = await event.reply("Enter a valid queue number")
        except Exception:
            yo = await event.reply("Pass a number for an item on queue to be removed")
    else:
        yo = await event.reply("**Cleared Queued Files!**")
        QUEUE.clear()
        if DATABASE_URL:
            queue.delete_many({})
    await asyncio.sleep(7)
    await event.delete()
    await yo.delete()
    return


async def thumb(event):
    if str(event.sender_id) not in OWNER and event.sender_id != DEV:
        return
    if not event.photo:
        return
    os.system("rm thumb.jpg")
    await event.client.download_media(event.media, file="/bot/thumb.jpg")
    await event.reply("**Thumbnail Saved Successfully.**")


async def qparse(q):
    kk = q
    if "[" in kk and "]" in kk:
        pp = kk.split("[")[0]
        qq = kk.split("]")[1]
        kk = pp + qq
    else:
        kk = kk
    aa = kk.split(".")[-1]
    namo = q
    if "v2" in namo:
        name = namo.replace("v2", "")
    else:
        name = namo
    bb2 = await parse(name, kk, aa)
    bb = bb2[0]
    return bb


async def pres(e):
    try:
        wah = e.pattern_match.group(1).decode("UTF-8")
        wh = decode(wah)
        out, dl, id = wh.split(";")
        nme = out.split("/")[1]
        name = dl.split("/")[1]
        thumb = Path("thumb2.jpg")
        if thumb.is_file():
            oho = "Yes"
        else:
            oho = "No"
        por = str(QUEUE)
        t = len(QUEUE)
        if t > 0:
            if name in por and t < 2:
                q = "N/A"
                t = t - 1
            elif name in por:
                q, file = QUEUE[list(QUEUE.keys())[1]]
                q = await qparse(q)
                t = t - 1
            else:
                q, file = QUEUE[list(QUEUE.keys())[0]]
                q = await qparse(q)
        else:
            q = "N/A"
        q = (q[:45] + "…") if len(q) > 45 else q
        ansa = f"Auto-generated Filename:\n{nme}\n\nAuto-Generated Thumbnail:\n{oho}\n\nNext Up:\n{q}\n\nQueue Count:\n{t}"
        await e.answer(ansa, cache_time=0, alert=True)
    except Exception as er:
        LOGS.info(er)
        ansa = "YIKES"
        await e.answer(
            ansa,
            cache_time=0,
            alert=True,
        )


async def stats(e):
    try:
        wah = e.pattern_match.group(1).decode("UTF-8")
        wh = decode(wah)
        out, dl, id = wh.split(";")
        ot = hbs(int(Path(out).stat().st_size))
        ov = hbs(int(Path(dl).stat().st_size))
        ed = dt.now()
        name = dl.split("/")[1]
        input = (name[:45] + "…") if len(name) > 45 else name
        currentTime = ts(int((ed - uptime).seconds) * 1000)
        total, used, free = shutil.disk_usage(".")
        total = get_readable_file_size(total)
        used = get_readable_file_size(used)
        free = get_readable_file_size(free)
        get_readable_file_size(psutil.net_io_counters().bytes_sent)
        get_readable_file_size(psutil.net_io_counters().bytes_recv)
        cpuUsage = psutil.cpu_percent(interval=0.5)
        psutil.virtual_memory().percent
        psutil.disk_usage("/").percent
        ans = f"CPU: {cpuUsage}%\n\nTotal Disk Space:\n{total}\n\nDownloaded:\n{ov}\n\nFileName:\n{input}\n\nCompressing:\n{ot}\n\nBot Uptime:\n{currentTime}\n\nUsed: {used}  Free: {free}"
        await e.answer(ans, cache_time=0, alert=True)
    except Exception as er:
        LOGS.info(er)
        ed = dt.now()
        currentTime = ts(int((ed - uptime).seconds) * 1000)
        total, used, free = shutil.disk_usage(".")
        total = get_readable_file_size(total)
        info = f"Error 404: File | Info not Found 🤔\nMaybe Bot was restarted\nKindly Resend Media\n\nOther Info\n═══════════\nBot Uptime: {currentTime}\n\nTotal Disk Space: {total}"
        await e.answer(
            info,
            cache_time=0,
            alert=True,
        )


async def encod(event):
    try:
        EVENT2.clear()
        EVENT2.append(event)
    except Exception as er:
        LOGS.info(er)


async def pencode(message):
    try:
        if str(message.chat.id) not in OWNER:
            try:
                if str(message.from_user.id) not in OWNER:
                    return await message.delete()
                else:
                    if GROUPENC:
                        pass
                    else:
                        yo = await message.reply(
                            "#Warning\n\n**Pm me with files to encode instead\nOR\nclick /groupenc to turn on group encoding!**"
                        )
                        await asyncio.sleep(5)
                        await yo.delete()
                        return
            except BaseException:
                yo = await message.reply("🙄")
                await asyncio.sleep(5)
                return await yo.delete()
        if WORKING or QUEUE:
            xxx = await message.reply("`Adding To Queue`", quote=True)
            media_type = str(message.media)
            if media_type == "MessageMediaType.VIDEO":
                doc = message.video
            else:
                doc = message.document
            sem = message.caption
            ttt = Path("cap.txt")
            if sem and "\n" in sem:
                sem = ""
            if sem and not ttt.is_file():
                name = sem
            else:
                name = doc.file_name
            if not name:
                name = "video_" + dt.now().isoformat("_", "seconds") + ".mp4"
            root, ext = os.path.splitext(name)
            if not ext:
                ext = ".mkv"
                name = root + ext
            for item in QUEUE.values():
                if name in item:
                    return await xxx.edit(
                        "**THIS FILE HAS ALREADY BEEN ADDED TO QUEUE**"
                    )
            user = message.from_user.id
            QUEUE.update({doc.file_id: [name, user]})
            await save2db()
            return await xxx.edit(
                "**Added To Queue ⏰,** \n`Please Wait , Encode will start soon`"
            )
        WORKING.append(1)
        xxx = await message.reply(
            "`Download Pending…` \n**(Waiting For Connection)**", quote=True
        )
        if LOG_CHANNEL:
            log = int(LOG_CHANNEL)
            op = await bot.send_message(
                log,
                f"[{message.from_user.first_name}](tg://user?id={message.from_user.id}) `Is Currently Downloading A Video…`",
            )
        s = dt.now()
        ttt = time.time()
        dir = f"downloads/"
        try:
            media_type = str(message.media)
            if media_type == "MessageMediaType.DOCUMENT":
                # if hasattr(event.media, "document"):
                # file = event.media.document
                # sem = event.message.message
                sem = message.caption
                ttx = Path("cap.txt")
                sen = message.document.file_name
                if sem and "\n" in sem:
                    sem = ""
                if sem and not ttx.is_file():
                    filename = sem
                else:
                    filename = sen
                if not filename:
                    filename = "video_" + dt.now().isoformat("_", "seconds") + ".mp4"
                root, ext = os.path.splitext(filename)
                if not ext:
                    ext = ".mkv"
                    filename = root + ext
                dl = dir + filename
                xxx = await xxx.edit("`Waiting For Download To Complete`")
                # tex = "`Downloading File 📶`"
                etch = await message.reply("`Downloading File 📂`", quote=True)
                # etch = await app.send_message(chat_id=message.from_user.id,
                # text=tex)
                down = await app.download_media(
                    message=message,
                    file_name=dl,
                    progress=progress_for_pyrogram,
                    progress_args=(app, "`Downloading…`", etch, ttt),
                )
            else:
                sem = message.caption
                ttx = Path("cap.txt")
                if sem and "\n" in sem:
                    sem = ""
                if sem and not ttx.is_file():
                    filename = sem
                else:
                    filename = message.video.file_name
                if not filename:
                    filename = "video_" + dt.now().isoformat("_", "seconds") + ".mp4"
                root, ext = os.path.splitext(filename)
                if not ext:
                    ext = ".mkv"
                    filename = root + ext
                dl = dir + filename
                xxx = await xxx.edit("`Waiting For Media To Finish Downloading…`")
                # tex = "`Downloading Video 🎥`"
                # etch = await app.send_message(chat_id=message.from_user.id,
                # text=tex)
                etch = await message.reply("`Downloading Video 🎥`", quote=True)
                down = await app.download_media(
                    message=message,
                    file_name=dl,
                    progress=progress_for_pyrogram,
                    progress_args=(app, "`Downloading…`", etch, ttt),
                )
        except Exception:
            WORKING.clear()
            er = traceback.format_exc()
            LOGS.info(er)
            return os.remove(dl)
        await etch.delete()
        es = dt.now()
        kk = dl.split("/")[-1]
        aa = kk.split(".")[-1]
        rr = f"encode"
        namo = dl.split("/")[1]
        if "v2" in namo:
            name = namo.replace("v2", "")
        else:
            name = namo
        bb1 = await parse(name, kk, aa)
        bb = bb1[0]
        bb2 = bb1[1]
        # if "'" in bb:
        # bb = bb.replace("'", "")
        out = f"{rr}/{bb}"
        b, d, rlsgrp = await dynamicthumb(name, kk, aa)
        tbcheck = Path("thumb2.jpg")
        if tbcheck.is_file():
            thum = "thumb2.jpg"
        else:
            thum = "thumb.jpg"
        with open("ffmpeg.txt", "r") as file:
            nani = file.read().rstrip()
            # ffmpeg = file.read().rstrip()
            file.close()
        try:
            if "This Episode" in nani:
                b = b.replace("'", "")
                b = b.replace(":", "\\:")
                bo = b
                if d:
                    bo = f"Episode {d} of {b}"
                nano = nani.replace(f"This Episode", bo)
            else:
                nano = nani
        except Exception:
            nano = nani
        if "Fileinfo" in nano:
            # bb = bb.replace("'", "")
            ffmpeg = nano.replace(f"Fileinfo", bb2)
        else:
            ffmpeg = nano
        dtime = ts(int((es - s).seconds) * 1000)
        e = xxx
        hehe = f"{out};{dl};0"
        wah = code(hehe)
        user = message.from_user.id
        xxx = await xxx.edit("`Waiting For Encoding To Complete`")
        nn = await bot.send_message(
            user,
            "`Encoding File(s)…` \n**⏳This Might Take A While⏳**",
            buttons=[
                [Button.inline("📂", data=f"pres{wah}")],
                [Button.inline("STATS", data=f"stats{wah}")],
                [Button.inline("CANCEL PROCESS", data=f"skip{wah}")],
            ],
        )
        try:
            qb = b.replace(" ", "_")
            for xob in [
                "\\",
                "",
                "*",
                "{",
                "}",
                "[",
                "]",
                "(",
                ")",
                ">",
                "#",
                "+",
                "-",
                ".",
                "!",
                "$",
                "/",
                ":",
            ]:
                if xob in qb:
                    qb = qb.replace(xob, "")
        except NameError:
            ob = bb.split("@")[0]
            qb = ob.replace(" ", "_")
            for xob in [
                "\\",
                "",
                "*",
                "{",
                "}",
                "[",
                "]",
                "(",
                ")",
                ">",
                "#",
                "+",
                "-",
                ".",
                "!",
                "$",
                "/",
                ":",
            ]:
                if xob in qb:
                    qb = qb.replace(xob, "")
        if LOG_CHANNEL:
            log = int(LOG_CHANNEL)
            oro = await bot.send_message(
                log,
                f"Encoding Of #{qb} Started By [{message.from_user.first_name}](tg://user?id={message.from_user.id})",
            )
            wak = await op.edit(
                f"[{message.from_user.first_name}](tg://user?id={message.from_user.id}) `Is Currently Encoding A Video…`",
                buttons=[
                    [Button.inline("ℹ️", data=f"pres{wah}")],
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
                    out_file = "ffmpeg_error.txt"
                    with open("ffmpeg_error.txt", "w") as file:
                        file.write(str(stderr.decode()))
                        wrror = await message.reply_document(
                            document=out_file,
                            force_document=True,
                            quote=True,
                            caption="`ffmpeg error`",
                        )
                    os.remove(out_file)
                else:
                    wrror = await message.reply(stderr.decode(), quote=True)
                WORKING.clear()
                try:
                    os.remove(dl)
                except Exception:
                    await wrror.reply("**Reason:** Download Cancelled!")
                await xxx.edit(f"🔺 **Encoding of** `{bb2}` **Failed**")
                if LOG_CHANNEL:
                    await wak.delete()
                return await nn.delete()
        except BaseException:
            er = traceback.format_exc()
            LOGS.info(er)
            LOGS.info(stderr.decode)
        ees = dt.now()
        ttt = time.time()
        try:
            await nn.delete()
            await wak.delete()
        except Exception:
            pass
        nnn = await xxx.edit("`▲ Uploading ▲`")
        fname = out.split("/")[1]
        pcap = await custcap(name, fname)
        ds = await upload2(app, message.from_user.id, out, nnn, thum, pcap)
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
        os.system("rm -rf thumb2.jpg")
        os.remove(dl)
        os.remove(out)
        WORKING.clear()
    except BaseException as er:
        ers = traceback.format_exc()
        LOGS.info(er)
        LOGS.info(ers)
        WORKING.clear()
