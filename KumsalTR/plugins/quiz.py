# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam

import os
import random
import asyncio
import re
import yt_dlp
from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from KumsalTR import app, db, lang, logger, config

# Active quizzes: {chat_id: {round_data...}}
QUIZ_STATE: dict[int, dict] = {}

TR_POP = [
    ("Mabel Matiz - Sarışın", "WYSnXJYFfTg"),
    ("Semicenk - Pişman Değilim", "WreX7kI5O08"),
    ("Tarkan - Kuzu Kuzu", "G7LN-Y-R3GY"),
    ("Sezen Aksu - Geri Dön", "WRbfRZCvCHs"),
    ("Barış Manço - Gülpembe", "Hpt3lS_6vIc"),
    ("Teoman - İstanbul'da Sonbahar", "J6IOMvSvKyU"),
    ("Mor ve Ötesi - Cambaz", "TFY-5RLSM8Y"),
    ("Manga - Dursun Zaman", "HhrY23GQEBU"),
    ("Simge - Yankı", "v31e6S-c3CA"),
    ("Edis - Çok Çok", "H-RgAqgqLNA"),
    ("Hadise - Düm Tek Tek", "LVMqyiUGBXQ"),
    ("Zeynep Bastık - Felaket", "U2dyjNNWW3U"),
    ("Gülşen - Bangır Bangır", "3I8I0XmxKqs"),
    ("Kenan Doğulu - Shake It Up Şekerim", "p-TdmLKL4Ck"),
]

TR_ARABESK = [
    ("Müslüm Gürses - Nilüfer", "tF_1YKkISRo"),
    ("Ahmet Kaya - Kum Gibi", "f3dA8x6gE90"),
    ("İbrahim Tatlıses - Haydi Söyle", "YcR5Fm5M7pY"),
    ("Ebru Gündeş - Araftayım", "7KjM4b5N9R0"),
    ("Orhan Gencebay - Batsın Bu Dünya", "JkP6T5O7wL4"),
    ("Bergen - Sen Ağlama", "IeJ6R3N4M8U"),
    ("Hakan Altun - Telefonun Başında", "KfH4M9wQ8R0"),
]

EN_POP = [
    ("The Weeknd - Blinding Lights", "4NRXx6U4d44"),
    ("Dua Lipa - Levitating", "TUVcZfQe-Kw"),
    ("Harry Styles - As It Was", "H5v3kku4y6Q"),
    ("Sia - Unstoppable", "cxjvTXo9WWM"),
    ("Rihanna - Diamonds", "lWA2pjMjpBs"),
    ("Imagine Dragons - Believer", "7wtfhZwyrcc"),
    ("Coldplay - Yellow", "yKNxeF4KMsY"),
    ("Linkin Park - In the End", "eVTXPUF4Oz4"),
    ("Eminem - Without Me", "YVkUvmDQ-as"),
    ("Lady Gaga - Bad Romance", "qrO4YZeyl0I"),
    ("Adele - Rolling in the Deep", "rYEDA3JcQqw"),
    ("Billie Eilish - Bad Guy", "DyDfgMOUjCI"),
    ("Drake - One Dance", "qL7zrWcc44c"),
    ("Doja Cat - Say So", "pok8H_KF1FA"),
    ("Post Malone - Circles", "wXhTHyIgQ_U"),
]

def normalize(text):
    return re.sub(r'[^a-zA-Z0-9]', '', text.lower())

async def get_snippet(vid_id):
    path = f"downloads/quiz_{vid_id}.m4a"
    if os.path.exists(path) and os.path.getsize(path) > 1024:
        return path
    
    start = random.randint(30, 90)
    end = start + 30
    
    opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio/best",
        "outtmpl": f"downloads/quiz_{vid_id}.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
        }],
        "download_ranges": yt_dlp.utils.download_range_func(None, [(start, end)]),
        "force_keyframes_at_cuts": True,
    }
    
    def _dl():
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={vid_id}"])
    
    try:
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
        await asyncio.wait_for(asyncio.to_thread(_dl), timeout=60)
    except asyncio.TimeoutError:
        logger.error(f"Quiz download timeout for {vid_id}")
        return None
    except Exception as e:
        logger.error(f"Quiz download error for {vid_id}: {e}")
        return None
        
    for ext in ["m4a", "mp3", "opus", "webm", "ogg"]:
        alt = f"downloads/quiz_{vid_id}.{ext}"
        if os.path.exists(alt) and os.path.getsize(alt) > 1024:
            return alt
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
        elif lang_sel == "en" and cat == "pop": pool = EN_POP
        
        if not pool: pool = TR_POP
        
        try:
            await cb.message.delete()
        except Exception:
            pass
        
        QUIZ_STATE[chat_id] = {
            "round": 0,
            "max_rounds": rounds,
            "wrong_rounds": 0,
            "scores": {},
            "answer": None,
            "winner_found": asyncio.Event(),
            "active": True,
            "pool": list(pool),
            "retry_count": 0,
        }
        
        asyncio.create_task(quiz_loop(chat_id))

