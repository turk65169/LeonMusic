# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam

import os
import random
import asyncio
import re
import yt_dlp
from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from KumsalTR import app, db, lang, logger, config, yt

# Active quizzes: {chat_id: {round_data...}}
QUIZ_STATE: dict[int, dict] = {}

TR_POP = [
    ("Mabel Matiz - Sarışın", "WYSnXJYFfTg"),
    ("Semicenk - Pişman Değilim", "U8n6x1G1h_Y"),
    ("Tarkan - Kuzu Kuzu", "G7LN-Y-R3GY"),
    ("Sezen Aksu - Geri Dön", "WRbfRZCvCHs"),
    ("Barış Manço - Gülpembe", "Hpt3lS_6vIc"),
    ("Teoman - İstanbul'da Sonbahar", "J6IOMvSvKyU"),
    ("Mor ve Ötesi - Cambaz", "w4j3h6c738U"),
    ("Manga - Dursun Zaman", "HhrY23GQEBU"),
    ("Simge - Yankı", "v31e6S-c3CA"),
    ("Edis - Çok Çok", "H-RgAqgqLNA"),
    ("Hadise - Düm Tek Tek", "LVMqyiUGBXQ"),
    ("Zeynep Bastık - Felaket", "U2dyjNNWW3U"),
    ("Gülşen - Bangır Bangır", "3I8I0XmxKqs"),
    ("Kenan Doğulu - Shake It Up Şekerim", "p-TdmLKL4Ck"),
    ("Mabel Matiz & Mert Demir - Antidepresan", "J51o4d9o6gE"),
    ("Zeynep Bastık - Lan", "-O22D3EV6G0"),
    ("Simge - Aşkın Olayım", "VREnTCTeS4k"),
    ("Sefo - Bilmem Mi", "w3h_n1l3m2I"),
    ("Mert Demir - Ateşe Düştüm", "lXv3lK-1y8o"),
    ("Melike Şahin - Pusulam Rüzgar", "fW5PqN2m94o"),
    ("Köfn - Bir Tek Ben Anlarım", "6g6W4p6W-H4"),
    ("Semicenk - Canın Sağ Olsun", "7L9_Z8W3Y6G"),
    ("Emir Can İğrek - Ali Cabbar", "U8V-W9Y6Z8H"),
    ("Kardelen - Narin", "W8V-Z9H3Y6G"),
    ("Derya Uluğ - Yansıma", "8G-Y9H6W3Z2"),
    ("Hande Yener - Benden Sonra", "6G-W3Z2Y9H6"),
    ("İrem Derici - Kalbimin Tek Sahibine", "Y-W3Z2G6H98"),
    ("Murat Boz - Janti", "8G-Y6W3V9U7"),
    ("Ajda Pekkan - Yakar Geçerim", "7F-W3Z2G9S1"),
    ("Serdar Ortaç - Poşet", "8G-S9V3W2G1"),
    ("Demet Akalın - Türkan", "7V-Z9H6S3W2"),
    ("Mustafa Sandal - Araba", "6G-V9U7W3Z2"),
]

TR_ARABESK = [
    ("Müslüm Gürses - Nilüfer", "tF_1YKkISRo"),
    ("Ahmet Kaya - Kum Gibi", "f3dA8x6gE90"),
    ("İbrahim Tatlıses - Haydi Söyle", "YcR5Fm5M7pY"),
    ("Ebru Gündeş - Araftayım", "7KjM4b5N9R0"),
    ("Orhan Gencebay - Batsın Bu Dünya", "JkP6T5O7wL4"),
    ("Bergen - Sen Ağlama", "IeJ6R3N4M8U"),
    ("Hakan Altun - Telefonun Başında", "KfH4M9wQ8R0"),
    ("Müslüm Gürses - Affet", "gM9V4G_eF_0"),
    ("Azer Bülbül - Çoğu Gitti Azı Kaldı", "x459c5d0m7U"),
    ("Cengiz Kurtoğlu - Hain Geceler", "1y1f12P8xG0"),
    ("Ferdi Tayfur - Huzurum Kalmadı", "8G_9Q4tM12Q"),
    ("Kibariye - Sil Baştan", "W9V-Z8G3H6Q"),
    ("Hakan Altun - Hani Bekleyecektin", "8G-Z9H3V6W2"),
    ("Yıldız Tilbe - Delikanlım", "7V-G9S3W6Z1"),
    ("Sibel Can - Padişah", "8G-Z9V3S1W6"),
]

