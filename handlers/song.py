import os
import aiohttp
import asyncio
import json
import sys
import time
from youtubesearchpython import SearchVideos
from pyrogram import filters, Client
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

@Client.on_message(filters.command("song") & ~filters.edited)
async def song(client, message):
    cap = "🎸 𝑻𝒉𝒊𝒔 𝒊𝒔 𝒀𝒐𝒖𝒓 ♪ 𝑺𝒐𝒏𝒈 𝑼𝒑𝒍𝒐𝒂𝒅𝒆𝒅 𝑩𝒚 𝑴𝒚 𝑶𝒘𝒏𝒆𝒓 [𝑨𝒅𝒊𝒕𝒚𝒂](https://t.me/AdityaHalder)."
    url = message.text.split(None, 1)[1]
    rkp = await message.reply("🔎 𝑺𝒆𝒂𝒓𝒄𝒉𝒊𝒏𝒈 𝒀𝒐𝒖𝒓 𝑺𝒐𝒏𝒈 ...")
    if not url:
        await rkp.edit("❎ 𝐍𝐨𝐭𝐡𝐢𝐧𝐠 𝐅𝐨𝐮𝐧𝐝, 𝐓𝐫𝐲 𝐀𝐧𝐨𝐭𝐡𝐞𝐫 𝐊𝐞𝐲𝐰𝐨𝐫𝐝 𝐎𝐫 𝐒𝐩𝐞𝐥𝐥 𝐈𝐭 𝐏𝐫𝐨𝐩𝐞𝐫𝐥𝐲...")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except BaseException:
        return await rkp.edit("❎ 𝐍𝐨𝐭𝐡𝐢𝐧𝐠 𝐅𝐨𝐮𝐧𝐝, 𝐓𝐫𝐲 𝐀𝐧𝐨𝐭𝐡𝐞𝐫 𝐊𝐞𝐲𝐰𝐨𝐫𝐝 𝐎𝐫 𝐒𝐩𝐞𝐥𝐥 𝐈𝐭 𝐏𝐫𝐨𝐩𝐞𝐫𝐥𝐲...")
    type = "audio"
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        song = True
    try:
        await rkp.edit("📥 𝑫𝒐𝒘𝒏𝒍𝒐𝒂𝒅𝒊𝒏𝒈 𝒀𝒐𝒖𝒓 𝑺𝒐𝒏𝒈 ...")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await rkp.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await rkp.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await rkp.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await rkp.edit("👉 𝑨𝒏𝒐𝒕𝒉𝒆𝒓 𝑫𝒐𝒘𝒏𝒍𝒐𝒂𝒅 𝒊𝒏 𝑷𝒓𝒐𝒈𝒓𝒆𝒔𝒔, 𝑷𝒍𝒆𝒂𝒔𝒆 𝑻𝒓𝒚 𝑨𝒈𝒂𝒊𝒏 𝑨𝒇𝒕𝒆𝒓 𝑺𝒐𝒎𝒆𝒕𝒊𝒎𝒆.")
        return
    except PostProcessingError:
        await rkp.edit("👉 𝑺𝒘𝒂𝒓𝒈 𝑺𝒆𝒓𝒗𝒆𝒓 𝒊𝒔 𝒊𝒏 𝑴𝒂𝒊𝒏𝒕𝒂𝒊𝒏𝒄𝒆 𝑴𝒐𝒅𝒆, 𝑷𝒍𝒆𝒂𝒔𝒆 𝑪𝒐𝒎𝒆 𝑩𝒂𝒄𝒌 𝑳𝒂𝒕𝒆𝒓.")
        return
    except UnavailableVideoError:
        await rkp.edit("👉 𝑴𝒆𝒅𝒊𝒂 𝒊𝒔 𝑵𝒐𝒕 𝑨𝒗𝒂𝒊𝒍𝒂𝒃𝒍𝒆 𝒊𝒏 𝑻𝒉𝒆 𝑹𝒆𝒒𝒖𝒆𝒔𝒕𝒆𝒅 𝑭𝒐𝒓𝒎𝒂𝒕, 𝑻𝒓𝒚 𝑨𝒏𝒐𝒕𝒉𝒆𝒓.")
        return
    except XAttrMetadataError as XAME:
        await rkp.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await rkp.edit("👉 𝑻𝒉𝒆𝒓𝒆 𝑾𝒂𝒔 𝑨𝒏 𝑬𝒓𝒓𝒐𝒓 𝑫𝒖𝒓𝒊𝒏𝒈... 𝑰𝒏𝒇𝒐 𝑬𝒙𝒕𝒓𝒂𝒄𝒕𝒊𝒐𝒏, 𝑻𝒓𝒚 𝑨𝒏𝒐𝒕𝒉𝒆𝒓.")
        return
    except Exception as e:
        await rkp.edit(f"{str(type(e)): {str(e)}}")
        return
    time.time()
    if song:
        await rkp.edit("📤 𝑼𝒑𝒍𝒐𝒂𝒅𝒊𝒏𝒈 𝒀𝒐𝒖𝒓 𝑺𝒐𝒏𝒈 ...") #AdityaHalder
        lol = "./etc/thumb.jpg"
        lel = await message.reply_audio(
                 f"{rip_data['id']}.mp3",
                 duration=int(rip_data["duration"]),
                 title=str(rip_data["title"]),
                 performer=str(rip_data["uploader"]),
                 thumb=lol,
                 caption=cap)
        await rkp.delete()
