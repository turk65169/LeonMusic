import json
import re

SMALL_CAPS = {
    'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ғ', 'g': 'ɢ', 
    'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 
    'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ', 
    'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ',
    'A': 'ᴀ', 'B': 'ʙ', 'C': 'ᴄ', 'D': 'ᴅ', 'E': 'ᴇ', 'F': 'ғ', 'G': 'ɢ', 
    'H': 'ʜ', 'I': 'ɪ', 'J': 'ᴊ', 'K': 'ᴋ', 'L': 'ʟ', 'M': 'ᴍ', 'N': 'ɴ', 
    'O': 'ᴏ', 'P': 'ᴘ', 'Q': 'ǫ', 'R': 'ʀ', 'S': 's', 'T': 'ᴛ', 'U': 'ᴜ', 
    'V': 'ᴠ', 'W': 'ᴡ', 'X': 'x', 'Y': 'ʏ', 'Z': 'ᴢ',
    'ç': 'ᴄ̧', 'Ç': 'ᴄ̧', 'ğ': 'ɢ̆', 'Ğ': 'ɢ̆', 'ı': 'ɪ', 'İ': 'ɪ̇', 'ö': 'ᴏ̈', 'Ö': 'ᴏ̈',
    'ü': 'ᴜ̈', 'Ü': 'ᴜ̈', 'ş': 'ş', 'Ş': 'ş'
}

BOLD_MATH = {
    'A': '𝐀', 'B': '𝐁', 'C': '𝐂', 'D': '𝐃', 'E': '𝐄', 'F': '𝐅', 'G': '𝐆', 
    'H': '𝐇', 'I': '𝐈', 'J': '𝐉', 'K': '𝐊', 'L': '𝐋', 'M': '𝐌', 'N': '𝐍', 
    'O': '𝐎', 'P': '𝐏', 'Q': '𝐐', 'R': '𝐑', 'S': '𝐒', 'T': '𝐓', 'U': '𝐔', 
    'V': '𝐕', 'W': '𝐖', 'X': '𝐗', 'Y': '𝐘', 'Z': '𝐙',
    'Ç': '𝐂̧', 'Ğ': '𝐆̆', 'İ': '𝐈̇', 'Ö': '𝐎̈', 'Ü': '𝐔̈', 'Ş': '𝐒̧'
}

def to_styled(text):
    # Split by HTML tags and string formatting
    parts = re.split(r'(<[^>]+>|\{[^\}]+\})', text)
    processed = []
    
    for part in parts:
        if part.startswith('<') or part.startswith('{'):
            processed.append(part)
        else:
            # For regular text, we want the first letter to be BOLD_MATH and rest SMALL_CAPS
            # But we might have multiple words. Let's make the FIRST letter of the word BOLD_MATH 
            # if the original was uppercase.
            res = ""
            for i, c in enumerate(part):
                if c.isupper() and c in BOLD_MATH:
                    res += BOLD_MATH[c]
                elif c in SMALL_CAPS:
                    res += SMALL_CAPS[c]
                else:
                    res += c
            processed.append(res)
    return "".join(processed)