TR_ROCK = [
    ("Madrigal - Seni Dert Etmeler", "pW-4w9W8o-0"),
    ("Adamlar - Zombi", "0_4lJ_0x8l0"),
    ("Mor ve Ötesi - Bir Derdim Var", "S3Q1M5zG_pU"),
    ("Teoman - Paramparça", "dJ8Gk1w5Z-c"),
    ("Duman - Kufi", "c5409Wd9L98"),
    ("Yüzyüzeyken Konuşuruz - Dinle Beni Bi", "8G-Y9H6S3V1"),
    ("Manga - Cevapsız Sorular", "6G-W3Z2G9S1"),
    ("Şebnem Ferah - Sil Baştan", "7V-Z9H6S3W2"),
    ("Dedublüman - Belki", "8G-V9U7W3Z2"),
    ("Hayko Cepkin - Fırtınam", "7F-W3Z2G9S1"),
]

TR_RAP = [
    ("Ezhel - Deli Mi Ne", "aL9z1v9mI-k"),
    ("Motive - 10MG", "1kS7V9oY-5E"),
    ("Uzi - Arasan da", "V5v9lY8nE-s"),
    ("Çakal - İmdat", "1l5Q9xW2z-s"),
    ("Heijan & Muti - Davay Davay", "8G-Y9H6W3V1"),
    ("Cakal - Lütfen", "7F-W3Z2G9S1"),
    ("Batuflex - Dalga", "6G-W3Z2G9S1"),
    ("Lvbel C5 - Doğuştan Beri", "7V-Z9H6S3W2"),
    ("Block3 - Vur", "8G-V9U7W3Z2"),
    ("Murda - Eh Baba", "7F-W3Z2G9S1"),
]

EN_POP = [
    ("The Weeknd - Blinding Lights", "4NRXx6U4d44"),
    ("Dua Lipa - Levitating", "TUVcZfQe-Kw"),
    ("Harry Styles - As It Was", "H5v3kku4y6Q"),
    ("Sia - Unstoppable", "cxjvTXo9WWM"),
    ("Rihanna - Diamonds", "lWA2pjMjpBs"),
    ("Imagine Dragons - Believer", "7t2MexigGRs"),
    ("Coldplay - Yellow", "yKNxeF4KMsY"),
    ("Linkin Park - In the End", "eVTXPUF4Oz4"),
    ("Eminem - Without Me", "YVkUvmDQ-as"),
    ("Lady Gaga - Bad Romance", "qrO4YZeyl0I"),
    ("Adele - Rolling in the Deep", "rYEDA3JcQqw"),
    ("Billie Eilish - Bad Guy", "DyDfgMOUjCI"),
    ("Drake - One Dance", "qL7zrWcc44c"),
    ("Doja Cat - Say So", "pok8H_KF1FA"),
    ("Post Malone - Circles", "wXhTHyIgQ_U"),
    ("Billie Eilish - Birds of a Feather", "3_qV_42A5Qk"),
    ("Taylor Swift - Anti-Hero", "b1kbLwvqugk"),
    ("Sabrina Carpenter - Espresso", "eVli-tBUBSs"),
    ("Harry Styles - Watermelon Sugar", "E07s5f96T-8"),
    ("Katy Perry - Roar", "CevxZvSJLk8"),
    ("Ed Sheeran - Shape of You", "JGwWNGJdvx8"),
    ("Justin Bieber - Baby", "kffacxfqcws"),
    ("The Kid LAROI & Justin Bieber - STAY", "8G-Y9H6W3V1"),
    ("Lil Nas X - Montero", "7F-W3Z2G9S1"),
    ("Bruno Mars - Uptown Funk", "6G-W3Z2G9S1"),
]

def normalize(text):
    return re.sub(r'[^a-zA-Z0-9]', '', text.lower())

