import time
import requests
import json
import re
import os
from datetime import datetime
import sqlite3
import telebot
from telebot import types
import random

# ======================
# 🔧 إعدادات البوت الأساسية
# ======================
BOT_TOKEN = "8600170211:AAG1J6RNCk_JqwcUi7V8zdic2mLYQW7f8GI" # ضع توكن بوتك هنا

# قروب التخزين الذي سيستقبل منه البوت الرسائل والأكواد
STORAGE_GROUP_ID = "-1003804573691" 

ADMIN_IDS =[6114298715, 8557165332]  # ضع الآيدي الخاص بك هنا
DB_PATH = "bot.db"
BOT_ACTIVE = True 

if not BOT_TOKEN:
    raise SystemExit("❌ BOT_TOKEN must be set")

# ======================
# 🌍 رموز الدول (محدثة وشاملة لأكثر من 260 دولة ومنطقة ذكية)
# ======================
COUNTRY_CODES = {
    # NANP (أمريكا الشمالية والكاريبي) - تم فصلها لحل مشكلة التداخل
    "1242": ("Bahamas", "🇧🇸", "BS"), "1246": ("Barbados", "🇧🇧", "BB"), "1264": ("Anguilla", "🇦🇮", "AI"),
    "1268": ("Antigua & Barbuda", "🇦🇬", "AG"), "1284": ("BVI", "🇻🇬", "VG"), "1340": ("USVI", "🇻🇮", "VI"),
    "1345": ("Cayman Islands", "🇰🇾", "KY"), "1441": ("Bermuda", "🇧🇲", "BM"), "1473": ("Grenada", "🇬🇩", "GD"),
    "1649": ("Turks & Caicos", "🇹🇨", "TC"), "1664": ("Montserrat", "🇲🇸", "MS"), "1721": ("Sint Maarten", "🇸🇽", "SX"),
    "1758": ("St. Lucia", "🇱🇨", "LC"), "1767": ("Dominica", "🇩🇲", "DM"), "1784": ("St. Vincent", "🇻🇨", "VC"),
    "1809": ("Dominican Rep.", "🇩🇴", "DO"), "1829": ("Dominican Rep.", "🇩🇴", "DO"), "1849": ("Dominican Rep.", "🇩🇴", "DO"),
    "1868": ("Trinidad & Tobago", "🇹🇹", "TT"), "1876": ("Jamaica", "🇯🇲", "JM"), "1939": ("Puerto Rico", "🇵🇷", "PR"),
    "1": ("USA/Canada", "🇺🇸/🇨🇦", "US/CA"),
    
    # باقي دول العالم
    "7": ("Russia/Kazakhstan", "🇷🇺", "RU"), "20": ("Egypt", "🇪🇬", "EG"),
    "27": ("South Africa", "🇿🇦", "ZA"), "30": ("Greece", "🇬🇷", "GR"), "31": ("Netherlands", "🇳🇱", "NL"),
    "32": ("Belgium", "🇧🇪", "BE"), "33": ("France", "🇫🇷", "FR"), "34": ("Spain", "🇪🇸", "ES"),
    "36": ("Hungary", "🇭🇺", "HU"), "39": ("Italy", "🇮🇹", "IT"), "40": ("Romania", "🇷🇴", "RO"),
    "41": ("Switzerland", "🇨🇭", "CH"), "43": ("Austria", "🇦🇹", "AT"), "44": ("United Kingdom", "🇬🇧", "UK"),
    "45": ("Denmark", "🇩🇰", "DK"), "46": ("Sweden", "🇸🇪", "SE"), "47": ("Norway", "🇳🇴", "NO"),
    "48": ("Poland", "🇵🇱", "PL"), "49": ("Germany", "🇩🇪", "DE"), "51": ("Peru", "🇵🇪", "PE"),
    "52": ("Mexico", "🇲🇽", "MX"), "53": ("Cuba", "🇨🇺", "CU"), "54": ("Argentina", "🇦🇷", "AR"),
    "55": ("Brazil", "🇧🇷", "BR"), "56": ("Chile", "🇨🇱", "CL"), "57": ("Colombia", "🇨🇴", "CO"),
    "58": ("Venezuela", "🇻🇪", "VE"), "60": ("Malaysia", "🇲🇾", "MY"), "61": ("Australia", "🇦🇺", "AU"),
    "62": ("Indonesia", "🇮🇩", "ID"), "63": ("Philippines", "🇵🇭", "PH"), "64": ("New Zealand", "🇳🇿", "NZ"),
    "65": ("Singapore", "🇸🇬", "SG"), "66": ("Thailand", "🇹🇭", "TH"), "81": ("Japan", "🇯🇵", "JP"),
    "82": ("South Korea", "🇰🇷", "KR"), "84": ("Vietnam", "🇻🇳", "VN"), "86": ("China", "🇨🇳", "CN"),
    "90": ("Turkey", "🇹🇷", "TR"), "91": ("India", "🇮🇳", "IN"), "92": ("Pakistan", "🇵🇰", "PK"),
    "93": ("Afghanistan", "🇦🇫", "AF"), "94": ("Sri Lanka", "🇱🇰", "LK"), "95": ("Myanmar", "🇲🇲", "MM"),
    "98": ("Iran", "🇮🇷", "IR"), "211": ("South Sudan", "🇸🇸", "SS"), "212": ("Morocco", "🇲🇦", "MA"),
    "213": ("Algeria", "🇩🇿", "DZ"), "216": ("Tunisia", "🇹🇳", "TN"), "218": ("Libya", "🇱🇾", "LY"),
    "220": ("Gambia", "🇬🇲", "GM"), "221": ("Senegal", "🇸🇳", "SN"), "222": ("Mauritania", "🇲🇷", "MR"),
    "223": ("Mali", "🇲🇱", "ML"), "224": ("Guinea", "🇬🇳", "GN"), "225": ("Ivory Coast", "🇨🇮", "CI"),
    "226": ("Burkina Faso", "🇧🇫", "BF"), "227": ("Niger", "🇳🇪", "NE"), "228": ("Togo", "🇹🇬", "TG"),
    "229": ("Benin", "🇧🇯", "BJ"), "230": ("Mauritius", "🇲🇺", "MU"), "231": ("Liberia", "🇱🇷", "LR"),
    "232": ("Sierra Leone", "🇸🇱", "SL"), "233": ("Ghana", "🇬🇭", "GH"), "234": ("Nigeria", "🇳🇬", "NG"),
    "235": ("Chad", "🇹🇩", "TD"), "236": ("Central African Rep", "🇨🇫", "CF"), "237": ("Cameroon", "🇨🇲", "CM"),
    "238": ("Cape Verde", "🇨🇻", "CV"), "239": ("Sao Tome", "🇸🇹", "ST"), "240": ("Equatorial Guinea", "🇬🇶", "GQ"), 
    "241": ("Gabon", "🇬🇦", "GA"), "242": ("Congo", "🇨🇬", "CG"), "243": ("DR Congo", "🇨🇩", "CD"), 
    "244": ("Angola", "🇦🇴", "AO"), "245": ("Guinea-Bissau", "🇬🇼", "GW"), "246": ("Diego Garcia", "🇮🇴", "IO"),
    "248": ("Seychelles", "🇸🇨", "SC"), "249": ("Sudan", "🇸🇩", "SD"), "250": ("Rwanda", "🇷🇼", "RW"), 
    "251": ("Ethiopia", "🇪🇹", "ET"), "252": ("Somalia", "🇸🇴", "SO"), "253": ("Djibouti", "🇩🇯", "DJ"), 
    "254": ("Kenya", "🇰🇪", "KE"), "255": ("Tanzania", "🇹🇿", "TZ"), "256": ("Uganda", "🇺🇬", "UG"), 
    "257": ("Burundi", "🇧🇮", "BI"), "258": ("Mozambique", "🇲🇿", "MZ"), "260": ("Zambia", "🇿🇲", "ZM"), 
    "261": ("Madagascar", "🇲🇬", "MG"), "262": ("Reunion", "🇷🇪", "RE"), "263": ("Zimbabwe", "🇿🇼", "ZW"),
    "264": ("Namibia", "🇳🇦", "NA"), "265": ("Malawi", "🇲🇼", "MW"), "266": ("Lesotho", "🇱🇸", "LS"),
    "267": ("Botswana", "🇧🇼", "BW"), "268": ("Eswatini", "🇸🇿", "SZ"), "269": ("Comoros", "🇰🇲", "KM"),
    "297": ("Aruba", "🇦🇼", "AW"), "298": ("Faroe Islands", "🇫🇴", "FO"), "299": ("Greenland", "🇬🇱", "GL"),
    "350": ("Gibraltar", "🇬🇮", "GI"), "351": ("Portugal", "🇵🇹", "PT"), "352": ("Luxembourg", "🇱🇺", "LU"),
    "353": ("Ireland", "🇮🇪", "IE"), "354": ("Iceland", "🇮🇸", "IS"), "355": ("Albania", "🇦🇱", "AL"),
    "356": ("Malta", "🇲🇹", "MT"), "357": ("Cyprus", "🇨🇾", "CY"), "358": ("Finland", "🇫🇮", "FI"), 
    "359": ("Bulgaria", "🇧🇬", "BG"), "370": ("Lithuania", "🇱🇹", "LT"), "371": ("Latvia", "🇱🇻", "LV"), 
    "372": ("Estonia", "🇪🇪", "EE"), "373": ("Moldova", "🇲🇩", "MD"), "374": ("Armenia", "🇦🇲", "AM"), 
    "375": ("Belarus", "🇧🇾", "BY"), "376": ("Andorra", "🇦🇩", "AD"), "377": ("Monaco", "🇲🇨", "MC"),
    "378": ("San Marino", "🇸🇲", "SM"), "380": ("Ukraine", "🇺🇦", "UA"), "381": ("Serbia", "🇷🇸", "RS"), 
    "382": ("Montenegro", "🇲🇪", "ME"), "383": ("Kosovo", "🇽🇰", "XK"), "385": ("Croatia", "🇭🇷", "HR"), 
    "386": ("Slovenia", "🇸🇮", "SI"), "387": ("Bosnia", "🇧🇦", "BA"), "389": ("North Macedonia", "🇲🇰", "MK"), 
    "420": ("Czech Republic", "🇨🇿", "CZ"), "421": ("Slovakia", "🇸🇰", "SK"), "423": ("Liechtenstein", "🇱🇮", "LI"),
    "500": ("Falkland Islands", "🇫🇰", "FK"), "501": ("Belize", "🇧🇿", "BZ"), "502": ("Guatemala", "🇬🇹", "GT"), 
    "503": ("El Salvador", "🇸🇻", "SV"), "504": ("Honduras", "🇭🇳", "HN"), "505": ("Nicaragua", "🇳🇮", "NI"), 
    "506": ("Costa Rica", "🇨🇷", "CR"), "507": ("Panama", "🇵🇦", "PA"), "508": ("St. Pierre", "🇵🇲", "PM"),
    "509": ("Haiti", "🇭🇹", "HT"), "590": ("Guadeloupe", "🇬🇵", "GP"), "591": ("Bolivia", "🇧🇴", "BO"), 
    "592": ("Guyana", "🇬🇾", "GY"), "593": ("Ecuador", "🇪🇨", "EC"), "594": ("French Guiana", "🇬🇫", "GF"),
    "595": ("Paraguay", "🇵🇾", "PY"), "596": ("Martinique", "🇲🇶", "MQ"), "597": ("Suriname", "🇸🇷", "SR"),
    "598": ("Uruguay", "🇺🇾", "UY"), "599": ("Curacao", "🇨🇼", "CW"), "670": ("Timor-Leste", "🇹🇱", "TL"),
    "672": ("Norfolk Island", "🇳🇫", "NF"), "673": ("Brunei", "🇧🇳", "BN"), "674": ("Nauru", "🇳🇷", "NR"),
    "675": ("Papua New Guinea", "🇵🇬", "PG"), "676": ("Tonga", "🇹🇴", "TO"), "677": ("Solomon Islands", "🇸🇧", "SB"),
    "678": ("Vanuatu", "🇻🇺", "VU"), "679": ("Fiji", "🇫🇯", "FJ"), "680": ("Palau", "🇵🇼", "PW"),
    "681": ("Wallis & Futuna", "🇼🇫", "WF"), "682": ("Cook Islands", "🇨🇰", "CK"), "683": ("Niue", "🇳🇺", "NU"),
    "685": ("Samoa", "🇼🇸", "WS"), "686": ("Kiribati", "🇰🇮", "KI"), "687": ("New Caledonia", "🇳🇨", "NC"),
    "688": ("Tuvalu", "🇹🇻", "TV"), "689": ("French Polynesia", "🇵🇫", "PF"), "690": ("Tokelau", "🇹🇰", "TK"),
    "691": ("Micronesia", "🇫🇲", "FM"), "692": ("Marshall Islands", "🇲🇭", "MH"), "850": ("North Korea", "🇰🇵", "KP"),
    "852": ("Hong Kong", "🇭🇰", "HK"), "853": ("Macau", "🇲🇴", "MO"), "855": ("Cambodia", "🇰🇭", "KH"), 
    "856": ("Laos", "🇱🇦", "LA"), "880": ("Bangladesh", "🇧🇩", "BD"), "886": ("Taiwan", "🇹🇼", "TW"),
    "960": ("Maldives", "🇲🇻", "MV"), "961": ("Lebanon", "🇱🇧", "LB"), "962": ("Jordan", "🇯🇴", "JO"), 
    "963": ("Syria", "🇸🇾", "SY"), "964": ("Iraq", "🇮🇶", "IQ"), "965": ("Kuwait", "🇰🇼", "KW"), 
    "966": ("Saudi Arabia", "🇸🇦", "SA"), "967": ("Yemen", "🇾🇪", "YE"), "968": ("Oman", "🇴🇲", "OM"), 
    "970": ("Palestine", "🇵🇸", "PS"), "971": ("UAE", "🇦🇪", "AE"), "972": ("Israel", "🇮🇱", "IL"), 
    "973": ("Bahrain", "🇧🇭", "BH"), "974": ("Qatar", "🇶🇦", "QA"), "975": ("Bhutan", "🇧🇹", "BT"),
    "976": ("Mongolia", "🇲🇳", "MN"), "977": ("Nepal", "🇳🇵", "NP"), "992": ("Tajikistan", "🇹🇯", "TJ"), 
    "993": ("Turkmenistan", "🇹🇲", "TM"), "994": ("Azerbaijan", "🇦🇿", "AZ"), "995": ("Georgia", "🇬🇪", "GE"), 
    "996": ("Kyrgyzstan", "🇰🇬", "KG"), "998": ("Uzbekistan", "🇺🇿", "UZ")
}