with open("KumsalTR/locales/en.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Hardcoded overrides for specific menus as requested
data["help_extras"] = "<b>🇮🇹 𝐃ɪɢ̆ᴇʀ 𝐊ᴏᴍᴜᴛʟᴀʀ:</b>\n\n• /bul <code>[sᴏ̈ᴢ/ᴠɪᴅᴇᴏ]</code>\n├ ʏᴀᴢᴅɪɢ̆ɪɴɪᴢ sᴏ̈ᴢʟᴇʀᴅᴇɴ şᴀʀᴋɪʏɪ ʙᴜʟᴜʀ,\n├ ʏᴀɴɪᴛʟᴀᴅɪɢ̆ɪɴɪᴢ ᴠɪᴅᴇᴏᴅᴀᴋɪ ᴍᴜ̈ᴢɪɢ̆ɪ ʙᴜʟᴜʀ,\n├ ᴍᴀᴋsɪᴍᴜᴍ 10ᴍʙ ᴠɪᴅᴇᴏ ᴅᴇsᴛᴇᴋʟᴇɴɪʀ,\n├ ʙᴜʟᴜɴᴀɴ şᴀʀᴋɪʏɪ ʏᴏᴜᴛᴜʙᴇ'ᴅᴀ ɪᴢʟᴇ,\n└ ɪsᴛᴇʀsᴇɴ ᴅɪʀᴇᴋᴛ ᴏʏɴᴀᴛ.\n\n• /oneri\n├ ᴛʀᴇɴᴅ ʟɪsᴛᴇsɪɴɪ ɢᴏ̈ʀᴜ̈ɴᴛᴜ̈ʟᴇ,\n├ ɪsᴛᴇᴅɪᴋʟᴇʀɪɴᴇ ᴛɪᴋʟᴀʏɪᴘ ɪşᴀʀᴇᴛʟᴇ,\n└ sᴇᴄ̧ɪʟᴇɴʟᴇʀɪ ᴏʏɴᴀᴛ ᴠᴇ ᴅɪɴʟᴇ.\n\n• /yarisma\n├ şᴀʀᴋɪ ᴅɪʟɪ sᴇᴄ̧ (ᴛᴜ̈ʀᴋᴄ̧ᴇ, ɪɴɢɪʟɪᴢᴄᴇ),\n├ ᴛᴜ̈ʀᴜ̈ sᴇᴄ̧ (ᴀʀᴀʙᴇsᴋ, ᴘᴏᴘ ᴠʙ.),\n├ ʙᴏᴛ 30sɴ ᴍᴜ̈ᴢɪᴋ ᴋᴇsɪᴛʟᴇʀɪ ᴀᴛᴀᴄᴀᴋ,\n└ ɪsɪᴍʟᴇʀɪɴɪ ʙɪʟ ᴠᴇ ᴘᴜᴀɴ ᴋᴀᴢᴀɴ.\n\n• /hediye\n├ ᴀʟɪᴄɪ ɪᴅ ᴠᴇʏᴀ ᴋᴜʟʟᴀɴɪᴄɪ ᴀᴅɪ ɢɪʀ,\n├ ɪsᴍɪɴ ɢᴏ̈ʀᴜ̈ɴsᴜ̈ɴ ᴍᴜ̈ sᴇᴄ̧,\n└ şᴀʀᴋɪ ᴀᴅɪɴɪ ʏᴀᴢ ᴠᴇ ɢᴏ̈ɴᴅᴇʀ.\n\n• /ruhesi <code>[ʏᴀɴɪᴛʟᴀ]</code>\n├ ʏᴀɴɪᴛʟᴀᴅɪɢ̆ɪɴ ᴋɪşɪʏʟᴇ ᴇşʟᴇş,\n├ ᴇşɪɴ ʜᴀɴɢɪ şᴀʀᴋɪʏɪ ᴅɪɴʟɪʏᴏʀ ɢᴏ̈ʀ,\n├ ʜᴀɴɢɪ ɢʀᴜᴘᴛᴀ ᴅɪɴʟɪʏᴏʀ ᴏ̈ɢ̆ʀᴇɴ,\n└ şᴀʀᴋɪ ᴀᴄ̧ᴛɪɢ̆ɪɴᴅᴀ ʙɪʟɢɪ ᴀʟ.\n\n• /ayril - ᴍᴇᴠᴄᴜᴛ ʀᴜʜ ᴇşɪɴɪᴢᴅᴇɴ ᴀʏʀɪʟɪɴ.\n• /stat - ᴅɪɴʟᴇᴍᴇ ɪsᴛᴀᴛɪsᴛɪᴋʟᴇʀɪɴɪ ᴀʟɪɴ.\n• /kart - ɪsᴛᴀᴛɪsᴛɪᴋ ᴋᴀʀᴛɪɴɪᴢɪ ᴀʟɪɴ.\n\n• /son VEYA /bitir\n└ ᴀᴋᴛɪғ ʏᴀʀɪşᴍᴀʏɪ, ᴍᴜ̈ᴢɪɢ̆ɪ ᴀɴɪɴᴅᴀ sᴏɴʟᴀɴᴅɪʀɪʀ."
data["help_indir"] = "<b>📥 𝐒̧ᴀʀᴋɪ ᴠᴇ 𝐌ᴇᴅʏᴀ 𝐈̇ɴᴅɪʀɪᴄɪ:</b>\n\n• /indir <code>[şᴀʀᴋɪ ᴀᴅɪ]</code> - şᴀʀᴋɪ ɪɴᴅɪʀɪʀ.\n\n<b>📥 Mᴇᴅʏᴀ ɪ̇ɴᴅɪʀɪᴄɪ:</b>\nᴀşᴀɢ̆ɪᴅᴀᴋɪ ᴘʟᴀᴛғᴏʀᴍʟᴀʀɪɴ ᴍᴇᴅʏᴀ ᴘᴀʏʟᴀşɪᴍ ʟɪɴᴋʟᴇʀɪɴɪ ɢʀᴜʙᴀ ᴀᴛᴍᴀɴɪᴢ ʏᴇᴛᴇʀʟɪᴅɪʀ:\n\n• ɪɴsᴛᴀɢʀᴀᴍ\n└ (ɢᴏ̈ɴᴅᴇʀɪ, ʜɪᴋᴀʏᴇ, ʀᴇᴇʟs)\n\n• ʏᴏᴜᴛᴜʙᴇ\n└ (ᴠɪᴅᴇᴏ, sʜᴏʀᴛs, sᴇs)\n\n• ᴛɪᴋᴛᴏᴋ\n└ (ғɪʟɪɢʀᴀɴsɪᴢ ᴠɪᴅᴇᴏ)\n\n• ғᴀᴄᴇʙᴏᴏᴋ\n└ (ɢᴏ̈ɴᴅᴇʀɪ, ʀᴇᴇʟs)\n\n• ᴘɪɴᴛᴇʀᴇsᴛ\n└ (ғᴏᴛᴏɢ̆ʀᴀғ, ᴠɪᴅᴇᴏ)\n\n• sɴᴀᴘᴄʜᴀᴛ\n└ (ғᴏᴛᴏɢ̆ʀᴀғ, ᴠɪᴅᴇᴏ)\n\n• ᴛᴇʟᴇɢʀᴀᴍ\n└ (ʜɪᴋᴀʏᴇ ɪɴᴅɪʀᴍᴇ)\n\n• ʟɪᴋᴇᴇ\n└ (ғɪʟɪɢʀᴀɴsɪᴢ ᴠɪᴅᴇᴏ)\n\n• ᴛʜʀᴇᴀᴅs\n└ (ғᴏᴛᴏɢ̆ʀᴀғ, ᴠɪᴅᴇᴏ)"

for k, v in data.items():
    if k not in ["start_pm", "help_extras", "help_indir"]:
        data[k] = to_styled(v)

with open("KumsalTR/locales/en.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print("Done")