async def quiz_loop(chat_id):
    state = QUIZ_STATE.get(chat_id)
    if not state:
        return

    try:
        while state["active"]:
            if state["round"] >= state["max_rounds"]:
                break
                
            state["round"] += 1
            state["winner_found"].clear()
            
            if state["wrong_rounds"] >= 4:
                await app.send_message(chat_id, "<b>🚫 Üsᴛ ᴜ̈sᴛᴇ 4 ᴋᴇᴢ ᴋɪᴍsᴇ ʙɪʟᴇᴍᴇᴅɪ! Yᴀʀɪşᴍᴀ ɪᴘᴛᴀʟ ᴇᴅɪʟᴅɪ.</b>")
                break

            name, vid = random.choice(state["pool"])
            state["answer"] = name
            
            await app.send_message(chat_id, f"🎵 <b>{state['round']}. Tᴜʀ Bᴀşʟᴀᴅɪ!</b>\n\n⌚ <b>30 sᴀɴɪʏᴇɴɪᴢ ᴠᴀʀ!</b>")
            
            snippet = await get_snippet(vid)
            
            if not snippet or not os.path.exists(snippet):
                state["round"] -= 1
                state["retry_count"] = state.get("retry_count", 0) + 1
                if state["retry_count"] >= 3:
                    await app.send_message(chat_id, "<b>⚠️ Şᴀʀᴋɪ ɪɴᴅɪʀɪʟᴇᴍɪʏᴏʀ, ᴀᴛʟᴀɴɪʏᴏʀ...</b>")
                    state["retry_count"] = 0
                    state["round"] += 1
                await asyncio.sleep(2)
                continue
            
            state["retry_count"] = 0
            
            try:
                await app.send_voice(chat_id, snippet)
            except Exception as e:
                logger.error(f"Quiz voice send error: {e}")
                state["round"] -= 1
                await asyncio.sleep(2)
                continue
            
            try:
                await asyncio.wait_for(state["winner_found"].wait(), timeout=30)
                state["wrong_rounds"] = 0
            except asyncio.TimeoutError:
                if not state["winner_found"].is_set() and state["active"]:
                    state["wrong_rounds"] += 1
                    await app.send_message(chat_id, f"❌ <b>Sᴜ̈ʀᴇ ᴅᴏʟᴅᴜ! Kɪᴍsᴇ ʙɪʟᴇᴍᴇᴅɪ.</b>\n\n🎵 <b>Cᴇᴠᴀᴘ:</b> {name}")
                    state["answer"] = None
            
            if snippet and os.path.exists(snippet):
                try:
                    os.remove(snippet)
                except Exception:
                    pass
                
            await asyncio.sleep(4)

        if state.get("active"):
            await end_quiz_logic(chat_id)
    except Exception as e:
        logger.error(f"Quiz loop error for {chat_id}: {e}")
        QUIZ_STATE.pop(chat_id, None)

async def end_quiz_logic(chat_id):
    state = QUIZ_STATE.get(chat_id)
    if not state:
        return
    
    scores_dict = state["scores"]
    results_text = "<b>Kɪᴍsᴇ ᴘᴜᴀɴ ᴀʟᴀᴍᴀᴅɪ!</b>"
    
    if scores_dict:
        sorted_sc = sorted(scores_dict.items(), key=lambda x: x[1][1], reverse=True)
        results_text = ""
        for i, (uid, (mention, pts)) in enumerate(sorted_sc, 1):
            results_text += f"{i}. {mention} ({pts} Pᴜᴀɴ)\n"
            
    await app.send_message(chat_id, f"🏆 <b>Yᴀʀɪşᴍᴀ Sᴏɴᴜᴄ̧ʟᴀʀɪ</b>\n\n{results_text}")
    QUIZ_STATE.pop(chat_id, None)

@app.on_message(filters.text & filters.group & ~app.blacklist_filter, group=10)
async def quiz_answer_hndlr(_, m: types.Message):
    chat_id = m.chat.id
    if chat_id not in QUIZ_STATE:
        return
    
    state = QUIZ_STATE[chat_id]
    if not state.get("answer"):
        return
    if not m.from_user:
        return
    
    guess = normalize(m.text)
    answer = normalize(state["answer"])
    
    if len(guess) < 3:
        return
    
    if answer in guess or guess in answer:
        uid = m.from_user.id
        if uid not in state["scores"]:
            state["scores"][uid] = [m.from_user.mention, 0]
        
        state["scores"][uid][1] += 10
        try:
            await db.add_quiz_score(uid, 10)
        except Exception as e:
            logger.error(f"Quiz score update error: {e}")
        
        state["answer"] = None 
        state["winner_found"].set()
        await m.reply_text(f"🎉 <b>Tᴇʙʀɪᴋʟᴇʀ {m.from_user.mention}!</b> Dᴏɢ̆ʀᴜ ʙɪʟᴅɪɴ ᴠᴇ <b>+10</b> ᴘᴜᴀɴ ᴋᴀᴢᴀɴᴅɪɴ!")


