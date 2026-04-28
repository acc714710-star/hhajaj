import time, redis, os, json, re, requests, asyncio
from pyrogram import Client, filters, idle, enums

token = "8478567517:AAGnC8yPwri7DxlMsN8E7ZZ4c1ymDE5r1Us"
owner_id = 7668115898

# وضعنا رابط الريدس من Upstash الخاص بك هنا
REDIS_URL = "rediss://default:gQAAAAAAARUvAAIgcDExYmQ2MTdkNjcxYTk0YzBlYjIyZTY3ZDc2MTBlMTJkYw@working-bluebird-70959.upstash.io:6379"

# الاتصال بقاعدة البيانات الخارجية
r = redis.from_url(REDIS_URL, decode_responses=True)

# قمنا بتعديل كتابة ملف الكونفق عشان البلوقنز تتصل بنفس القاعدة الخارجية وما يصير خطأ localhost
to_config = f"""
import redis
r = redis.from_url('{REDIS_URL}', decode_responses=True)
"""

print('Loading…')
print('\n')

Dev_Zaid = token.split(':')[0]
r.set(f'{Dev_Zaid}botowner', owner_id)

if not r.get(f'{Dev_Zaid}botowner'):
    r.set(f'{Dev_Zaid}botowner', owner_id)
else:
    owner_id = int(r.get(f'{Dev_Zaid}botowner'))

to_config += f"\ntoken = '{token}'"
to_config += f"\nDev_Zaid = token.split(':')[0]"
to_config += f"\nsudo_id = {owner_id}"

username = requests.get(f"https://api.telegram.org/bot{token}/getMe").json()["result"]["username"]
to_config += f"\nbotUsername = '{username}'"
to_config += "\nfrom kvsqlite.sync import Client as DB"
to_config += "\nytdb = DB('ytdb.sqlite')"
to_config += "\nsounddb = DB('sounddb.sqlite')"
to_config += "\nwsdb = DB('wsdb.sqlite')"

with open('config.py','w+') as w:
    w.write(to_config)

app = Client(f'{Dev_Zaid}r3d', 9398500, 'ad2977d673006bed6e5007d953301e13',
    bot_token=token,
    plugins={"root": "Plugins"},
)

if not r.get(f'{Dev_Zaid}:botkey'):
    r.set(f'{Dev_Zaid}:botkey', '⇜')

if not r.get(f'{Dev_Zaid}botname'):
    r.set(f'{Dev_Zaid}botname', 'رعد')

if not r.get(f'{Dev_Zaid}botchannel'):
    r.set(f'{Dev_Zaid}botchannel', 'eFFb0t')

def Find(text):
    m = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(m, text)
    return[x[0] for x in url]

app.start()

print('Bot started')

if r.get(f'DevGroup:{Dev_Zaid}'):
    id = int(r.get(f'DevGroup:{Dev_Zaid}'))
    try:
        app.send_message(id, "تم تشغيل البوت بنجاح ✔️")
    except:
        pass

idle()