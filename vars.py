import os
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ---- Environment Variables ----
API_ID = int(os.getenv("API_ID", 34422904))
API_HASH = os.getenv("API_HASH", "7e0002469784f47fc08a6b3d93d7ebed")
BOT_TOKEN = os.getenv("BOT_TOKEN", "863839853AAGd0NJg0MEGbY2Zx7d1RHF8z6gaZ5PVo4")
OWNER_ID = int(os.getenv("OWNER_ID", 5349573682))
SUDO_USERS = [int(x) for x in os.getenv("SUDO_USERS", "5349573682").replace(",", " ").split() if x]

# ---- Bot Credentials & Tokens ----
CREDIT = os.getenv("CREDIT", "Krishna Bot")
cptoken = os.getenv("CPTOKEN", "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJpZCI6MzgzNjkyMTIsIm9yZ0lkIjoyNjA1LCJ0eXBlIjoxLCJtb2JpbGUiOiI5MTcwODI3NzQyODkiLCJuYW1lIjoiQWNlIiwiZW1haWwiOm51bGwsImlzRmlyc3RMb2dpbiI6dHJ1ZSwiZGVmYXVsdExhbmd1YWdlIjpudWxsLCJjb3VudHJ5Q29kZSI6IklOIiwiaXNJbnRlcm5hdGlvbmFsIjowLCJpYXQiOjE2NDMyODE4NzcsImV4cCI6MTY0Mzg4NjY3N30.hM33P2ai6ivdzxPPfm01LAd4JWv-vnrSxGXqvCirCSpUfhhofpeqyeHPxtstXwe0")
cwtoken = os.getenv("CWTOKEN", "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3NTExOTcwNjQsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiVWtoeVRtWkhNbXRTV0RjeVJIcEJUVzExYUdkTlp6MDkiLCJmaXJzdF9uYW1lIjoiVWxadVFXaFBaMnAwSzJsclptVXpkbGxXT0djMlREWlRZVFZ5YzNwdldXNXhhVEpPWjFCWFYyd3pWVDA9IiwiZW1haWwiOiJWSGgyWjB0d2FUZFdUMVZYYmxoc2FsZFJSV2xrY0RWM2FGSkRSU3RzV0c5M1pDOW1hR0kxSzBOeVRUMD0iLCJwaG9uZSI6IldGcFZSSFZOVDJFeGNFdE9Oak4zUzJocmVrNHdRVDA5IiwiYXZhdGFyIjoiSzNWc2NTOHpTMHAwUW5sa2JrODNSRGx2ZWtOaVVUMDkiLCJyZWZlcnJhbF9jb2RlIjoiWkdzMlpUbFBORGw2Tm5OclMyVTRiRVIxTkVWb1FUMDkiLCJkZXZpY2VfdHlwZSI6ImFuZHJvaWQiLCJkZXZpY2VfdmVyc2lvbiI6IlEoQW5kcm9pZCAxMC4wKSIsImRldmljZV9tb2RlbCI6IlhpYW9taSBNMjAwN0oyMENJIiwicmVtb3RlX2FkZHIiOiI0NC4yMDIuMTkzLjIyMCJ9fQ.ONBsbnNwCQQtKMK2h18LCi73e90s2Cr63ZaIHtYueM-Gt5Z4sF6Ay-SEaKaIf1ir9ThflrtTdi5eFkUGIcI78R1stUUch_GfBXZsyg7aVyH2wxm9lKsFB2wK3qDgpd0NiBoT-ZsTrwzlbwvCFHhMp9rh83D4kZIPPdbp5yoA_06L0Zr4fNq3S328G8a8DtboJFkmxqG2T1yyVE2wLIoR3b8J3ckWTlT_VY2CCx8RjsstoTrkL8e9G5ZGa6sksMb93ugautin7GKz-nIz27pCr0h7g9BCoQWtL69mVC5xvVM3Z324vo5uVUPBi1bCG-ptpD9GWQ4exOBk9fJvGo-vRg")
api_url = os.getenv("API_URL", "http://master-api-v3.vercel.app/")
api_token = os.getenv("API_TOKEN", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzkxOTMzNDE5NSIsInRnX3VzZXJuYW1lIjoi4p61IFtvZmZsaW5lXSIsImlhdCI6MTczODY5MjA3N30.SXzZ1MZcvMp5sGESj0hBKSghhxJ3k1GTWoBUbivUe1I")

# ---- Images ----
photologo = os.getenv("PHOTOLOGO", "https://envs.sh/Nf.jpg/IMG20250803704.jpg")
photoyt = os.getenv("PHOTOYT", "https://tinypic.host/images/2025/03/18/YouTube-Logo.wine.png")
photocp = os.getenv("PHOTOCP", "https://tinypic.host/images/2025/03/28/IMG_20250328_133126.jpg")
photozip = os.getenv("PHOTOZIP", "https://envs.sh/fH.jpg/IMG20250803719.jpg")

# ---- Cookies ----
cookies_file_path = os.getenv("cookies_file_path", "youtube_cookies.txt")

# ---- Keyboard ----
KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("📞 Contact", url="https://t.me/MrFrontMa1")]
])
