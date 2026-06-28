import os
import time
import asyncio
import subprocess
import aiohttp
import aiofiles
import logging
import yt_dlp
from utils import progress_bar
from pyrogram.types import Message

logger = logging.getLogger(__name__)

# ---------- Duration ----------
def duration(filename):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", filename],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=10
        )
        return float(result.stdout) if result.stdout else 0
    except:
        return 0

# ---------- PDF Download (simple) ----------
async def download(url, name):
    filename = f"{name}.pdf"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(filename, "wb")
                await f.write(await resp.read())
                await f.close()
                return filename
    return None

# ---------- PDF Download via API (for .ws) ----------
async def pdf_download(api_url, output_file):
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(output_file, "wb")
                await f.write(await resp.read())
                await f.close()
                return True
    return False

# ---------- Video Download (yt-dlp) ----------
async def download_video(url, cmd, name):
    # cmd already contains yt-dlp command with output template
    download_cmd = f'{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args "aria2c: -x 16 -j 32"'
    logger.info(f"Running: {download_cmd}")
    for attempt in range(10):
        proc = subprocess.run(download_cmd, shell=True)
        if proc.returncode == 0:
            break
        logger.warning(f"Retry {attempt+1}/10")
        await asyncio.sleep(5)
    else:
        raise RuntimeError("Download failed after 10 retries")

    # Check possible output extensions
    for ext in [".mp4", ".mkv", ".webm"]:
        if os.path.isfile(f"{name}{ext}"):
            return f"{name}{ext}"
    raise FileNotFoundError(f"No output file found for {name}")

# ---------- Send Video (with thumbnail) ----------
async def send_vid(bot, m, caption, filename, thumb, name, prog_msg, channel_id, watermark="/d"):
    # Generate thumbnail if not provided
    if thumb == "no" or thumb == "/d":
        thumb_file = f"{filename}.jpg"
        subprocess.run(
            f'ffmpeg -i "{filename}" -ss 00:01:00 -vframes 1 "{thumb_file}"',
            shell=True, stderr=subprocess.DEVNULL
        )
        thumb = thumb_file if os.path.isfile(thumb_file) else None
    else:
        thumb = thumb if os.path.isfile(thumb) else None

    await prog_msg.delete()
    reply_msg = await bot.send_message(channel_id, f"**Uploading...** `{name}`")
    dur = int(duration(filename))
    start = time.time()

    try:
        await bot.send_video(
            chat_id=channel_id,
            video=filename,
            caption=caption,
            supports_streaming=True,
            width=1280,
            height=720,
            thumb=thumb,
            duration=dur,
            progress=progress_bar,
            progress_args=(reply_msg, start)
        )
    except Exception as e:
        logger.error(f"Video upload failed: {e}")
        await bot.send_document(
            chat_id=channel_id,
            document=filename,
            caption=caption,
            progress=progress_bar,
            progress_args=(reply_msg, start)
        )

    # Cleanup
    if os.path.exists(filename):
        os.remove(filename)
    if thumb and thumb != "no" and thumb != "/d" and os.path.exists(thumb):
        os.remove(thumb)
    await reply_msg.delete()

# ---------- DRM / Encrypted Video (AppX) ----------
async def download_and_decrypt_video(url, cmd, name, appxkey):
    """
    डिक्रिप्ट करके वीडियो डाउनलोड करें (AppX encrypted).
    यहाँ हम सिर्फ yt-dlp से डाउनलोड कर रहे हैं – आप चाहें तो अपनी डिक्रिप्शन लॉजिक यहाँ डालें.
    """
    # If you have decryption logic, implement here.
    # For now, we just download the video as is.
    return await download_video(url, cmd, name)

# ---------- DRM MPD + Keys ----------
async def decrypt_and_merge_video(mpd, keys_string, path, name, quality):
    """
    MPD और keys का उपयोग करके डिक्रिप्ट करें और मर्ज करें.
    यहाँ हम yt-dlp से डाउनलोड कर रहे हैं – अगर आपके पास keys हैं तो आप shaka-packager या ffmpeg का उपयोग कर सकते हैं.
    """
    # Simple approach: download with yt-dlp (it may handle some DRM)
    cmd = f'yt-dlp -f "bestvideo[height<={quality}]+bestaudio" "{mpd}" -o "{name}.mp4"'
    return await download_video(mpd, cmd, name)

# ---------- Get MPD and Keys from API ----------
def get_mps_and_keys(url):
    """
    API से MPD URL और keys प्राप्त करें.
    यहाँ हम सिर्फ URL को ही लौटा रहे हैं – आप अपनी API लॉजिक यहाँ डालें.
    """
    # Placeholder – replace with actual API call if needed.
    # For now, return the same URL and an empty keys list.
    return url, []