async def get_snippet(name, vid_id=None):
    # Try ID first if provided
    current_url = f"https://www.youtube.com/watch?v={vid_id}" if vid_id else f"ytsearch1:{name}"
    file_tag = vid_id if vid_id else normalize(name)[:10]
    path = f"downloads/quiz_{file_tag}.m4a"

    if os.path.exists(path) and os.path.getsize(path) > 1024:
        return path
    
    start = random.randint(30, 90)
    end = start + 30
    
    format_attempts = [
        "bestaudio[ext=m4a]/bestaudio/best",
        "bestaudio/best",
        "best",
    ]
    
    # Ensure cookies are loaded
    yt.get_cookies()
    cookies = [None] + yt.cookies
    random.shuffle(cookies)

    # User-Agent Rotasyonu
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    ]

    # First attempt: Direct URL (ID or Search)
    async def _try_download(url, tag):
        # Deneme sırası: Cookiesiz -> Kayıtlı çerezler
        attempts = [None] + list(cookies)
        random.shuffle(attempts)

        for cookie in attempts:
            agent = random.choice(user_agents)
            for fmt in format_attempts:
                opts = {
                    "quiet": True,
                    "no_warnings": True,
                    "format": fmt,
                    "outtmpl": f"downloads/quiz_{tag}.%(ext)s",
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "m4a",
                    }],
                    "download_ranges": yt_dlp.utils.download_range_func(None, [(start, end)]),
                    "force_keyframes_at_cuts": True,
                    "cookiefile": cookie,
                    "geo_bypass": True,
                    "nocheckcertificate": True,
                    "http_headers": {
                        "User-Agent": agent,
                        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
                        "Sec-Ch-Ua-Platform": "\"Windows\"",
                    }
                }
                def _dl(_o=opts, _u=url):
                    with yt_dlp.YoutubeDL(_o) as ydl:
                        ydl.download([_u])
                try:
                    await asyncio.wait_for(asyncio.to_thread(_dl), timeout=30)
                    for ext in ["m4a", "mp3", "opus", "webm", "ogg"]:
                        alt = f"downloads/quiz_{tag}.{ext}"
                        if os.path.exists(alt) and os.path.getsize(alt) > 1024:
                            return alt
                except Exception as e:
                    err_str = str(e).lower()
                    if "sign in to confirm" in err_str:
                        if cookie and cookie in yt.cookies:
                            logger.warning(f"Quiz: Bozuk çerez siliniyor: {cookie}")
                            try:
                                yt.cookies.remove(cookie)
                                os.remove(cookie)
                            except: pass
                        break
                    continue
        return None

    # Step 1: Try current_url
    result = await _try_download(current_url, file_tag)
    if result:
        return result

    # Step 2: If we had an ID and it failed, try search as fallback
    if vid_id:
        logger.warning(f"ID {vid_id} failed for {name}, trying search fallback...")
        result = await _try_download(f"ytsearch1:{name}", file_tag)
        return result

    return None

@app.on_message(filters.command(["yarisma"]) & filters.group & ~app.blacklist_filter)
@lang.language()
async def start_quiz_cmd(_, m: types.Message):
    chat_id = m.chat.id
    if chat_id in QUIZ_STATE and QUIZ_STATE[chat_id].get("active"):
        return await m.reply_text(m.lang.get("quiz_started_already", "<b>❌ Bᴜ ɢʀᴜᴘᴛᴀ ᴢᴀᴛᴇɴ ᴀᴋᴛɪғ ʙɪʀ ʏᴀʀɪşᴍᴀ ᴠᴀʀ!</b>"))
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🇹🇷 ᴛᴜ̈ʀᴋᴄ̧ᴇ", callback_data="quiz_lang_tr"),
         InlineKeyboardButton("🌍 ɪ̇ɴɢɪʟɪᴢᴄᴇ", callback_data="quiz_lang_en")],
        [InlineKeyboardButton("❌ ɪ̇ᴘᴛᴀʟ", callback_data="quiz_cancel")]
    ])
    
    text = "🏆 <b>Mᴜ̈ᴢɪᴋ Bɪʟɢɪ Yᴀʀɪşᴍᴀsɪ</b>\n\n👇 <b>Lᴜ̈ᴛғᴇɴ şᴀʀᴋɪ ᴅɪʟɪɴɪ sᴇᴄ̧ɪɴɪᴢ:</b>"
    await m.reply_text(text, reply_markup=keyboard)

