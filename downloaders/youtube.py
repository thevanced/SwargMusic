from os import path

from youtube_dl import YoutubeDL

from config import BOT_NAME as bn, DURATION_LIMIT
from helpers.errors import DurationLimitError

ydl_opts = {
    "format": "bestaudio/best",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)


def download(url: str) -> str:
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 60)

    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"❌ 𝐒𝐨𝐫𝐫𝐲 𝐒𝐨𝐧𝐠 𝐋𝐨𝐧𝐠𝐞𝐫 𝐓𝐡𝐚𝐧 {DURATION_LIMIT} 𝐌𝐢𝐧𝐮𝐭𝐞𝐬 𝐀𝐫𝐞 𝐍𝐨𝐭 𝐀𝐥𝐥𝐨𝐰𝐞𝐝, 𝐘𝐨𝐮𝐫 𝐏𝐫𝐨𝐯𝐢𝐝𝐞𝐝 𝐒𝐨𝐧𝐠 𝐢𝐬 {duration} 𝐌𝐢𝐧𝐮𝐭𝐞𝐬..."
        )

    ydl.download([url])
    return path.join("downloads", f"{info['id']}.{info['ext']}")
