import time
from pyrogram.errors import FloodWait
from datetime import timedelta

class Timer:
    def __init__(self, interval=5):
        self.interval = interval
        self.last = time.time()
    def can_send(self):
        now = time.time()
        if now - self.last >= self.interval:
            self.last = now
            return True
        return False

def hrb(size, digits=2):
    if size is None:
        return "0 B"
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    idx = 0
    while size > 1024 and idx < len(units)-1:
        size /= 1024
        idx += 1
    return f"{size:.{digits}f} {units[idx]}"

def hrt(seconds):
    if seconds < 60:
        return f"{int(seconds)}s"
    minutes, seconds = divmod(int(seconds), 60)
    if minutes < 60:
        return f"{minutes}m {seconds}s"
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes}m"

timer = Timer()

async def progress_bar(current, total, reply, start):
    if not timer.can_send():
        return
    now = time.time()
    elapsed = now - start
    if elapsed < 1:
        return
    percent = current * 100 / total
    speed = current / elapsed
    eta = (total - current) / speed if speed > 0 else 0
    bar_length = 20
    filled = int(current * bar_length / total)
    bar = "■" * filled + "□" * (bar_length - filled)
    text = (
        f"╭─⌈ 📤 Uploading 📤 ⌋\n"
        f"├ {bar} {percent:.1f}%\n"
        f"├ 🚀 Speed: {hrb(speed)}/s\n"
        f"├ 📟 Processed: {hrb(current)}\n"
        f"├ 🧲 Size: {hrb(total)} | ETA: {hrt(eta)}\n"
        f"╰─ 🤖 Powered by DRM Wizard"
    )
    try:
        await reply.edit(text)
    except FloodWait as e:
        time.sleep(e.x)