@app.on_callback_query(filters.regex(r"^quiz_"))
async def quiz_callback_handler(client, cb: types.CallbackQuery):
    chat_id = cb.message.chat.id
    data = cb.data
    
    if data == "quiz_cancel":
        await cb.message.edit_text("❌ <b>Yᴀʀɪşᴍᴀ ɪᴘᴛᴀʟ ᴇᴅɪʟᴅɪ.</b>")
        return
        
    elif data.startswith("quiz_lang_"):
        lang_sel = data.split("_")[2]
        if lang_sel == "tr":
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🎙 ᴘᴏᴘ", callback_data="quiz_cat_tr_pop"),
                 InlineKeyboardButton("🍺 ᴀʀᴀʙᴇsᴋ", callback_data="quiz_cat_tr_arabesk")],
                [InlineKeyboardButton("🎸 ʀᴏᴄᴋ", callback_data="quiz_cat_tr_rock"),
                 InlineKeyboardButton("🎧 ʀᴀᴘ", callback_data="quiz_cat_tr_rap")],
                [InlineKeyboardButton("⬅️ ɢᴇʀɪ", callback_data="quiz_back_main")]
            ])
            text = "🇹🇷 <b>Tᴜ̈ʀᴋᴄ̧ᴇ Kᴀᴛᴇɢᴏʀɪsɪ</b>\n\n👇 <b>Lᴜ̈ᴛғᴇɴ ᴍᴜ̈ᴢɪᴋ ᴛᴜ̈ʀᴜ̈ɴᴜ̈ sᴇᴄ̧ɪɴ:</b>"
        else:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🎙 ᴘᴏᴘ", callback_data="quiz_cat_en_pop")],
                [InlineKeyboardButton("⬅️ ɢᴇʀɪ", callback_data="quiz_back_main")]
            ])
            text = "🌍 <b>İɴɢɪʟɪᴢᴄᴇ Kᴀᴛᴇɢᴏʀɪsɪ</b>\n\n👇 <b>Lᴜ̈ᴛғᴇɴ ᴍᴜ̈ᴢɪᴋ ᴛᴜ̈ʀᴜ̈ɴᴜ̈ sᴇᴄ̧ɪɴ:</b>"
            
        await cb.message.edit_text(text, reply_markup=keyboard)
        
    elif data == "quiz_back_main":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🇹🇷 ᴛᴜ̈ʀᴋᴄ̧ᴇ", callback_data="quiz_lang_tr"),
             InlineKeyboardButton("🌍 ɪ̇ɴɢɪʟɪᴢᴄᴇ", callback_data="quiz_lang_en")],
            [InlineKeyboardButton("❌ ɪ̇ᴘᴛᴀʟ", callback_data="quiz_cancel")]
        ])
        text = "🏆 <b>Mᴜ̈ᴢɪᴋ Bɪʟɢɪ Yᴀʀɪşᴍᴀsɪ</b>\n\n👇 <b>Lᴜ̈ᴛғᴇɴ şᴀʀᴋɪ ᴅɪʟɪɴɪ sᴇᴄ̧ɪɴɪᴢ:</b>"
        await cb.message.edit_text(text, reply_markup=keyboard)
        
    elif data.startswith("quiz_cat_"):
        parts = data.split("_")
        lang_sel = parts[2]
        cat = parts[3]
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏁 10 ᴛᴜʀ", callback_data=f"quiz_start_{lang_sel}_{cat}_10"),
             InlineKeyboardButton("🏁 20 ᴛᴜʀ", callback_data=f"quiz_start_{lang_sel}_{cat}_20")],
            [InlineKeyboardButton("🏁 30 ᴛᴜʀ", callback_data=f"quiz_start_{lang_sel}_{cat}_30")],
            [InlineKeyboardButton("❌ ɪ̇ᴘᴛᴀʟ", callback_data="quiz_cancel")]
        ])
        text = f"✅ <b>Sᴇᴄ̧ɪᴍ:</b> {lang_sel.upper()} — {cat.upper()}\n\n👇 <b>Kᴀᴄ̧ ᴛᴜʀ ᴏʏɴᴀɴᴀᴄᴀɢɢɪɴɪ sᴇᴄ̧ɪɴ:</b>"
        await cb.message.edit_text(text, reply_markup=keyboard)
        
    elif data.startswith("quiz_start_"):
        if chat_id in QUIZ_STATE and QUIZ_STATE[chat_id].get("active"):
            return await cb.answer("Yᴀʀɪşᴍᴀ ᴢᴀᴛᴇɴ ʙᴀşʟᴀᴛɪʟᴍɪş!", show_alert=True)
            
        parts = data.split("_")
        lang_sel = parts[2]
        cat = parts[3]
        rounds = int(parts[4])
        
        pool = []
        if lang_sel == "tr" and cat == "pop": pool = TR_POP
        elif lang_sel == "tr" and cat == "arabesk": pool = TR_ARABESK
        elif lang_sel == "tr" and cat == "rock": pool = TR_ROCK
        elif lang_sel == "tr" and cat == "rap": pool = TR_RAP
        elif lang_sel == "en" and cat == "pop": pool = EN_POP
        if not pool: pool = TR_POP
        
        try:
            await cb.message.delete()
        except: pass
        
        QUIZ_STATE[chat_id] = {
            "round": 0,
            "max_rounds": rounds,
            "wrong_rounds": 0,
            "scores": {},
            "answer": None,
            "winner_found": asyncio.Event(),
            "active": True,
            "pool": list(pool),
        }
        
        asyncio.create_task(quiz_loop(chat_id))