# ترتيب مفاتيح الدول تنازلياً حسب الطول (لضمان الفحص الذكي)
SORTED_COUNTRY_PREFIXES = sorted(COUNTRY_CODES.keys(), key=len, reverse=True)

# ======================
# 🧠 دوال إنشاء قاعدة البيانات
# ======================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            country_code TEXT,
            assigned_number TEXT,
            is_banned INTEGER DEFAULT 0,
            private_combo_country TEXT DEFAULT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS combos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country_code TEXT,
            combo_index INTEGER DEFAULT 1,
            numbers TEXT,
            UNIQUE(country_code, combo_index)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS otp_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT,
            otp TEXT,
            full_message TEXT,
            timestamp TEXT,
            assigned_to INTEGER
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS bot_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS private_combos (
            user_id INTEGER,
            country_code TEXT,
            numbers TEXT,
            PRIMARY KEY (user_id, country_code)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS force_sub_channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_url TEXT UNIQUE NOT NULL,
            description TEXT DEFAULT '',
            enabled INTEGER DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ======================
# 🧰 دوال إدارة قاعدة البيانات
# ======================
def get_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row

def save_user(user_id, username="", first_name="", last_name="", country_code=None, assigned_number=None, private_combo_country=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    existing_data = get_user(user_id)
    if existing_data:
        if country_code is None: country_code = existing_data[4]
        if assigned_number is None: assigned_number = existing_data[5]
        if private_combo_country is None: private_combo_country = existing_data[7]

    if isinstance(assigned_number, list):
        assigned_number = json.dumps(assigned_number)

    c.execute("""
        REPLACE INTO users (user_id, username, first_name, last_name, country_code, assigned_number, is_banned, private_combo_country)
        VALUES (?, ?, ?, ?, ?, ?, COALESCE((SELECT is_banned FROM users WHERE user_id=?), 0), ?)
    """, (user_id, username, first_name, last_name, country_code, assigned_number, user_id, private_combo_country))
    conn.commit()
    conn.close()

def ban_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET is_banned=1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def unban_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET is_banned=0 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def is_banned(user_id):
    user = get_user(user_id)
    return user and user[6] == 1
    
def is_maintenance_mode():
    return not BOT_ACTIVE

def set_maintenance_mode(status):
    global BOT_ACTIVE
    BOT_ACTIVE = not status
    
def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE is_banned=0")
    users =[row[0] for row in c.fetchall()]
    conn.close()
    return users

def get_combo(country_code, combo_index=1, user_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if user_id:
        c.execute("SELECT numbers FROM private_combos WHERE user_id=? AND country_code=?", (user_id, country_code))
        row = c.fetchone()
        if row:
            conn.close()
            return json.loads(row[0])
    c.execute("SELECT numbers FROM combos WHERE country_code=? AND combo_index=?", (country_code, combo_index))
    row = c.fetchone()
    conn.close()
    return json.loads(row[0]) if row else[]

def save_combo(country_code, numbers, user_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if user_id:
        c.execute("REPLACE INTO private_combos (user_id, country_code, numbers) VALUES (?, ?, ?)",
                  (user_id, country_code, json.dumps(numbers)))
    else:
        c.execute("SELECT MAX(combo_index) FROM combos WHERE country_code=?", (country_code,))
        max_index = c.fetchone()[0]
        next_index = 1 if max_index is None else max_index + 1
        c.execute("INSERT INTO combos (country_code, combo_index, numbers) VALUES (?, ?, ?)",
                  (country_code, next_index, json.dumps(numbers)))
    conn.commit()
    conn.close()

def delete_combo(country_code, combo_index=None, user_id=None):
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH, timeout=30.0, check_same_thread=False)
        c = conn.cursor()
        if user_id:
            c.execute("DELETE FROM private_combos WHERE user_id=? AND country_code=?", (user_id, country_code))
        elif combo_index:
            c.execute("DELETE FROM combos WHERE country_code=? AND combo_index=?", (country_code, combo_index))
        else:
            c.execute("DELETE FROM combos WHERE country_code=?", (country_code,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        if conn: conn.rollback()
        return False
    finally:
        if conn: conn.close()

def get_all_combos():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT country_code, combo_index FROM combos ORDER BY country_code, combo_index")
    combos = c.fetchall()
    conn.close()
    return combos 

def assign_numbers_to_user(user_id, numbers_list):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET assigned_number=? WHERE user_id=?", (json.dumps(numbers_list), user_id))
    conn.commit()
    conn.close()

def log_otp(number, otp, full_message, assigned_to=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO otp_logs (number, otp, full_message, timestamp, assigned_to) VALUES (?, ?, ?, ?, ?)",
              (number, otp, full_message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), assigned_to))
    conn.commit()
    conn.close()

def release_numbers(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET assigned_number=NULL WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def get_otp_logs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM otp_logs")
    logs = c.fetchall()
    conn.close()
    return logs

def get_user_info(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row

def get_all_force_sub_channels(enabled_only=True):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if enabled_only:
        c.execute("SELECT id, channel_url, description FROM force_sub_channels WHERE enabled = 1 ORDER BY id")
    else:
        c.execute("SELECT id, channel_url, description FROM force_sub_channels ORDER BY id")
    rows = c.fetchall()
    conn.close()
    return rows

def add_force_sub_channel(channel_url, description=""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO force_sub_channels (channel_url, description, enabled) VALUES (?, ?, 1)",
                  (channel_url.strip(), description.strip()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False 
    finally:
        conn.close()

def delete_force_sub_channel(channel_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM force_sub_channels WHERE id = ?", (channel_id,))
    changed = c.rowcount > 0
    conn.commit()
    conn.close()
    return changed

def toggle_force_sub_channel(channel_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE force_sub_channels SET enabled = 1 - enabled WHERE id = ?", (channel_id,))
    conn.commit()
    conn.close()

# ======================
# 🔐 دوال الاشتراك الإجباري
# ======================
def force_sub_check(user_id):
    channels = get_all_force_sub_channels(enabled_only=True)
    if not channels: return True
    for _, url, _ in channels:
        try:
            if url.startswith("https://t.me/"): ch = "@" + url.split("/")[-1]
            elif url.startswith("@"): ch = url
            else: continue
            member = bot.get_chat_member(ch, user_id)
            if member.status not in["member", "administrator", "creator"]: return False
        except:
            return False 
    return True

def force_sub_markup():
    channels = get_all_force_sub_channels(enabled_only=True)
    if not channels: return None
    markup = types.InlineKeyboardMarkup()
    for _, url, desc in channels:
        text = f"📢 {desc}" if desc else "📢 اشترك في القناة"
        markup.add(types.InlineKeyboardButton(text, url=url))
    markup.add(types.InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_sub"))
    return markup

# ======================
# 🤖 إنشاء بوت Telegram
# ======================
bot = telebot.TeleBot(BOT_TOKEN)

def is_admin(user_id):
    return user_id in ADMIN_IDS

def safe_html(text):
    if not text: return ""
    text = str(text)
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    return text
    
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if is_maintenance_mode() and not is_admin(user_id):
        bot.send_message(chat_id, "<b>⚠️ عذراً عزيزي المستخدم..\nالبوت الآن في وضع الصيانة لتحديث الخدمات.</b>", parse_mode="HTML")
        return

    if is_banned(user_id):
        bot.reply_to(message, "<b>🚫 عذراً، لقد تم حظرك من استخدام البوت.</b>", parse_mode="HTML")
        return

    if not force_sub_check(user_id):
        markup = force_sub_markup()
        if markup: bot.send_message(chat_id, "<b>🔒 يجب الاشتراك في القنوات لاستخدام البوت.</b>", parse_mode="HTML", reply_markup=markup)
        return

    if not get_user(user_id):
        save_user(user_id, username=message.from_user.username or "", first_name=message.from_user.first_name or "", last_name=message.from_user.last_name or "")
        for admin in ADMIN_IDS:
            try: bot.send_message(admin, f"🆕 <b>مستخدم جديد دخل البوت:</b>\n🆔: <code>{user_id}</code>", parse_mode="HTML")
            except: pass
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons =[]
    user_data = get_user(user_id)
    private_combo = user_data[7] if user_data else None
    all_combos = get_all_combos()

    country_combos = {}
    for country_code, combo_index in all_combos:
        if country_code not in country_combos: country_combos[country_code] =[]
        country_combos[country_code].append(combo_index)

    if private_combo and private_combo in COUNTRY_CODES:
        name, flag, _ = COUNTRY_CODES[private_combo]
        buttons.append(types.InlineKeyboardButton(f"{flag} {name} (Private)", callback_data=f"country_{private_combo}_1"))

    for country_code, indices in country_combos.items():
        if country_code in COUNTRY_CODES and country_code != private_combo:
            name, flag, _ = COUNTRY_CODES[country_code]
            for idx in indices:
                btn_text = f"{flag} {name}" if len(indices) == 1 else f"{flag} {name} ({idx})"
                buttons.append(types.InlineKeyboardButton(btn_text, callback_data=f"country_{country_code}_{idx}"))

    for i in range(0, len(buttons), 2):
        markup.row(*buttons[i:i+2])

    if is_admin(user_id):
        markup.add(types.InlineKeyboardButton("🔐 Admin Panel", callback_data="admin_panel"))

    fancy_text = (
        "<b>❍────── <u> بـوت الأرقـام </u> ──────❍</b>\n\n"
        "<b>🔋 <u>أهـلاً بك عزيزي المستخدم في البوت</u></b>\n\n"
        "<b>🎓 <u>نـوفـر لـك أرقـام لـجـمـيـع الـدول</u></b>\n\n"
        "<b>────────────────────</b>\n"
        "<b><u>اخـتـر الــدولـة الـتـي تـريـدهـا مـن الـزر بالأسـفـل</u> ⬇️</b>"
    )
    bot.send_message(chat_id, fancy_text, parse_mode="HTML", reply_markup=markup, disable_web_page_preview=True)

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription(call):
    if force_sub_check(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ تم التحقق! يمكنك استخدام البوت الآن.", show_alert=True)
        send_welcome(call.message)
    else: bot.answer_callback_query(call.id, "❌ لم تشترك بعد!", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data.startswith("country_"))
def handle_country_selection(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if is_banned(user_id): return
    if not force_sub_check(user_id): return

    parts = call.data.split("_")
    country_code = parts[1]
    combo_index = int(parts[2]) if len(parts) > 2 else 1
    
    available_numbers = get_available_numbers(country_code, combo_index, user_id)
    
    if not available_numbers:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 العودة لاختيار دولة أخرى", callback_data="back_to_countries"))
        bot.edit_message_text("<b>❌ نعتذر، جميع الأرقام قيد الاستخدام حالياً لهذه الدولة.</b>", chat_id, message_id, reply_markup=markup, parse_mode="HTML")
        return

    # سحب 5 أرقام
    numbers_to_assign = random.sample(available_numbers, min(5, len(available_numbers)))
    
    release_numbers(user_id)
    assign_numbers_to_user(user_id, numbers_to_assign)
    save_user(user_id, country_code=country_code, assigned_number=numbers_to_assign)
    
    name, flag, _ = COUNTRY_CODES.get(country_code, ("Unknown", "🌍", ""))
    nums_display = "\n".join([f"<code>+{num}</code>" for num in numbers_to_assign])
    
    msg_text = (
        f"<b>◈ Country:</b> {flag} {name}\n"
        f"<b>◈ Combo:</b> #{combo_index}\n"
        f"<b>◈ Numbers ({len(numbers_to_assign)}):</b>\n{nums_display}\n\n"
        f"<b>◈ Status :</b> ⏳ Waiting for SMS (أي كود يصل لأي رقم سيظهر لك فوراً هنا)"
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 قـنـاة الـبـوت", url="https://t.me/telegram"))
    markup.row(
        types.InlineKeyboardButton("🔄 Change Numbers", callback_data=f"change_num_{country_code}_{combo_index}"),
        types.InlineKeyboardButton("🔙 Back", callback_data="back_to_countries")
    )

    try:
        bot.edit_message_text(text=msg_text, chat_id=chat_id, message_id=message_id, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)
        bot.answer_callback_query(call.id, "✅ تم استلام 5 أرقام بنجاح")
    except Exception as e: print(f"Error: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("change_num_"))
def change_number(call):
    user_id = call.from_user.id
    if is_banned(user_id): return
    if not force_sub_check(user_id): return
        
    parts = call.data.split("_")
    country_code = parts[2]
    combo_index = int(parts[3]) if len(parts) > 3 else 1
    
    available_numbers = get_available_numbers(country_code, combo_index, user_id)
    if not available_numbers:
        bot.answer_callback_query(call.id, "❌ نعتذر، جميع الأرقام قيد الاستخدام حالياً.", show_alert=True)
        return

    numbers_to_assign = random.sample(available_numbers, min(5, len(available_numbers)))
    
    release_numbers(user_id)
    assign_numbers_to_user(user_id, numbers_to_assign)
    save_user(user_id, country_code=country_code, assigned_number=numbers_to_assign)
    
    name, flag, _ = COUNTRY_CODES.get(country_code, ("Unknown", "🌍", ""))
    nums_display = "\n".join([f"<code>+{num}</code>" for num in numbers_to_assign])
    
    msg_text = (
        f"<b>◈ Country:</b> {flag} {name}\n"
        f"<b>◈ Combo:</b> #{combo_index}\n"
        f"<b>◈ Numbers ({len(numbers_to_assign)}):</b>\n{nums_display}\n\n"
        f"<b>◈ Status :</b> ⏳ Waiting for SMS"
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 قـنـاة الـبـوت", url="https://t.me/telegram"))
    markup.row(
        types.InlineKeyboardButton("🔄 Change Numbers", callback_data=f"change_num_{country_code}_{combo_index}"),
        types.InlineKeyboardButton("🔙 Back", callback_data="back_to_countries")
    )

    try:
        bot.edit_message_text(text=msg_text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)
        bot.answer_callback_query(call.id, "🔄 تم تغيير الأرقام بنجاح 💯")
    except Exception as e: print(f"Error in change_number: {e}")

@bot.callback_query_handler(func=lambda call: call.data == "back_to_countries")
def back_to_countries(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons =[]
    user = get_user(call.from_user.id)
    private_combo = user[7] if user else None
    all_combos = get_all_combos()

    country_combos = {}
    for country_code, combo_index in all_combos:
        if country_code not in country_combos: country_combos[country_code] =[]
        country_combos[country_code].append(combo_index)

    if private_combo and private_combo in COUNTRY_CODES:
        name, flag, _ = COUNTRY_CODES[private_combo]
        buttons.append(types.InlineKeyboardButton(f"{flag} {name} (Private)", callback_data=f"country_{private_combo}_1"))

    for country_code, indices in country_combos.items():
        if country_code in COUNTRY_CODES and country_code != private_combo:
            name, flag, _ = COUNTRY_CODES[country_code]
            for idx in indices:
                btn_text = f"{flag} {name}" if len(indices) == 1 else f"{flag} {name} ({idx})"
                buttons.append(types.InlineKeyboardButton(btn_text, callback_data=f"country_{country_code}_{idx}"))

    for i in range(0, len(buttons), 2): markup.row(*buttons[i:i+2])
    if is_admin(call.from_user.id): markup.add(types.InlineKeyboardButton("🔐 Admin Panel", callback_data="admin_panel"))

    fancy_text = (
        "<b>❍────── <u> بـوت الأرقـام </u> ──────❍</b>\n\n"
        "<b>🔋 <u>أهـلاً بك عزيزي المستخدم في البوت</u></b>\n\n"
        "<b>🎓 <u>نـوفـر لـك أرقـام لـجـمـيـع الـدول</u></b>\n\n"
        "<b>────────────────────</b>\n"
        "<b><u>اخـتـر الــدولـة الـتـي تـريـدهـا مـن الـزر بالأسـفـل</u> ⬇️</b>"
    )
    try: bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=fancy_text, parse_mode="HTML", reply_markup=markup, disable_web_page_preview=True)
    except: pass

# ======================
# 🔐 لوحة التحكم الإدارية
# ======================
user_states = {}

def admin_main_menu():
    markup = types.InlineKeyboardMarkup()
    status_icon = "🟢" if not is_maintenance_mode() else "🔴"
    status_text = "الآن: يعمل بنجاح" if not is_maintenance_mode() else "الآن: قيد الصيانة"
    markup.add(types.InlineKeyboardButton(f"{status_icon} {status_text} {status_icon}", callback_data="toggle_maintenance"))
    markup.row(types.InlineKeyboardButton("📥 إضافة كومبو", callback_data="admin_add_combo"), types.InlineKeyboardButton("🗑️ حذف كومبو", callback_data="admin_del_combo"))
    markup.row(types.InlineKeyboardButton("📊 الإحصائيات", callback_data="admin_stats"), types.InlineKeyboardButton("📄 تقرير شامل", callback_data="admin_full_report"))
    markup.row(types.InlineKeyboardButton("📢 إذاعة عامة", callback_data="admin_broadcast_all"), types.InlineKeyboardButton("📨 إذاعة مخصصة", callback_data="admin_broadcast_user"))
    markup.row(types.InlineKeyboardButton("🚫 حظر", callback_data="admin_ban"), types.InlineKeyboardButton("✅ إلغاء حظر", callback_data="admin_unban"), types.InlineKeyboardButton("👤 معلومات", callback_data="admin_user_info"))
    markup.row(types.InlineKeyboardButton("🔗 إشتراك", callback_data="admin_force_sub"), types.InlineKeyboardButton("🔑 برايفت", callback_data="admin_private_combo"))
    markup.add(types.InlineKeyboardButton("🔙 مغادرة لوحة التحكم", callback_data="back_to_countries"))
    return markup

@bot.callback_query_handler(func=lambda call: call.data == "admin_panel")
def show_admin_panel(call):
    if not is_admin(call.from_user.id): return
    admin_text = "<b>👋 مرحباً بك يا مطور في لوحة التحكم.</b>\n<b>⚙️ يمكنك التحكم في كامل وظائف البوت من هنا.</b>"
    try: bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=admin_text, parse_mode="HTML", reply_markup=admin_main_menu())
    except: pass

@bot.callback_query_handler(func=lambda call: call.data == "admin_force_sub")
def admin_force_sub(call):
    if not is_admin(call.from_user.id): return
    channels = get_all_force_sub_channels(enabled_only=False)
    text = "⚙️ إدارة قنوات الاشتراك الإجباري:\n"
    markup = types.InlineKeyboardMarkup()
    for ch_id, url, desc in channels:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT enabled FROM force_sub_channels WHERE id=?", (ch_id,))
        enabled = c.fetchone()[0]
        conn.close()
        status = "✅" if enabled else "❌"
        markup.add(types.InlineKeyboardButton(f"{status} {desc or url[:25]}", callback_data=f"edit_force_ch_{ch_id}"))
    markup.add(types.InlineKeyboardButton("➕ إضافة قناة", callback_data="add_force_ch"))
    markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "toggle_maintenance")
def handle_maintenance_toggle(call):
    if not is_admin(call.from_user.id): return
    current_status = is_maintenance_mode()
    set_maintenance_mode(not current_status)
    bot.answer_callback_query(call.id, "🔓 تم فتح البوت للجميع" if current_status else "🔒 تم قفل البوت (وضع الصيانة)", show_alert=True)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=admin_main_menu())
    
@bot.callback_query_handler(func=lambda call: call.data == "add_force_ch")
def add_force_ch_step1(call):
    if not is_admin(call.from_user.id): return
    user_states[call.from_user.id] = "add_force_ch_url"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_force_sub"))
    bot.edit_message_text("أرسل رابط القناة (مثل: https://t.me/xxx أو @xxx):", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id) == "add_force_ch_url")
def add_force_ch_step2(message):
    url = message.text.strip()
    if not (url.startswith("@") or url.startswith("https://t.me/")):
        bot.reply_to(message, "❌ رابط غير صالح! يجب أن يبدأ بـ @ أو https://t.me/")
        return
    user_states[message.from_user.id] = {"step": "add_force_ch_desc", "url": url}
    bot.reply_to(message, "أدخل وصفًا للقناة (أو اترك فارغًا):")

@bot.message_handler(func=lambda msg: isinstance(user_states.get(msg.from_user.id), dict) and user_states[msg.from_user.id].get("step") == "add_force_ch_desc")
def add_force_ch_step3(message):
    data = user_states[message.from_user.id]
    if add_force_sub_channel(data["url"], message.text.strip()): bot.reply_to(message, f"✅ تم إضافة القناة")
    else: bot.reply_to(message, "❌ القناة موجودة مسبقًا!")
    del user_states[message.from_user.id]

@bot.callback_query_handler(func=lambda call: call.data.startswith("edit_force_ch_"))
def edit_force_ch(call):
    if not is_admin(call.from_user.id): return
    ch_id = int(call.data.split("_", 3)[3])
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT channel_url, description, enabled FROM force_sub_channels WHERE id=?", (ch_id,))
    row = c.fetchone()
    conn.close()
    if not row: return
    url, desc, enabled = row
    markup = types.InlineKeyboardMarkup()
    if enabled: markup.add(types.InlineKeyboardButton("❌ تعطيل", callback_data=f"toggle_ch_{ch_id}"))
    else: markup.add(types.InlineKeyboardButton("✅ تفعيل", callback_data=f"toggle_ch_{ch_id}"))
    markup.add(types.InlineKeyboardButton("🗑️ حذف", callback_data=f"del_ch_{ch_id}"))
    markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_force_sub"))
    bot.edit_message_text(f"🔧 إدارة القناة:\nالرابط: {url}\nالوصف: {desc}", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("toggle_ch_"))
def toggle_ch(call):
    ch_id = int(call.data.split("_", 2)[2])
    toggle_force_sub_channel(ch_id)
    admin_force_sub(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith("del_ch_"))
def del_ch(call):
    ch_id = int(call.data.split("_", 2)[2])
    delete_force_sub_channel(ch_id)
    admin_force_sub(call)

# ======================
# ⚙️ نظام التعرف الذكي على الدول ورفع الملفات
# ======================
def get_country_from_number(number):
    """نظام كشف ذكي يفحص من الكود الأطول إلى الأقصر"""
    num = clean_number(number)
    for code in SORTED_COUNTRY_PREFIXES:
        if num.startswith(code):
            return code
    return None

@bot.callback_query_handler(func=lambda call: call.data == "admin_add_combo")
def admin_add_combo(call):
    if not is_admin(call.from_user.id): return
    user_states[call.from_user.id] = "waiting_combo_file"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text("📤 أرسل ملف الكومبو بصيغة TXT", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.message_handler(content_types=['document'])
def handle_combo_file(message):
    if not is_admin(message.from_user.id) or user_states.get(message.from_user.id) != "waiting_combo_file": return
    try:
        file_info = bot.get_file(message.document.file_id)
        content = bot.download_file(file_info.file_path).decode('utf-8')
        lines =[line.strip() for line in content.splitlines() if line.strip()]
        
        if not lines: 
            return bot.reply_to(message, "❌ الملف فارغ!")
            
        first_num = clean_number(lines[0])
        country_code = get_country_from_number(first_num)
        
        if country_code:
            # التعرف التلقائي نجح
            save_combo(country_code, lines)
            name, flag, _ = COUNTRY_CODES[country_code]
            bot.reply_to(message, f"✅ تم تحديد الدولة تلقائياً وحفظ الكومبو:\nالدولة: {flag} {name}\n🔢 عدد الأرقام: {len(lines)}")
            del user_states[message.from_user.id]
        else:
            # التعرف التلقائي فشل -> تشغيل نظام الطوارئ
            user_states[message.from_user.id] = {"step": "waiting_manual_country", "lines": lines}
            bot.reply_to(message, "⚠️ لم أتمكن من تحديد الدولة تلقائياً من الأرقام.\n\nيرجى كتابة **رمز الدولة** يدوياً ( ليتم حفظ الملف.\nأو أرسل كلمة `إلغاء` لإلغاء العملية.", parse_mode="Markdown")
            
    except Exception as e: 
        bot.reply_to(message, f"❌ خطأ: {e}")

@bot.message_handler(func=lambda msg: isinstance(user_states.get(msg.from_user.id), dict) and user_states[msg.from_user.id].get("step") == "waiting_manual_country")
def handle_manual_country_code(message):
    if message.text.strip() == "إلغاء":
        bot.reply_to(message, "🚫 تم إلغاء رفع الملف.")
        del user_states[message.from_user.id]
        return

    manual_code = clean_number(message.text)
    if not manual_code:
        bot.reply_to(message, "❌ يرجى إرسال أرقام فقط لرمز الدولة (مثال: 967)")
        return

    data = user_states[message.from_user.id]
    lines = data["lines"]

    # إضافة الدولة مؤقتاً إذا لم تكن موجودة بقاعدة البيانات الشاملة
    if manual_code not in COUNTRY_CODES:
        COUNTRY_CODES[manual_code] = (f"Country +{manual_code}", "🏳️", "UN")

    save_combo(manual_code, lines)
    name, flag, _ = COUNTRY_CODES[manual_code]

    bot.reply_to(message, f"✅ تم حفظ الكومبو يدوياً بنجاح:\nالدولة: {flag} {name} (+{manual_code})\n🔢 عدد الأرقام: {len(lines)}")
    del user_states[message.from_user.id]


@bot.callback_query_handler(func=lambda call: call.data == "admin_del_combo")
def admin_del_combo(call):
    if not is_admin(call.from_user.id): return
    combos = get_all_combos()
    if not combos: return bot.answer_callback_query(call.id, "لا توجد كومبوهات!")
    markup = types.InlineKeyboardMarkup()
    for country_code, combo_index in combos:
        if country_code in COUNTRY_CODES:
            name, flag, _ = COUNTRY_CODES[country_code]
            markup.add(types.InlineKeyboardButton(f"{flag} {name} ({combo_index})", callback_data=f"del_combo_{country_code}_{combo_index}"))
        else:
            markup.add(types.InlineKeyboardButton(f"🏳️ +{country_code} ({combo_index})", callback_data=f"del_combo_{country_code}_{combo_index}"))
            
    markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text("اختر الكومبو للحذف:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("del_combo_"))
def confirm_del_combo(call):
    if not is_admin(call.from_user.id): return
    parts = call.data.split("_")
    delete_combo(parts[2], int(parts[3]) if len(parts) > 3 else 1)
    admin_del_combo(call)

@bot.callback_query_handler(func=lambda call: call.data == "admin_stats")
def admin_stats(call):
    if not is_admin(call.from_user.id): return
    combos = get_all_combos()
    total_numbers = sum(len(get_combo(cc, ci)) for cc, ci in combos)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="admin_panel"))
    bot.edit_message_text(f"📊 إحصائيات البوت:\n👥 المستخدمين: {len(get_all_users())}\n📞 إجمالي الأرقام: {total_numbers}", call.message.chat.id, call.message.message_id, reply_markup=markup)

# ======================
# 🔄 دوال المساعدة للبيانات
# ======================
def get_available_numbers(country_code, combo_index=1, user_id=None):
    all_numbers = get_combo(country_code, combo_index, user_id)
    if not all_numbers: return[]
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT assigned_number FROM users WHERE assigned_number IS NOT NULL AND assigned_number != ''")
    
    used_numbers = set()
    for row in c.fetchall():
        try:
            nums = json.loads(row[0])
            if isinstance(nums, list):
                used_numbers.update(nums)
        except:
            used_numbers.add(row[0])
    conn.close()
    
    return[num for num in all_numbers if num not in used_numbers]

def clean_number(number):
    if not number: return ""
    return re.sub(r'\D', '', str(number))

def extract_otp(message):
    patterns =[
        r'(?:code|رمز|كود|verification|تحقق|otp|pin)[:\s]+[‎]?(\d{3,8}(?:[- ]\d{3,4})?)',
        r'(\d{3})[- ](\d{3,4})',
        r'\b(\d{4,8})\b',
        r'[‎](\d{3,8})',
    ]
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            if len(match.groups()) > 1: return ''.join(match.groups())
            return match.group(1).replace(' ', '').replace('-', '')
    all_numbers = re.findall(r'\d{4,8}', message)
    if all_numbers: return all_numbers[0]
    return "N/A"

# ======================
# 👁️ دالة مطابقة آخر 4 أرقام من رسائل التخزين
# ======================
def get_user_by_text_match(text):
    """تبحث عن آخر 4 أرقام من الأرقام المسلمة للمستخدمين داخل نص الرسالة"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id, assigned_number FROM users WHERE assigned_number IS NOT NULL AND assigned_number != ''")
    rows = c.fetchall()
    conn.close()
    
    for row in rows:
        user_id = row[0]
        assigned_data = row[1]
        nums_list =[]
        try:
            parsed = json.loads(assigned_data)
            if isinstance(parsed, list):
                nums_list = parsed
            else:
                nums_list =[str(parsed)]
        except:
            nums_list =[str(assigned_data)]
            
        for number in nums_list:
            num_str = str(number).strip()
            if len(num_str) >= 4:
                last_4 = num_str[-4:]
                
                if f"•{last_4}" in text or f"*{last_4}" in text or f".{last_4}" in text or f" {last_4}" in text:
                    return user_id, num_str
                elif last_4 in text:
                    return user_id, num_str
                    
    return None, None

# ======================
# 📥 مستمع قروب التخزين
# ======================
@bot.message_handler(func=lambda msg: str(msg.chat.id) == STORAGE_GROUP_ID)
def handle_storage_group_message(message):
    text = message.text or message.caption
    if not text:
        return
        
    user_id, matched_number = get_user_by_text_match(text)
    
    if user_id:
        otp_code = extract_otp(text)
        
        keyboard = {
            "inline_keyboard": [[
                    {
                        "text": f"✌🏻 نسخ الكود: {otp_code}", 
                        "copy_text": {"text": str(otp_code)}
                    }
                ]
            ]
        }
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": user_id,
            "text": f"<b>🔔 رسالة جديدة لرقمك:</b> <code>+{matched_number}</code>\n\n{safe_html(text)}",
            "parse_mode": "HTML",
            "reply_markup": json.dumps(keyboard)
        }
        
        try:
            requests.post(url, data=payload)
            log_otp(matched_number, otp_code, text, user_id)
        except Exception as e:
            print(f"❌ خطأ في الإرسال للمستخدم: {e}")

# ======================
# ▶️ تشغيل البوت
# ======================
if __name__ == "__main__":
    print("🚀 البوت يعمل الآن ويراقب قروب التخزين...")
    bot.polling(none_stop=True)