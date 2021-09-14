import os
from os import path
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from callsmusic import callsmusic, queues
from callsmusic.callsmusic import client as USER
from helpers.admins import get_administrators
import requests
import aiohttp
import youtube_dl
from youtube_search import YoutubeSearch
import converter
from downloaders import youtube
from config import DURATION_LIMIT
from helpers.filters import command
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
import aiofiles
import ffmpeg
from PIL import Image, ImageFont, ImageDraw


def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 32)
    draw.text((190, 550), f"Title: {title}", (255, 255, 255), font=font)
    draw.text(
        (190, 590), f"Duration: {duration}", (255, 255, 255), font=font
    )
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text((190, 670),
        f"Added By: {requested_by}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")




@Client.on_message(command("play") 
                   & filters.group
                   & ~filters.edited 
                   & ~filters.forwarded
                   & ~filters.via_bot)
async def play(_, message: Message):

    lel = await message.reply("🔄 𝑷𝒓𝒐𝒄𝒄𝒆𝒔𝒔𝒊𝒏𝒈 ...")
    
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "𝐒𝐖𝐀𝐑𝐆 💐⃝🌹 𝐌𝐔𝐒𝐈𝐂"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "🤖 𝐀𝐭 𝐅𝐢𝐫𝐬𝐭 𝐌𝐚𝐤𝐞 𝐌𝐞 𝐀𝐝𝐦𝐢𝐧 𝐢𝐧 𝐓𝐡𝐢𝐬 𝐆𝐫𝐨𝐮𝐩.")
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "🤖 𝐒𝐰𝐚𝐫𝐠 𝐌𝐮𝐬𝐢𝐜 (𝑨𝒔𝒔𝒊𝒂𝒕𝒂𝒏𝒕 𝑼𝒔𝒆𝒓𝒃𝒐𝒕) 𝐉𝐨𝐢𝐧𝐞𝐝 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 ❗️")

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"🤖 𝐅𝐥𝐨𝐨𝐝 𝐄𝐫𝐫𝐨𝐫 - 𝐌𝐚𝐧𝐮𝐚𝐥𝐥𝐲 𝐀𝐝𝐝 𝐒𝐰𝐚𝐫𝐠 𝐌𝐮𝐬𝐢𝐜 (𝑨𝒔𝒔𝒊𝒂𝒕𝒂𝒏𝒕 𝑼𝒔𝒆𝒓𝒃𝒐𝒕) 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 𝐎𝐫 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐓𝐨 𝐌𝐮𝐬𝐢𝐜 𝐁𝐨𝐭 𝐎𝐰𝐧𝐞𝐫 ...")
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"🤖 𝐒𝐰𝐚𝐫𝐠 𝐌𝐮𝐬𝐢𝐜 (𝑨𝒔𝒔𝒊𝒂𝒕𝒂𝒏𝒕 𝑼𝒔𝒆𝒓𝒃𝒐𝒕) 𝐍𝐨𝐭 𝐢𝐧 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 ...\n𝐏𝐥𝐞𝐚𝐬𝐞 𝐀𝐝𝐝 𝐌𝐚𝐧𝐮𝐚𝐥𝐥𝐲 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 𝐎𝐫 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐓𝐨 𝐌𝐮𝐬𝐢𝐜 𝐁𝐨𝐭 𝐎𝐰𝐧𝐞𝐫 ...")
        return
    
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ 𝐒𝐨𝐫𝐫𝐲 𝐒𝐨𝐧𝐠 𝐋𝐨𝐧𝐠𝐞𝐫 𝐓𝐡𝐚𝐧 {DURATION_LIMIT} 𝐌𝐢𝐧𝐮𝐭𝐞𝐬 𝐀𝐫𝐞 𝐍𝐨𝐭 𝐀𝐥𝐥𝐨𝐰𝐞𝐝."
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/5b3c5f37b756df9a4bcb2.png"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "𝑳𝒐𝒄𝒂𝒍𝒍𝒚 𝑨𝒅𝒅𝒆𝒅"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="🎭 𝐉𝐨𝐢𝐧 𝐇𝐞𝐫𝐞 𝐚𝐧𝐝 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 🔥", url=f"https://t.me/swargworld")
                   
                ]
            ]
        )
        
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")
            
            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60
                
            keyboard = InlineKeyboardMarkup(
                [
                    [
                    InlineKeyboardButton(text="🎭 𝐉𝐨𝐢𝐧 𝐇𝐞𝐫𝐞 𝐚𝐧𝐝 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 🔥", url=f"https://t.me/swargworld")
                   
                   ]
                ]
            )
        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/5b3c5f37b756df9a4bcb2.png"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                    [
                        [
                    InlineKeyboardButton(text="🎭 𝐉𝐨𝐢𝐧 𝐇𝐞𝐫𝐞 𝐚𝐧𝐝 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 🔥", url=f"https://t.me/swargworld")
                   
                ]
                    ]
                )
        if (dur / 60) > DURATION_LIMIT:
             await lel.edit(f"❌ 𝐒𝐨𝐫𝐫𝐲 𝐒𝐨𝐧𝐠 𝐋𝐨𝐧𝐠𝐞𝐫 𝐓𝐡𝐚𝐧 {DURATION_LIMIT} 𝐌𝐢𝐧𝐮𝐭𝐞𝐬 𝐀𝐫𝐞 𝐍𝐨𝐭 𝐀𝐥𝐥𝐨𝐰𝐞𝐝.")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)     
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit("❎ 𝐍𝐨𝐭𝐡𝐢𝐧𝐠 𝐅𝐨𝐮𝐧𝐝, 𝐓𝐫𝐲 𝐀𝐧𝐨𝐭𝐡𝐞𝐫 𝐊𝐞𝐲𝐰𝐨𝐫𝐝 𝐎𝐫 𝐒𝐩𝐞𝐥𝐥 𝐈𝐭 𝐏𝐫𝐨𝐩𝐞𝐫𝐥𝐲 ...")
        await lel.edit("🔎 𝑺𝒆𝒂𝒓𝒄𝒉𝒊𝒏𝒈 ...")
        query = message.text.split(None, 1)[1]
        # print(query)
        await lel.edit("🔄 𝑷𝒓𝒐𝒄𝒆𝒔𝒔𝒊𝒏𝒈 ...")
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60
                
        except Exception as e:
            await lel.edit(
                "❎ 𝐍𝐨𝐭𝐡𝐢𝐧𝐠 𝐅𝐨𝐮𝐧𝐝, 𝐓𝐫𝐲 𝐀𝐧𝐨𝐭𝐡𝐞𝐫 𝐊𝐞𝐲𝐰𝐨𝐫𝐝 𝐎𝐫 𝐒𝐩𝐞𝐥𝐥 𝐈𝐭 𝐏𝐫𝐨𝐩𝐞𝐫𝐥𝐲 ..."
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
                [
                    [
                    InlineKeyboardButton(text="🎭 𝐉𝐨𝐢𝐧 𝐇𝐞𝐫𝐞 𝐚𝐧𝐝 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 🔥", url=f"https://t.me/swargworld")
                   
                ]
                ]
            )
        
        if (dur / 60) > DURATION_LIMIT:
             await lel.edit(f"❌ 𝐒𝐨𝐫𝐫𝐲 𝐒𝐨𝐧𝐠 𝐋𝐨𝐧𝐠𝐞𝐫 𝐓𝐡𝐚𝐧 {DURATION_LIMIT} 𝐌𝐢𝐧𝐮𝐭𝐞𝐬 𝐀𝐫𝐞 𝐍𝐨𝐭 𝐀𝐥𝐥𝐨𝐰𝐞𝐝.")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(youtube.download(url))
  
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo="final.png", 
        caption="#️⃣ 𝐑𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐒𝐨𝐧𝐠 𝐐𝐮𝐞𝐮𝐞𝐝 𝐀𝐭 𝐏𝐨𝐬𝐢𝐭𝐢𝐨𝐧 - {}".format(
         position
        ),
        reply_markup=keyboard)
        os.remove("final.png")
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
        photo="final.png",
        reply_markup=keyboard,
        caption="▶️ 𝐒𝐰𝐚𝐫𝐠 𝐌𝐮𝐬𝐢𝐜 𝐍𝐨𝐰 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 ... 𝐀𝐭 - **{}**".format(
        message.chat.title
        ), )
        os.remove("final.png")
        return await lel.delete()