async def quiz_loop(chat_id):
    state = QUIZ_STATE.get(chat_id)
    if not state: return

    try:
        await app.send_message(chat_id, "<b>⚙️ Yᴀʀɪşᴍᴀ ʜᴀᴢɪʀʟᴀɴɪʏᴏʀ... Şᴀʀᴋɪʟᴀʀ ʏᴜ̈ᴋʟᴇɴɪʏᴏʀ, ʟᴜ̈ᴛғᴇɴ ʙᴇᴋʟᴇʏɪɴ.</b>")
        while state["active"]:
            if state["round"] >= state["max_rounds"]:
                break
            
            if state["wrong_rounds"] >= 5:
                # Arka arkaya kimse bilmediğinde botu yormamak için sonlandır
                try:
                    await app.send_message(chat_id, "<b>🚫 Üsᴛ ᴜ̈sᴛᴇ 5 ᴋᴇᴢ ᴋɪᴍsᴇ ʙɪʟᴇᴍᴇᴅɪ! Yᴀʀɪşᴍᴀ Sᴏɴʟᴀɴᴅɪ.</b>")
                except: pass
                break

            name, vid = random.choice(state["pool"])
            
            # ADIM 1: Önce Snippet İndir (Duplicate mesajları engellemek için)
            snippet = await get_snippet(name, vid)
            
            if not snippet or not os.path.exists(snippet):
                logger.error(f"Quiz snippet failed for {name}, skipping this track.")
                try:
                    await app.send_message(chat_id, f"⚠️ <b>{name}</b> ɪɴᴅɪʀɪʟᴇᴍᴇᴅɪ, ᴀᴛʟᴀɴɪʏᴏʀ... (Bᴏᴛ ᴇɴɢᴇʟɪ ᴠᴇʏᴀ ᴠɪᴅᴇᴏ ᴍᴇᴠᴄᴜᴛ ᴅᴇɢ̆ɪʟ)")
                except: pass
                await asyncio.sleep(2)
                continue
            
            # ADIM 2: Snippet hazır olduktan sonra Turu Başlat
            state["round"] += 1
            state["winner_found"].clear()
            state["answer"] = name
            
            try:
                round_msg = await app.send_message(chat_id, f"🎵 <b>{state['round']}. Tᴜʀ Bᴀşʟᴀᴅɪ!</b>\n\n⌚ <b>30 sᴀɴɪʏᴇɴɪᴢ ᴠᴀʀ!</b>")
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                round_msg = await app.send_message(chat_id, f"🎵 <b>{state['round']}. Tᴜʀ Bᴀşʟᴀᴅɪ!</b>\n\n⌚ <b>30 sᴀɴɪʏᴇɴɪᴢ ᴠᴀʀ!</b>")

            try:
                voice_msg = await app.send_voice(chat_id, snippet)
            except Exception as e:
                logger.error(f"Quiz voice send error: {e}")
                if os.path.exists(snippet): os.remove(snippet)
                continue
            
            # ADIM 3: Kazananı veya Zaman Aşımını Bekle
            try:
                await asyncio.wait_for(state["winner_found"].wait(), timeout=30)
                state["wrong_rounds"] = 0
            except asyncio.TimeoutError:
                if not state["winner_found"].is_set() and state["active"]:
                    state["wrong_rounds"] += 1
                    ans_text = f"❌ <b>Sᴜ̈ʀᴇ ᴅᴏʟᴅᴜ! Kɪᴍsᴇ ʙɪʟᴇᴍᴇᴅɪ.</b>\n\n🎵 <b>Cᴇᴠᴀᴘ:</b> {name}"
                    try:
                        await app.send_message(chat_id, ans_text)
                    except FloodWait as e:
                        await asyncio.sleep(e.value + 1)
                        await app.send_message(chat_id, ans_text)
                    state["answer"] = None
            
            # Temizlik
            if snippet and os.path.exists(snippet):
                try: os.remove(snippet)
                except: pass
                
            # Tur arası bekleme (FloodWait riskini azaltmak için)
            await asyncio.sleep(7)

        if state.get("active"):
            await end_quiz_logic(chat_id)
            
    except Exception as e:
        logger.error(f"Quiz loop error for {chat_id}: {e}")
        QUIZ_STATE.pop(chat_id, None)

