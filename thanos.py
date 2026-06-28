import os, time, asyncio, subprocess, aiohttp, aiofiles, logging
from utils import progress_bar

logger = logging.getLogger(__name__)

def duration(filename):
    try:
        result = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=10)
        return float(result.stdout) if result.stdout else 0
    except: return 0

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

async def pdf_download(api_url, output_file):
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(output_file, "wb")
                await f.write(await resp.read())
                await f.close()
                return True
    return False

async def download_video(url, cmd, name):
    download_cmd = f'{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args "aria2c: -x 16 -j 32"'
    logger.info(f"Running: {download_cmd}")
    for attempt in range(10):
        proc = subprocess.run(download_cmd, shell=True)
        if proc.returncode == 0: break
        await asyncio.sleep(5)
    else:
        raise RuntimeError("Download failed after 10 retries")
    for ext in [".mp4", ".mkv", ".webm"]:
        if os.path.isfile(f"{name}{ext}"):
            return f"{name}{ext}"
    raise FileNotFoundError(f"No output file for {name}")

async def send_vid(bot, m, caption, filename, thumb, name, prog_msg, channel_id, watermark="/d"):
    if thumb == "no" or thumb == "/d":
        thumb_file = f"{filename}.jpg"
        subprocess.run(f'ffmpeg -i "{filename}" -ss 00:01:00 -vframes 1 "{thumb_file}"', shell=True, stderr=subprocess.DEVNULL)
        thumb = thumb_file if os.path.isfile(thumb_file) else None
    else:
        thumb = thumb if os.path.isfile(thumb) else None
    await prog_msg.delete()
    reply_msg = await bot.send_message(channel_id, f"**Uploading...** `{name}`")
    dur = int(duration(filename))
    start = time.time()
    try:
        await bot.send_video(chat_id=channel_id, video=filename, caption=caption, supports_streaming=True, width=1280, height=720, thumb=thumb, duration=dur, progress=progress_bar, progress_args=(reply_msg, start))
    except Exception as e:
        logger.error(f"Video upload failed: {e}")
        await bot.send_document(chat_id=channel_id, document=filename, caption=caption, progress=progress_bar, progress_args=(reply_msg, start))
    if os.path.exists(filename): os.remove(filename)
    if thumb and thumb != "no" and thumb != "/d" and os.path.exists(thumb): os.remove(thumb)
    await reply_msg.delete()

async def download_and_decrypt_video(url, cmd, name, appxkey):
    # Implement decryption if needed, otherwise just download
    return await download_video(url, cmd, name)

async def decrypt_and_merge_video(mpd, keys_string, path, name, quality):
    # Implement DRM decryption if needed, otherwise just download
    cmd = f'yt-dlp -f "bestvideo[height<={quality}]+bestaudio" "{mpd}" -o "{name}.mp4"'
    return await download_video(mpd, cmd, name)

def get_mps_and_keys(url):
    # Replace with actual API call if needed
    return url, []
