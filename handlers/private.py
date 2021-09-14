from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_NAME as bn, BOT_OWNER
from helpers.filters import other_filters2


@Client.on_message(other_filters2)
async def start(_, message: Message):
    await message.reply_text(
        f"""👋 𝐇𝐞𝐥𝐥𝐨 𝐈 𝐀𝐦 𝐀𝐧 𝐒𝐮𝐩𝐞𝐫𝐟𝐚𝐬𝐭 𝐏𝐫𝐞𝐦𝐢𝐮𝐦
𝐌𝐮𝐬𝐢𝐜 𝐏𝐥𝐚𝐲𝐞𝐫 𝐑𝐨𝐛𝐨𝐭 𝐅𝐨𝐫 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐕𝐂
(𝑽𝒐𝒊𝒄𝒆 𝑪𝒉𝒂𝒕), 𝐓𝐨 𝐏𝐥𝐚𝐲 𝐌𝐮𝐬𝐢𝐜 𝐀𝐝𝐝 𝐌𝐞 &
𝐌𝐲 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐀𝐧𝐝 𝐌𝐚𝐤𝐞 𝐀𝐝𝐦𝐢𝐧.

💥 𝐄𝐧𝐣𝐨𝐲 𝐒𝐮𝐩𝐞𝐫𝐟𝐚𝐬𝐭 𝐚𝐧𝐝 𝐇𝐢𝐠𝐡 𝐐𝐮𝐚𝐥𝐢𝐭𝐲
𝐍𝐨 𝐋𝐚𝐠 𝐕𝐢𝐏 𝐌𝐮𝐬𝐢𝐜 𝐢𝐧 𝐆𝐫𝐨𝐮𝐩 𝐕𝐂.

        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 ➕", url="https://t.me/swargrobot?startgroup=true")
                  ],[
                    InlineKeyboardButton(
                        "🌐 𝐔𝐩𝐝𝐚𝐭𝐞𝐬 🌐", url="https://t.me/swargofficial"
                    ),
                    InlineKeyboardButton(
                        "💬 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 💬", url="https://t.me/swargworld"
                    )    
                ],[ 
                    InlineKeyboardButton(
                        "🤖 𝐌𝐲 ♪ 𝐎𝐰𝐧𝐞𝐫 🤖", url=f"https://t.me/{BOT_OWNER}"
                    )]
            ]
        ),
     disable_web_page_preview=True
    )

@Client.on_message(filters.command("start") & ~filters.private & ~filters.channel)
async def gstart(_, message: Message):
      await message.reply_text("""🤖 𝐒𝐰𝐚𝐫𝐠 𝐑𝐨𝐛𝐨𝐭 𝐢𝐬 𝐎𝐧𝐥𝐢𝐧𝐞 🤖""",
      reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💥 𝐂𝐥𝐢𝐜𝐤 𝐇𝐞𝐫𝐞 𝐅𝐨𝐫 𝐌𝐨𝐫𝐞 𝐈𝐧𝐟𝐨 🔥", url="https://t.me/swargrobot")
                ]
            ]
        )
   )