async def end_quiz_logic(chat_id):
    state = QUIZ_STATE.get(chat_id)
    if not state: return
    
    scores_dict = state["scores"]
    results_text = "<b>Kɪᴍsᴇ ᴘᴜᴀɴ ᴀʟᴀᴍᴀᴅɪ!</b>"
    
    if scores_dict:
        sorted_sc = sorted(scores_dict.items(), key=lambda x: x[1][1], reverse=True)
        results_text = "<b>🥇 Tᴏᴘʟᴀᴍ Pᴜᴀɴ Sɪʀᴀʟᴀᴍᴀsɪ:</b>\n\n"
        for i, (uid, (mention, pts)) in enumerate(sorted_sc, 1):
            results_text += f"{i}. {mention} → <b>{pts} Pᴜᴀɴ</b>\n"
            
    try:
        await app.send_message(chat_id, f"🏆 <b>Yᴀʀɪşᴍᴀ Sᴏɴᴜᴄ̧ʟᴀʀɪ</b>\n\n{results_text}")
    except: pass
    QUIZ_STATE.pop(chat_id, None)

@app.on_message(filters.text & filters.group & ~app.blacklist_filter, group=10)
async def quiz_answer_hndlr(_, m: types.Message):
    chat_id = m.chat.id
    if chat_id not in QUIZ_STATE: return
    
    state = QUIZ_STATE[chat_id]
    if not state.get("active") or not state.get("answer"): return
    if not m.from_user: return
    
    guess = normalize(m.text)
    answer = normalize(state["answer"])
    
    if len(guess) >= 3 and (guess in answer or answer in guess):
        uid = m.from_user.id
        if uid not in state["scores"]:
            state["scores"][uid] = [m.from_user.mention, 0]
        
        state["scores"][uid][1] += 10
        try: await db.add_quiz_score(uid, 10)
        except: pass
        
        state["answer"] = None 
        state["winner_found"].set()
        await m.reply_text(m.lang.get("quiz_winner", "🎉 <b>Tebrikler {0}, doğru bildin! (+10 Puan)</b>").format(m.from_user.mention, 10))

@app.on_message(filters.command(["son", "bitir"]) & filters.group & ~app.blacklist_filter)
async def end_quiz_early_cmd(_, m: types.Message):
    chat_id = m.chat.id
    if chat_id in QUIZ_STATE and QUIZ_STATE[chat_id].get("active"):
        QUIZ_STATE[chat_id]["active"] = False
        QUIZ_STATE[chat_id]["winner_found"].set()
        await m.reply_text("<b>🛑 Yarışma erken sonlandırıldı!</b>")
        await end_quiz_logic(chat_id)


