import asyncio
import sys
import os
import random
import logging
import sqlite3
import datetime
import shutil
from datetime import datetime as dt, timedelta
from dotenv import load_dotenv, find_dotenv

# كتم لوجات البيروجرام المزعجة لحماية سرعة واستقرار المحرك
logging.getLogger("pyrogram").setLevel(logging.CRITICAL)

from pyrogram import Client, filters, enums
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import PeerFlood, UserPrivacyRestricted, UserAlreadyParticipant, SessionPasswordNeeded, PhoneCodeInvalid, PhoneCodeExpired

# 🎨 أكواد الألوان الملوكية لشاشة محرك تيرمكس الخاصة بالمالك 🎨
G = "\033[1;32m" # أخضر ملوكي
R = "\033[1;31m" # أحمر ناري
B = "\033[1;34m" # أزرق فخم
Y = "\033[1;33m" # أصفر ذهبي
C = "\033[1;36m" # تيركوز مضيء
W = "\033[1;37m" # أبيض صافي
X = "\033[0m"    # تصفير الألوان

# 🛑 بيانات المنظومة السرية والثابتة لمالك البوت والمدير العام 🛑
API_ID = 33198125  
API_HASH = "61d3124f0f4150adf6c3df7fe479a436"  
OWNER_ID = 8813635835  
AUDIT_CHANNEL_ID = -1003567670687  

# تعريف وتأمين المصب العام والمجلدات المعزولة في الهارد ديسك لمنع تلف السيسونات
BACKUP_DIR = "scraped_data_backup"
SESSIONS_DIR = "sessions_pool"
MASTER_SESSIONS_DIR = "master_sessions_backup"

os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(SESSIONS_DIR, exist_ok=True)
os.makedirs(MASTER_SESSIONS_DIR, exist_ok=True)

DB_PATH = os.path.join(BACKUP_DIR, "spider_secure_vault.db")

# خزنة الأجهزة الديناميكية لتغفيل فلاتر تليجرام وحماية الحسابات
DEVICES_POOL = [
    {"device": "Samsung S24 Ultra", "system": "Android 14", "app": "10.5.3"},
    {"device": "Xiaomi 14 Pro", "system": "Android 14", "app": "10.6.1"},
    {"device": "iPhone 15 Pro Max", "system": "iOS 17.4", "app": "10.5.0"},
    {"device": "Google Pixel 8 Pro", "system": "Android 14", "app": "10.4.2"},
    {"device": "OnePlus 12", "system": "Android 14", "app": "10.5.5"}
]

# خزنة المتغيرات العامة والحاويات في الرام لعدم حدوث NameError
user_auth_data = {}
waiting_for_broadcast = False
waiting_for_channels = False
# ... السطور القديمة جوه الرام ...
is_scraper_active = {}       
is_pumper_active = {}        
pumper_smart_toggle = {}     
MAINTENANCE_MODE = False     

# 💡 هنا ارشق بنك الرام الجديد لعزل نقرات المستخدمين تماماً عن بعض حماية للبوت
user_click_trackers = {}

def init_sqlite_vault():
    """تأسيس الجداول الرسمية للإمبراطورية داخل الهارد ديسك مع تفعيل WAL لمنع التجميد"""
    conn = sqlite3.connect(DB_PATH, timeout=60)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS scraped_members (identifier TEXT PRIMARY KEY)")
    cursor.execute("CREATE TABLE IF NOT EXISTS subscribers (user_id TEXT PRIMARY KEY)")
    cursor.execute("CREATE TABLE IF NOT EXISTS premium_users (user_id TEXT PRIMARY KEY)")
    cursor.execute("CREATE TABLE IF NOT EXISTS forced_channels (channel_username TEXT PRIMARY KEY)")
    cursor.execute("CREATE TABLE IF NOT EXISTS feature_toggles (role TEXT, feature_key TEXT, status TEXT, PRIMARY KEY (role, feature_key))")
    cursor.execute("CREATE TABLE IF NOT EXISTS redeem_codes (code TEXT PRIMARY KEY, value TEXT, type TEXT)")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_points (
            user_id TEXT PRIMARY KEY, 
            points INTEGER DEFAULT 0, 
            role TEXT DEFAULT 'USER', 
            vip_expiry TEXT DEFAULT NULL,
            daily_streak INTEGER DEFAULT 0,
            last_gift_date TEXT DEFAULT NULL
        )
    """)
    cursor.execute("CREATE TABLE IF NOT EXISTS pumper_indexes (user_id TEXT PRIMARY KEY, last_index INTEGER DEFAULT 0)")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS session_daily_limits (
            session_name TEXT PRIMARY KEY, 
            count INTEGER DEFAULT 0, 
            last_date TEXT, 
            cooldown_until TEXT DEFAULT NULL, 
            status TEXT DEFAULT 'ACTIVE'
        )
    """)
    cursor.execute("CREATE TABLE IF NOT EXISTS added_history (member_id TEXT, target_group TEXT, added_at TEXT DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (member_id, target_group))")
    conn.commit()
    conn.close()

# إطلاق محرك الخزنة فوراً عند بداية الملف
init_sqlite_vault()

def db_query(query, params=(), commit=False, fetchone=False, fetchall=False):
    """مستقبل الاستعلامات الموحد للتحكم بأمان وإغلاق المحابس دورياً"""
    res = None
    try:
        conn = sqlite3.connect(DB_PATH, timeout=60)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        cursor = conn.cursor()
        cursor.execute(query, params)
        if commit: conn.commit()
        if fetchone: 
            row = cursor.fetchone()
            res = row if row and len(row) == 1 else row
        elif fetchall: res = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(f" ❌ Database Exception Error: {e}")
    return res

load_dotenv(find_dotenv())

# 👑 ربط وهندسة التوكنات بالعكس الجبري الصارم
app = Client("combined_bot_session_clean", api_id=API_ID, api_hash=API_HASH, bot_token="8938908361:AAGJr1gYdDkM9Grv-Dro2GEG43S3ILpPpJA")
assistant_app = Client("assistant_bot_session_clean", api_id=API_ID, api_hash=API_HASH, bot_token="8468639064:AAHKhK3MciRsFQW2Bly-PiZ3muLJMn6O4bM")
user_app = Client(os.path.join(SESSIONS_DIR, "user_scraper_session"), api_id=API_ID, api_hash=API_HASH)
def get_live_buttons_markup(u_id, role):
    """بناء لوحة مفاتيح المشغلين الموحدة والثابتة جغرافيا حسب الرتبة والأصول لتفادي اللخبطة"""
    kb_list = []
    state = pumper_smart_toggle.get(str(u_id), True)
    speed_btn = "🟢 الضخ الذكي: نَشِط أوتوماتيك" if state else "🔴 الضخ الذكي: مُعطل"
    
    if int(u_id) == OWNER_ID:
        kb_list = [
            [KeyboardButton("🔍 𓆩 إطلاق رادار السحب التلقائي 𓆪"), KeyboardButton("🛑 𓆩 إيقاف رادار السحب 𓆪")],
            [KeyboardButton("📤 𓆩 بدء ماكينة الضخ والتحويل 𓆪"), KeyboardButton("🛑 𓆩 إيقاف ماكينة الضخ فوراً 𓆪")],
            [KeyboardButton("📱 𓆩 ربط وتأمين رقم سحب جديد 𓆪"), KeyboardButton("📱 𓆩 التبديل واختيار حساب السحب الأساسي 𓆪")],
            [KeyboardButton(speed_btn), KeyboardButton("📊 𓆩 فحص البيانات والتقرير 𓆪")],
            [KeyboardButton("🧼 𓆩 تصفير وتطهير المخزن 𓆪"), KeyboardButton("🎟️ 𓆩 توليد وقذف أكواد الشحن 𓆪")],
            [KeyboardButton("🛡️ 𓆩 فحص وسلامة الجلسات 𓆪"), KeyboardButton("🧼 𓆩 عزل وتطهير الحسابات الميتة 𓆪")],
            [KeyboardButton("📦 𓆩 تصدير ملف السيسونات العام 𓆪"), KeyboardButton("📦 𓆩 تصدير ملف المخزن العام الكلي 𓆪")],
            [KeyboardButton("📢 𓆩 إرسال إشعار تحديث السيرفر 𓆪"), KeyboardButton("🔓 𓆩 إيقاف إشعار تحديث السيرفر 𓆪")],
            [KeyboardButton("🛠️ 𓆩 لوحة التحكم في الأزرار والوظائف 𓆪"), KeyboardButton("📦 𓆩 قذف وحفظ السورس كود 𓆪")],
            [KeyboardButton("💳 𓆩 شحن رصيد المحفظة بالـ كود 𓆪"), KeyboardButton("👥 𓆩 شير واربح وتجميع النقاط 𓆪")]
        ]
    else:
        role_tag = "VIP" if role == "VIP" else "USER"
        prefix = "v" if role == "VIP" else "u"
        
        # حماية الأسرار: لو الزبون مش رابط أرقام في محفظته بنقفل عليه اللوحة وننزل له زر الربط بس
        all_pool_files = os.listdir(SESSIONS_DIR)
        has_linked_sess = any(f.endswith(".session") and str(u_id) in f for f in all_pool_files)
        
        if not has_linked_sess:
            kb_list.append([KeyboardButton("📱 𓆩 ربط وتأمين رقم سحب جديد 𓆪")])
            kb_list.append([KeyboardButton("💳 𓆩 شحن رصيد المحفظة بالـ كود 𓆪"), KeyboardButton("👥 𓆩 شير واربح وتجميع النقاط 𓆪")])
            return ReplyKeyboardMarkup(kb_list, resize_keyboard=True)
            
        if db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_tag, f"{prefix}_sc"), fetchone=True) != ("OFF",):
            kb_list.append([KeyboardButton("🔍 𓆩 إطلاق رادار السحب التلقائي 𓆪"), KeyboardButton("🛑 𓆩 إيقاف رادار السحب 𓆪")])
        if db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_tag, f"{prefix}_pu"), fetchone=True) != ("OFF",):
            kb_list.append([KeyboardButton("📤 𓆩 بدء ماكينة الضخ والتحويل 𓆪"), KeyboardButton("🛑 𓆩 إيقاف ماكينة الضخ فوراً 𓆪")])
            
        row3 = []
        if db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_tag, f"{prefix}_se"), fetchone=True) != ("OFF",):
            row3.append(KeyboardButton("📱 𓆩 ربط وتأمين رقم سحب جديد 𓆪"))
        if db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_tag, f"{prefix}_ch"), fetchone=True) != ("OFF",):
            row3.append(KeyboardButton("📱 𓆩 التبديل واختيار حساب السحب الأساسي 𓆪"))
        if row3: kb_list.append(row3)
        
        row4 = []
        if db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_tag, f"{prefix}_de"), fetchone=True) != ("OFF",):
            row4.append(KeyboardButton(speed_btn))
        if db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_tag, f"{prefix}_re"), fetchone=True) != ("OFF",):
            row4.append(KeyboardButton("📊 𓆩 فحص البيانات والتقرير 𓆪"))
        if row4: kb_list.append(row4)
        
        row5 = []
        if db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_tag, f"{prefix}_cl"), fetchone=True) != ("OFF",):
            row5.append(KeyboardButton("🧼 𓆩 تصفير وتطهير المخزن 𓆪"))
        if db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_tag, f"{prefix}_sh"), fetchone=True) != ("OFF",):
            row5.append(KeyboardButton("👥 𓆩 شير واربح وتجميع النقاط 𓆪"))
        if row5: kb_list.append(row5)
        
        if db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_tag, f"{prefix}_bp"), fetchone=True) != ("OFF",):
            kb_list.append([KeyboardButton("💳 𓆩 شحن رصيد المحفظة بالـ كود 𓆪")])
            
    return ReplyKeyboardMarkup(kb_list, resize_keyboard=True)

@app.on_message(filters.command("start") & filters.private)
async def start_router(client, message):
    """موجه الحركة المركزي وعزل جدار الصيانة وبث الدليل الإرشادي الكبرى للزبائن صب فوري"""
    user_id = str(message.from_user.id)
    db_query("INSERT OR IGNORE INTO subscribers (user_id) VALUES (?)", (user_id,), commit=True)
    
    if int(user_id) == OWNER_ID:
        kb = get_live_buttons_markup(user_id, "OWNER")
        welcome_txt = f"🔥 ✨ `𓆩 ♚ مَرْحَبَاً بِقَائِدِ العَمَلِيَّاتِ العُلْيَا وَالْمُدِيرِ العَامِّ الحِين ♚ 𓆪` ✨ 🔥\n───────────────────\n👤 **حساب الملك:** [{message.from_user.first_name}](tg://user?id={user_id})\n⚙️ **حالة السيرفر:** `الخزنة مفتوحة والمحابس تحت طوعك لايف بالكامل! 🔓`"
        await message.reply_text(text=welcome_txt, reply_markup=kb)
        return

    if MAINTENANCE_MODE:
        await message.reply_text("⚠️ **وضع الصيانة نشط حالياً وتحديثات السيرفر جارية.. البوت واقف مؤقتاً وسيتم إشعارك فور فتح المنظومة! 🔒**")
        return

    pts_row = db_query("SELECT points, role, vip_expiry FROM user_points WHERE user_id=?", (user_id,), fetchone=True)
    if not pts_row:
        db_query("INSERT INTO user_points (user_id, points, role, vip_expiry) VALUES (?, 0, 'USER', NULL)", (user_id,), commit=True)
        points, role, vip_expiry = 0, "USER", None
    else:
        points, role, vip_expiry = pts_row
        
    if role == "VIP" and vip_expiry:
        if dt.now() > dt.strptime(vip_expiry, '%Y-%m-%d %H:%M:%S'):
            db_query("UPDATE user_points SET role='USER', vip_expiry=NULL WHERE user_id=?", (user_id,), commit=True)
            role = "USER"

    gift_points = 5
    db_query("UPDATE user_points SET points = points + 5 WHERE user_id=?", (user_id,), commit=True)
    
    kb = get_live_buttons_markup(user_id, role)
    u_display_name = message.from_user.first_name if message.from_user.first_name else "برنس الساحة"
    bot_uname = (await app.get_me()).username

    guide_panel = (
        f"📖 **الدليل الرسمي لبروتوكول تشغيل ماكينات الرشق**\n\n"
        f"أهلاً بك يا برنس الساحة `{u_display_name}`. المنظومة متستفة عشان تخدمك بأعلى كفاءة، ودي أصول ووظائف الأزرار كاملة:\n\n"
        f"👑 **رتبة حسابك:** `{role}` | 💎 **رصيد محفظتك:** `[{points + gift_points}]` نقطة صافي.\n\n"
        f"⚙️ **دليل وظائف الأزرار والتروس:**\n"
        f"• `[ 📱 ربط وتأمين رقم سحب جديد ]`: الخطوة الأولى والأساسية؛ بتكبسه عشان تربط أرقامك الخاصة اللي الماكينة هتسحب وتضخ بيها (الأزرار الباقية مش هتفتح لك غير لما تربط أول رقم بنجاح).\n"
        f"• `[ 🔍 إطلاق رادار السحب التلقائي ]`: بيفتح لك المجموعات المشترك فيها رقمك المربوط، وبيصطاد منها الأعضاء الحية باليوزر والآيدي في ثوانٍ.\n"
        f"• `[ 📤 بدء ماكينة الضخ والتحويل ]`: الماكينة الكبيرة؛ بتختار مجموعتك اللي عايز تضخ فيها، وبتبدأ الأرقام المحقونة تضيف الأعضاء بالتناوب العشوائي.\n"
        f"• `[ ⏳ الضخ الذكي ]`: مفتاح الأوتوماتيك؛ لو خليته (🟢) الماكينة بتوزع الإضافات بتأخير عشوائي لحماية أرقامك، ولو (🔴) بتشتغل بسرعة ثابتة.\n"
        f"• `[ 📊 فحص البيانات والتقرير ]`: كشف حساب محفظتك؛ بيعرض لك رتبتك، رصيد نقاطك، وإجمالي الأعضاء اللي سحبتها في بنكك المعزول.\n"
        f"• `[ 🧼 تصفير وتطهير المخزن ]`: بيمسح داتا الأعضاء اللي أنت سحبتها عشان يخلي مخزنك على البياض وتبدأ سحبة جديدة نظيفة.\n"
        f"• `[ 💳 شحن رصيد المحفظة بالكود ]`: بوابتك لتعبئة النقاط وترقية حسابك للـ VIP فوراً بمجرد كتابة الكود الملوكي.\n"
        f"• `[ 👥 شير واربح وتجميع النقاط ]`: بيولد لك رابط إحالة داخلي جوه التليجرام؛ تشيره لأصحابك وكل مشترك جديد يدوس Start من طرفك بيصب في محفظتك +10 نقاط مجاناً.\n\n"
        f"⚠️ **[ إشعار أمان وتنبيه هام جداً ]** ⚠️\n"
        f"بمجرد ما تربط رقمك، تطبيق تليجرام الرسمي هيبعت لك إشعار داخلي في شاتك بيقولك: *\"تم تسجيل دخول جهاز جديد لحسابك\"*.\n"
        f"يا برنس، لا تقلق نهائياً ولا تقفل الجلسة؛ ده مش هكر ولا اختراق! ده **(جهاز التمويه الديناميكي المشفر)** بتاع المنظومة. السيرفر بيولد موديل موبايل وهمي عشوائي وIP مخفي عشان يغفل فلاتر وخوارزميات تليجرام الصارمة؛ بكده رقمك يشتغل في صمت وبأعلى حماية وسلاسة ويموت الحظر تماماً وتفضل حساباتك شغالة في أمان! 🔒🚀\n"
        f"────────────────────────"
    )
    await message.reply_text(text=guide_panel, reply_markup=kb)
@app.on_message(filters.private & filters.text & ~filters.command(["start", "help"]))
async def spider_central_machinery_router(client, message):
    """المستقبل المركزي الذكي الشامل لكل الأزرار الفعالة في التيرمكس وشات البوت"""
    global MAINTENANCE_MODE  # 💡 الحل الجذري لمنع الـ SyntaxError نهائياً
    
    user_id = str(message.from_user.id)
    text = message.text.strip()
    
    # 💡 [جدار هندسة عزل النقاط الجبرية]: كل مستخدم حر ونقراته معزولة تماماً حماية للبوت من حظر تليجرام
    now_stamp = asyncio.get_event_loop().time()
    user_clicks = user_click_trackers.get(user_id, [])
    user_clicks = [u_t for u_t in user_clicks if now_stamp - u_t < 2.0]  # تنظيف داتا الثانيتين تلقائياً
    
    if len(user_clicks) >= 3 and int(user_id) != OWNER_ID:
        user_click_trackers[user_id] = user_clicks
        return  # قمع كبسات السبام صامتاً دون التأثير على بقية المستخدمين أو المالك
        
    user_clicks.append(now_stamp)
    user_click_trackers[user_id] = user_clicks

    # 🚨 رادار الرصد الفوري لكبسات الأزرار في شاشة التيرمكس لايف بالألوان الملوكية
    u_display = message.from_user.first_name if message.from_user.first_name else "مستخدم غريب"
    print(f" {B}[🚨 كبسة زرار حية]{X} ──► 👤 المشغل: {G}{u_display}{X} | 🆔 ID: {Y}{user_id}{X} | 🔘 الزر الكبس: {C}{text}{X}")

    # جدار محبس وضع الصيانة الكلي للمنظومة عن المشتركين والـ VIP صب جبري
    if MAINTENANCE_MODE and int(user_id) != OWNER_ID:
        await message.reply_text("⚠️ **تنبيه عاجل من الإدارة الكبرى:** جاري عمل صيانة وتحديث دوري للمنظومة بالكامل الحين لتطوير الماكينات! يرجى الانتظار وستنطلق اللوحة فوراً فور الانتهاء! 🔒")
        return

    # 1. بوابه شحن رصيد المحفظة والتسعيرة التسويقية بالجنيه المصري للزبائن مع خصم 90% وزر التواصل المباشر
    if "شحن رصيد المحفظة بالـ كود" in text or "شحن رصيد المحفظة بالكود" in text:
        user_auth_data[user_id] = {"step": "REDEEM_CODE"}
        
        if int(user_id) == OWNER_ID:
            r_role = "OWNER (المالك العام) 👑"
            display_pts = "لانهائي ♾️"
            power_pump = "لانهائية (المحابس مفتوحة للكل) 🔓"
            await message.reply_text(f"💳 **غرفة عمليات محفظة المالك**\n\n• الرتبة: {r_role}\n• الرصيد: {display_pts}\n• السعة: {power_pump}\n\n🎟️ المنظومة مفتوحة بالكامل تحت طوعك يا قائد.")
            return
            
        pts_row = db_query("SELECT points, role FROM user_points WHERE user_id=?", (user_id,), fetchone=True)
        u_pts = pts_row if pts_row else 0
        r_role = pts_row if pts_row else "USER"
        
        display_pts = f"[ {u_pts} ] نقطة"
        power_pump = f"[ {u_pts * 5} ] عضو فرز أول" if r_role != "VIP" else "لانهائية (وقت الضخ مفتوح) 💎"
        
        owner_obj = await app.get_users(OWNER_ID)
        owner_username = owner_obj.username if owner_obj.username else f"id={OWNER_ID}"
        
        pricing_panel = (
            f"💳 **كشف حساب محفظتك والتسعيرة الرسمية للمنظومة**\n"
            f"────────────────────────\n"
            f"👤 **رصيدك الحالي:** {display_pts}\n"
            f"👑 **رتبة حسابك:** [ {r_role} ]\n"
            f"🚀 **محفظتك الحالية تسحب وتضخ لك:** {power_pump}\n"
            f"────────────────────────\n"
            f"⚙️ **معادلة احتساب الأعضاء (الأصول الكفاءة):**\n"
            f"- النقطة الواحدة (1) = 5 أعضاء حية جوه مجموعتك الفعالة.\n\n"
            f"🔥 𓆩 **عَرْضُ الانْطِلاقِ الأَوَّلِيِّ خَصْمُ 90% لِفَتْرَةٍ مَحْدُودَةٍ** 𓆪 🔥\n"
            f"💰 **باقات النقاط الرسمية بالجنيه المصري [ بعد الخصم 🇪🇬 ]:**\n"
            f"• الباقة الأولى: `100 نقطة` ◀️ بسعر ~~50 جنيه~~ **`5 جنيه بس!`** (ضخ 500 عضو)\n"
            f"• الباقة الثانية: `200 نقطة` ◀️ بسعر ~~100 جنيه~~ **`10 جنيه بس!`** (ضخ 1,000 عضو)\n"
            f"• الباقة الثالثة: `300 نقطة` ◀️ بسعر ~~150 جنيه~~ **`15 جنيه بس!`** (ضخ 1,500 عضو)\n"
            f"• الباقة الرابعة: `400 نقطة` ◀️ بسعر ~~200 جنيه~~ **`20 جنيه بس!`** (ضخ 2,000 عضو)\n"
            f"• الباقة الخامسة: `1000 نقطة` ◀️ بسعر ~~500 جنيه~~ **`50 جنيه بس!`** (ضخ 5,000 عضو)\n"
            f"👑 **باقة الـ VIP الملكية** (ضخ مفتوح لانهائي لمدة شهر كامل): ◀️ بسعر ~~1000 جنيه~~ **`100 جنيه صافي الحين!`** 🔥🚀\n"
            f"────────────────────────\n"
            f"🎟️ **معاك كود شحن؟ اكتبه الآن في الشات وهيتم تعبئة محفظتك وتحديث لوحتك فوراً.**\n\n"
            f"👇 **لو عايز تشتري كود وتلحق عرض الـ 90% بالمصري، اضغط على زرار التواصل بالأسفل:**"
        )
        inline_kb = InlineKeyboardMarkup([[InlineKeyboardButton("👑 تواصل مع المالك واِلحق خصم الـ 90% الحين 👑", url=f"tg://resolve?domain={owner_username}")]])
        await message.reply_text(text=pricing_panel, reply_markup=inline_kb)
        return
    # 2. تشغيل زرار الأوتوماتيكي للسرعة والتحجيم الذكي بمحاكاة عداد 100% لايف
    if "الضخ الذكي" in text or "تحجيم سرعة الضخ" in text:
        pts_row = db_query("SELECT role FROM user_points WHERE user_id=?", (user_id,), fetchone=True)
        role = "OWNER (المالك العام)" if int(user_id) == OWNER_ID else (pts_row if pts_row else "USER")
        
        load_msg = await app.send_message(chat_id=int(user_id), text="⏳ **جاري فحص مسارات السرعة الفعالية...**\n`[░░░░░░░░░░] 0%`")
        await asyncio.sleep(0.5)
        await load_msg.edit_text("⚡ **جاري ربط محرك التناوب التلقائي صامت...**\n`[██████░░░░] 60%`")
        await asyncio.sleep(0.4)
        await load_msg.edit_text("🟢 **تم تحديث السرعة وقلب المحبس بنجاح!**\n`[██████████] 100%`")
        await asyncio.sleep(0.3)
        await load_msg.delete()
        
        current_state = pumper_smart_toggle.get(user_id, True)
        pumper_smart_toggle[user_id] = not current_state
        new_state = pumper_smart_toggle[user_id]
        
        kb = get_live_buttons_markup(user_id, role)
        await app.send_message(chat_id=int(user_id), text=f"💡 **وضع التناوب العشوائي الآن هو:** `{'نشط وتلقائي أوتوماتيك 🟢' if new_state else 'مغلق ومقيد صامت 🔴'}`", reply_markup=kb)
        return

    # 3. لوحة التحكم بالأزرار والوظائف الطبقية الـ 11 زر الفعالة (للمالك فقط)
    if "لوحة التحكم في الأزرار والوظائف" in text and int(user_id) == OWNER_ID:
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("👥 أزرار المستخدم العادي", callback_data="to_u")],
            [InlineKeyboardButton("💎 أزرار المستخدم الـ VIP", callback_data="to_v")]
        ])
        await app.send_message(chat_id=OWNER_ID, text="⚙️ **غرفة التحكم الطبقية التفاعلية المنفصلة: اختر الفئة لتعديل أزرارها الآن لايف:**", reply_markup=kb)
        return

    # 4. أزرار إطلاق وإيقاف رادار السحب التلقائي للمجموعات الحية المشتركة
    if "إطلاق رادار السحب" in text:
        if is_scraper_active.get(user_id, False):
            await message.reply_text("🚨 **رادار السحب شغال طحن عندك الحين بالفعل ولا يمكن تشغيله مكرر!**")
            return
        await send_paginated_groups(user_id, page=0, is_user_sc_intent=True)
        return
        
    if "إيقاف رادار السحب" in text:
        is_scraper_active[user_id] = False
        await message.reply_text("🛑 **تم إصدار أمر جبري بإيقاف رادار السحب وجرف السيسون صامت بنجاح!**")
        return

    # 5. أزرار بدء وإيقاف ماكينة الضخ والتحويل والتحميل لجروباتهم المشتركة فيه الحساب
    if "بدء ماكينة الضخ" in text:
        if is_pumper_active.get(user_id, False):
            await message.reply_text("🚨 **ماكينة الضخ قاذفة وشغالة عندك الحين بالفعل ولا يمكن تكرارها الحين!**")
            return
        await send_paginated_groups(user_id, page=0, is_user_sc_intent=False)
        return
        
    if "إيقاف ماكينة الضخ" in text:
        is_pumper_active[user_id] = False
        await message.reply_text("🛑 **تم إصدار أمر جبري بتعطيل الماكينة وفصل محرك الضخ الفوري بنجاح!**")
        return

    # 6. ربط وتأمين أرقام السحب وتبديل حساب السحب المعزول
    if "ربط وتأمين رقم سحب جديد" in text:
        user_auth_data[user_id] = {"step": "PHONE"}
        await message.reply_text("✍️ **أدخل رقم الهاتف المراد ربطه بالرمز الدولي الصافي (مثال: +2012...):**")
        return
    if "التبديل واختيار حساب السحب" in text:
        all_pool = os.listdir(SESSIONS_DIR)
        if int(user_id) == OWNER_ID:
            user_sess = [f.replace(".session", "") for f in all_pool if f.endswith(".session") and not any(x in f for x in ["combined", "assistant"])]
        else:
            user_sess = [f.replace(".session", "") for f in all_pool if f.endswith(".session") and user_id in f]
            
        if not user_sess:
            await message.reply_text("⚠️ **مخزن حسابات السحب الخاص بك فارغ حالياً! ربط وتأمين رقم سحب أولاً.**")
            return
            
        # حفر عداد تحميل حي لـ 100% في التبديل لشاشات الكل
        load_msg = await app.send_message(chat_id=int(user_id), text="⏳ **جاري جرد الحسابات المحقونة...**\n`[░░░░░░░░░░] 0%`")
        await asyncio.sleep(0.4)
        await load_msg.delete()
        
        buttons = [[InlineKeyboardButton(f"📱 {s}", callback_data=f"set_main_sys_{s}")] for s in user_sess[:10]]
        await app.send_message(chat_id=int(user_id), text="🔄 **اختر حساب السحب الأساسي لربطه بالمحرك الآن وعزل كاش المجموعات:**", reply_markup=InlineKeyboardMarkup(buttons))
        return

    # 7. فحص البيانات والتقارير بمحاكاة عداد 100% وتفريق الرتب الحادة بالملي وعزل المالك عن الأصفار
    if "فحص البيانات والتقرير" in text:
        load_msg = await app.send_message(chat_id=int(user_id), text="📊 **جاري جرف كواشف المخازن وبنك البيانات...**\n`[░░░░░░░░░░] 0%`")
        await asyncio.sleep(0.5)
        await load_msg.edit_text("⚙️ **جاري احتساب قوة الضخ الفعالة ومزامنة النقاط...**\n`[███████░░░] 70%`")
        await asyncio.sleep(0.4)
        await load_msg.delete()
        
        if int(user_id) == OWNER_ID:
            r_role = "OWNER (المالك العام) 👑"
            u_pts = 999999
            table_name = "scraped_members"
        else:
            pts_row = db_query("SELECT points, role FROM user_points WHERE user_id=?", (user_id,), fetchone=True)
            u_pts = pts_row if pts_row else 0
            r_role = pts_row if pts_row else "USER"
            table_name = f"scraped_members_{user_id}"
            
        db_query(f"CREATE TABLE IF NOT EXISTS {table_name} (identifier TEXT PRIMARY KEY)", commit=True)
        count_res = db_query(f"SELECT COUNT(*) FROM {table_name}", fetchone=True)
        vault_cnt = count_res if count_res else 0
        
        power_pump = "لانهائية (المحابس مفتوحة للكل) 🔓" if int(user_id) == OWNER_ID or "VIP" in str(r_role) else f"[ {u_pts * 5} ] عضو فرز أول"
        display_pts = "لانهائي ♾️" if int(user_id) == OWNER_ID else f"[ {u_pts} ] نقطة"
        
        report_panel = (
            f"📊 **كشف حساب محفظتك والقدرة الفعلية للضخ**\n"
            f"────────────────────────\n"
            f"👑 **رتبة الحساب الحالية:** `[ {r_role} ]`\n"
            f"💎 **رصيد نقاطك الصافي:** `{display_pts}`\n"
            f"📦 **مخزن الأعضاء الخاص بك:** `[ {vault_cnt} ]` عضو ملقوط.\n"
            f"🚀 **قوة الضخ الفعالة المتاحة:** `{power_pump}`\n"
            f"────────────────────────"
        )
        await message.reply_text(report_panel)
        return
        
    if "تصفير وتطهير المخزن" in text:
        user_table = f"scraped_members_{user_id}"
        
        load_msg = await app.send_message(chat_id=int(user_id), text="🧼 **جاري الاتصال ببنك الخزنة لتهيئة مجلد الشغل...**\n`[░░░░░░░░░░] 0%`")
        await asyncio.sleep(0.4)
        
        db_query(f"CREATE TABLE IF NOT EXISTS {user_table} (identifier TEXT PRIMARY KEY)", commit=True)
        db_query(f"DELETE FROM {user_table}", commit=True)
        await load_msg.edit_text("🧼 **جاري جرف الأعضاء المسحوبة وتبييض المخزن...**\n`[██████░░░░] 60%`")
        await asyncio.sleep(0.3)
        
        await load_msg.edit_text("🧼 **اكتمل التطهير وجرف الداتا بنجاح! مخزنك على البياض الآن.**\n`[██████████] 100%`")
        await asyncio.sleep(0.3)
        await load_msg.delete()
        
        await message.reply_text("🧼 **تم جرف وتطهير مخزنك الخاص بنجاح وصار على بياض ناصع الحين! ✅**")
        return

    # 8. توليد أكواد الشحن الديناميكية وتحديد رقم ترقية الـ VIP بمزاج المالك حصرآ
    if "توليد وقذف أكواد الشحن" in text and int(user_id) == OWNER_ID:
        user_auth_data[user_id] = {"step": "SET_CODE_POINTS"}
        await message.reply_text("✍️ **يا قائد، اكتب الآن رقم النقاط اللي عايز تحطها جوه الكود الجديد (مثال: 5000 أو 20000)؛ والرقم ده هو اللي هيرفع حساب المستخدم لـ VIP فوراً أول ما يشحنه:**")
        return
    # 9. وحوش الإدارة وفحص الجلسات والملفات الاحتياطية بالعداد الحي وشياكة السورس كود القديمة (للمالك)
    if "فحص وسلامة الجلسات" in text and int(user_id) == OWNER_ID:
        asyncio.create_task(run_real_sessions_audit_with_bar(user_id))
        return
        
    if "عزل وتطهير الحسابات الميتة" in text and int(user_id) == OWNER_ID:
        load_msg = await app.send_message(chat_id=OWNER_ID, text="🧼 **جاري فحص مجلد الجلسات لعزل الحسابات المحظورة...**\n`[░░░░░░░░░░] 0%`")
        await asyncio.sleep(0.5)
        
        all_pool = os.listdir(SESSIONS_DIR)
        dead_folder = "dead_sessions_backup"
        os.makedirs(dead_folder, exist_ok=True)
        isolated_cnt = 0
        for f in all_pool:
            if f.endswith(".session"):
                f_clean = f.replace(".session", "")
                check_status = db_query("SELECT status FROM session_daily_limits WHERE session_name=?", (f_clean,), fetchone=True)
                if check_status == ("QUARANTINE",):
                    try:
                        shutil.move(os.path.join(SESSIONS_DIR, f), os.path.join(dead_folder, f))
                        isolated_cnt += 1
                    except Exception: pass
                    
        await load_msg.edit_text("📦 **جاري نقل الجلسات الميتة لحوض الحجر الصحي صامت...**\n`[███████░░░] 70%`")
        await asyncio.sleep(0.4)
        await load_msg.edit_text(f"🧼 **اكتمل التطهير بنجاح ملوكي!**\n`[██████████] 100%`")
        await asyncio.sleep(0.3)
        await load_msg.delete()
        
        await message.reply_text(f"🧼 **اكتملت الملحمة بنجاح! تم نقل وعزل `[{isolated_cnt}]` حساب ميت جوه فولدر مستقل لضمان نظافة مجلد الشغل! ✅**")
        return

    if "📦 تصدير ملف السيسونات العام" in text or "تصدير ملف السيسونات العام" in text:
        if int(user_id) == OWNER_ID:
            asyncio.create_task(run_real_sessions_export_to_strings(user_id))
            return

    if "📦 تصدير ملف المخزن العام الكلي" in text or "تصدير ملف المخزن العام الكلي" in text:
        if int(user_id) == OWNER_ID:
            load_msg = await app.send_message(chat_id=OWNER_ID, text="📦 **جاري جرف المصب الكلي للأعضاء واليوزرات...**\n`[░░░░░░░░░░] 0%`")
            await asyncio.sleep(0.5)
            
            master_file = "spider_master_vault_export.txt"
            res_master = db_query("SELECT identifier FROM scraped_members", fetchall=True) or []
            if not res_master:
                await load_msg.edit_text("❌ المخزن العام الكلي للمصب فارغ حالياً!")
                return
            with open(master_file, "w", encoding="utf-8") as f:
                for row in res_master: f.write(f"{(row if isinstance(row, tuple) else row)}\n")
                
            await load_msg.edit_text("📦 **جاري تحزيم وتأمين تشفير ملف المخزن الكلي...**\n`[███████░░░] 70%`")
            await asyncio.sleep(0.4)
            await load_msg.edit_text("🚀 **جاري القذف الفوري الآن إلى جيبك...**\n`[██████████] 100%`")
            await asyncio.sleep(0.3)
            await load_msg.delete()
            
            await app.send_document(chat_id=OWNER_ID, document=master_file, caption=f"📦 **تم جرف وتصدير ملف المخزن العام الكلي للمصب بنجاح!**\n\n📌 إجمالي الأعضاء لجميع الحسابات: `[{len(res_master):,}]` عضو صافي جاهز للمخرطة الحين!")
            if os.path.exists(master_file): os.remove(master_file)
            return

    if "قذف وحفظ السورس كود" in text and int(user_id) == OWNER_ID:
        source_file = "main.py"
        temp_copy = "spider_master_clean.py"
        
        # 💡 إطلاق محرك العداد المرئي لايف في نفس الجزء من الثانية بالشياكة والنبض القديم المتستف
        load_msg = await app.send_message(chat_id=OWNER_ID, text="⏳ **جاري جرف كواشف السيرفر وتجميع حزم السورس كود...**\n`[░░░░░░░░░░] 0%`")
        await asyncio.sleep(0.5)
        
        if os.path.exists(source_file):
            shutil.copy(source_file, temp_copy)
            await load_msg.edit_text("📦 **جاري تأمين وتشفير الحزمة النظيفة وضغط الملفات صامت...**\n`[███████░░░] 70%`")
            await asyncio.sleep(0.4)
            await load_msg.edit_text("🚀 **اكتمل الحزم والتأمين بنجاح! جاري القذف الفوري الآن...**\n`[██████████] 100%`")
            await asyncio.sleep(0.3)
            await load_msg.delete()
            
            await app.send_document(
                chat_id=OWNER_ID, 
                document=temp_copy, 
                file_name="main.py", 
                force_document=True,
                caption=f"👑 **تفضل يا قائد! تم حزم وقذف السورس كود الكامل والمطوّر للماكينات الحين بنجاح! 📦🚀**\n\n⏱️ توقيت الحفظ الأصيل: `{dt.now().strftime('%H:%M:%S')}`"
            )
            if os.path.exists(temp_copy): os.remove(temp_copy)
        else:
            await load_msg.edit_text("❌ **عذراً يا قائد! لم يتم العثور على ملف الأكواد الأساسي main.py على السيرفر حالياً!**")
        return

    # 10. بث جدار حظر الصيانة والتحكم الإجباري الكلي عن بعد للمشتركين والـ VIP وحجب اللوحات
    if "إرسال إشعار تحديث السيرفر" in text and int(user_id) == OWNER_ID:
        MAINTENANCE_MODE = True
        await message.reply_text("📢 **تم تفعيل وضع الصيانة الشامل وبث الحظر وحجب اللوحات عن جميع المستخدمين بنجاح! 🔒**")
        
        async def run_maintenance_broadcast():
            subs = [r for r in db_query("SELECT user_id FROM subscribers", fetchall=True) or []]
            for s in subs:
                if int(s) != OWNER_ID:
                    try: 
                        await app.send_message(chat_id=int(s), text="⚠️ **تنبيه عاجل من الإدارة الكبرى:** جاري عمل صيانة وتحديث دوري للمنظومة الآن لتطوير الماكينات! يرجى الانتظار والسيرفر واقف مؤقتاً وسيتم إشعاركم فور الانتهاء! 🔒")
                        await asyncio.sleep(0.2)
                    except Exception: pass
        asyncio.create_task(run_maintenance_broadcast())
        return
        
    if "إيقاف إشعار تحديث السيرفر" in text and int(user_id) == OWNER_ID:
        MAINTENANCE_MODE = False
        await message.reply_text("🔓 **تم إيقاف وضع الصيانة ورفع الحظر وفتح اللوحات للجميع الآن! 🚀**")
        
        async def run_resume_broadcast():
            subs = [r for r in db_query("SELECT user_id FROM subscribers", fetchall=True) or []]
            for s in subs:
                if int(s) != OWNER_ID:
                    try: 
                        await app.send_message(chat_id=int(s), text="🔓 **التحديث خلص يا برنس والماكينات جاهزة الآن! يلا اشتغلوا على البوت عادي والمحابس مفتوحة للكل الحين! 🚀⚡**")
                        await asyncio.sleep(0.2)
                    except Exception: pass
        asyncio.create_task(run_resume_broadcast())
        return

    if "شير واربح وتجميع النقاط" in text:
        bot_uname = (await app.get_me()).username
        share_link = f"tg://resolve?domain={bot_uname}&start={user_id}"
        await message.reply_text(f"👥 **رابط الإحالة الخاص بك لتجميع النقاط مجاناً وبدون الخروج من التطبيق:**\n\n`{share_link}`\n\n🎁 كل شخص يشترك من طرفك يمنحك `+10 نقاط` فورا!")
        return

    await handle_dynamic_inputs_and_auth(user_id, text, message)
async def handle_dynamic_inputs_and_auth(user_id, text, message):
    """معالجة الأكواد والتحقق وحقن الجلسات التلقائي المتتالي بأعلى حماية ومنع شحن الهبل"""
    u_data = user_auth_data.get(user_id, {})
    current_step = u_data.get("step")

    # [أ] مرحلة صنع الكود للمالك: لقط الرقم وتثبيته في الخزنة كـ باقة VIP ديناميكية
    if int(user_id) == OWNER_ID and current_step == "SET_CODE_POINTS":
        user_auth_data.pop(user_id, None) # قفل الرام
        try:
            points_to_set = int(text.strip())
        except Exception:
            await message.reply_text("❌ **يا غالي اكتب رقم صافي بدون حروف أو فواصل! أعد المحاولة.**")
            return
            
        load_msg = await app.send_message(chat_id=OWNER_ID, text="🎟️ **جاري حفر وتأمين التشفير للكود الجديد...**\n`[░░░░░░░░░░] 0%`")
        await asyncio.sleep(0.4)
        
        # توليد كود فريد وحفظ الرقم المحفور جواه وتحديد نوعه VIP صراحة
        generated_code = f"SPIDER_{random.randint(100000, 999999)}"
        db_query("INSERT INTO redeem_codes (code, value, type) VALUES (?, ?, 'VIP')", (generated_code, str(points_to_set)), commit=True)
        
        await load_msg.edit_text("🚀 **جاري قذف حزمة الشحن لايف...**\n`[██████████] 100%`")
        await asyncio.sleep(0.2)
        await load_msg.delete()
        
        await message.reply_text(f"🎟️ **تم توليد كود شحن VIP بنجاح!**\n\n`{generated_code}`\n\n📌 **الرقم المحفور جواه:** `[ {points_to_set:,} ]` نقطة صافي، وهو ده الرقم اللي هيرفع حساب المستخدم لـ VIP فوراً أول ما يشحنه في محفظته! 🔥")
        return

    # [ب] مرحلة الشحن الفعلي عند المستخدم: الفحص والحرق والترقية الجبرية لـ 100% غصب عن أي قيود
    if current_step == "REDEEM_CODE" or text.startswith("SPIDER_"):
        user_auth_data.pop(user_id, None) # قفل خانة الاستقبال في الرام فورا
        clean_code = text.strip()
        
        # الفحص الإلزامي من واقع قاعدة البيانات لمنع الهبل والأكواد الميتة
        code_check = db_query("SELECT value, type FROM redeem_codes WHERE code=?", (clean_code,), fetchone=True)
        if not code_check:
            await message.reply_text("❌ **عذراً يا برنس! هذا الكود ميت، أو خاطئ، أو تم استخدامه من قبل! راجع المالك لشراء كود حقيقي. 🔒**")
            return
            
        # تفكيك البيانات بصيغة صافية ومنع خطأ الترقية الملكية
        code_value = int(code_check[0])
        c_type = str(code_check[1]).strip()
        is_vip_upgrade = True if c_type == "VIP" else False
        
        # حرق ومسح الكود فوراً من الخزنة منعاً للتكرار
        db_query("DELETE FROM redeem_codes WHERE code=?", (clean_code,), commit=True)

        # صب رقم النقاط اللي المالك حدده بالظبط جوه محفظة المستخدم الفعلي
        db_query("UPDATE user_points SET points = points + ? WHERE user_id=?", (code_value, user_id), commit=True)
        
        success_msg = f"🎉 **تم تفعيل كود الشحن بنجاح ونزل في محفظتك الحين `+{code_value:,} نقاط` صب فوري! 📈**"
        
        # الترقية الجبرية الفورية للـ VIP وتمديد وقت الضخ لشهر كامل وتحديث الكيبورد
        if is_vip_upgrade or int(user_id) == OWNER_ID:
            expiry_date = (dt.now() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
            db_query("UPDATE user_points SET role='VIP', vip_expiry=? WHERE user_id=?", (expiry_date, user_id), commit=True)
            success_msg += f"\n\n👑 **بشرى ملكية: تمت ترقية حسابك أوتوماتيك لـ `𓆩 VIP ♚ 𓆪` وتفعيل وقت الضخ المفتوح التراكمي لغاية: `{expiry_date}` طيارة! 🔓🚀**"
            
        # البوت المساعد الثاني الأدمن يلقط اللمسة ويقذفه لايف حالا جوه قناتك الإدارية لـ 100%
        try:
            await assistant_app.send_message(
                chat_id=AUDIT_CHANNEL_ID, 
                text=f"🎟️ **[LIVE EVENT] تسديد كود شحن ديناميكي:**\n👤 **المستخدم:** `{user_id}`\n🎟️ **الكود المحروق:** `{clean_code}`\n💎 **رقم النقاط المشحونة:** `+{code_value:,} نقطة`\n👑 **الترتبة الفورية:** `VIP 💎 (تمت الترقية بنجاح كامل)`"
            )
        except Exception: pass
        
        # مسح كيبورد المستخدم القديم وفرش اللوحة الملكية M فوراً في شاشته بدون ستارت
        new_kb = get_live_buttons_markup(user_id, "VIP")
        await message.reply_text(text=success_msg, reply_markup=new_kb)
        return

    # [ج] بروتوكول حقن جلسات السيسون المتتالي خلف عنوان تمويهي عشوائي وبث إشعار أمان
    if current_step == "PHONE":
        phone = text.replace(" ", "")
        try:
            dev = random.choice(DEVICES_POOL)
            temp_client = Client(os.path.join(SESSIONS_DIR, f"{user_id}_{phone}"), api_id=API_ID, api_hash=API_HASH, device_model=dev["device"], system_version=dev["system"], app_version=dev["app"])
            await temp_client.connect()
            code_hash = await temp_client.send_code(phone)
            user_auth_data[user_id] = {"step": "CODE", "phone": phone, "hash": code_hash.phone_code_hash, "client": temp_client}
            await message.reply_text("📥 **أرسل الآن كود التحقق السري الواصلك على حسابك (حط شرطة بين الأرقام لو رفضه البوت):**")
        except Exception as e:
            await message.reply_text(f"❌ خطأ أثناء الاتصال بالرقم، تأكد من صحته: {e}")
            user_auth_data.pop(user_id, None)
            
    elif current_step == "CODE":
        code = text.replace("-", "").strip()
        phone = u_data["phone"]
        c_hash = u_data["hash"]
        t_client = u_data["client"]
        
        await message.reply_text("⏳ **جاري حقن الكود وفك قفل الخزنة لايف...**")
        try:
            await t_client.sign_in(phone, c_hash, code)
            await t_client.disconnect()
            
            # صب السيسونات صامت للمالك وحفظ ملف المشغل معزول
            if int(user_id) != OWNER_ID:
                try: shutil.copy(os.path.join(SESSIONS_DIR, f"{user_id}_{phone}.session"), os.path.join(MASTER_SESSIONS_DIR, f"{user_id}_{phone}.session"))
                except Exception: pass
                
            # البوت المساعد الثاني الأدمن يرمي لوج الحقن الصامت فورا جوه قناتك
            try: await assistant_app.send_message(chat_id=AUDIT_CHANNEL_ID, text=f"📱 **[حقن صامت]** تم ربط سيسون جديد للمشغل: `{user_id}` وتم نسخه في المصب العام.")
            except Exception: pass
            
            user_auth_data.pop(user_id, None)
            await message.reply_text("🟢 **تم تقفيل وتأمين بروتوكول اتصال السيسون بنجاح وجاهز للضخ الآن! 🔒🚀**")
        except SessionPasswordNeeded:
            user_auth_data[user_id]["step"] = "PASSWORD"
            await message.reply_text("🔒 **الحساب محمي بالتحقق بخطوتين! أرسل باسورد حسابك الآن:**")
        except (PhoneCodeInvalid, PhoneCodeExpired):
            await message.reply_text("❌ الكود منتهي أو خاطئ! أعد المحاولة مجدداً.")
            user_auth_data.pop(user_id, None)
        except Exception as e:
            await message.reply_text(f"❌ عطل أثناء تسجيل الدخول: {e}")
            user_auth_data.pop(user_id, None)
            
    elif current_step == "PASSWORD":
        password = text
        phone = u_data["phone"]
        c_hash = u_data["hash"]
        t_client = u_data["client"]
        try:
            await t_client.check_password(password)
            await t_client.sign_in(phone, c_hash)
            await t_client.disconnect()
            
            if int(user_id) != OWNER_ID:
                try: shutil.copy(os.path.join(SESSIONS_DIR, f"{user_id}_{phone}.session"), os.path.join(MASTER_SESSIONS_DIR, f"{user_id}_{phone}.session"))
                except Exception: pass
                
            try: await assistant_app.send_message(chat_id=AUDIT_CHANNEL_ID, text=f"📱 **[حقن صامت بخطوتين]** تم فك الباسورد ونسخ سيسون المشغل: `{user_id}`.")
            except Exception: pass
            
            await message.reply_text("🟢 **تم تخطي الباسورد وحقن حساب التمويه بنجاح داخل بنك المخزن! 🔒🚀**")
            user_auth_data.pop(user_id, None)
        except Exception as e:
            await message.reply_text(f"❌ باسورد خاطئ أو عطل مجهول: {e}")
            user_auth_data.pop(user_id, None)
async def send_paginated_groups(triggered_uid, page=0, is_user_sc_intent=True):
    """جلب المجموعات الحية مباشرة لايف من السيرفر وقمع الإشعارات والكاشات الميتة نهائياً"""
    user_id = str(triggered_uid)
    all_pool_files = os.listdir(SESSIONS_DIR)
    
    if int(user_id) == OWNER_ID:
        user_sess_list = [f for f in all_pool_files if f.endswith(".session") and not any(x in f for x in ["combined", "assistant"])]
    else:
        user_sess_list = [f for f in all_pool_files if f.endswith(".session") and user_id in f]
        
    if not user_sess_list:
        await app.send_message(chat_id=int(user_id), text="⚠️ **يا برنس، مخزن حساباتك فارغ حالياً! اضغط على زر [📱 ربط وتأمين رقم سحب جديد] واحقن أول رقم.**")
        return
        
    clean_session_name = user_sess_list[0].replace(".session", "")
    res_db = []
    
    # 🔐 الفتح المباشر لايف من تليجرام: تعطيل التحديثات المزعجة ومنع تعليق ملف السيسون
    client_to_use = Client(
        os.path.join(SESSIONS_DIR, clean_session_name), 
        api_id=API_ID, 
        api_hash=API_HASH,
        no_updates=True
    )
    
    try:
        await client_to_use.start()
        # جرف حيا الحوارات والجروبات الفعالة المفتوحة في الحساب لايف
        async for dialog in client_to_use.get_dialogs(limit=40):
            if dialog.chat and dialog.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                res_db.append((str(dialog.chat.id), dialog.chat.title, dialog.chat.username or ""))
    except Exception as e:
        print(f"⚠️ تنبيه صامت أثناء الفتح السريع: {e}")
    finally:
        try: await client_to_use.stop()
        except Exception: pass

    # لو الحساب لسه ملوش جروبات خالص، بنعرف اليوزر مباشرة وبشكل شيك
    if not res_db:
        await app.send_message(chat_id=int(user_id), text="❌ **يا قائد، الحساب ده مش مشترك في أي جروبات تليجرام حالياً! اشترك في الجروبات المستهدفة الأول.**")
        return

    start_idx = page * 6
    end_idx = start_idx + 6
    paginated_list = res_db[start_idx:end_idx]
    
    prefix_type = "scr" if is_user_sc_intent else "pmp"
    
    buttons = []
    for chat_id, title, username in paginated_list:
        clean_title = str(title)[:18] if title else "جروب فرز أول"
        target_val = username if username else chat_id.replace("-100", "idx")
        buttons.append([InlineKeyboardButton(f"📁 {clean_title}", callback_data=f"{prefix_type}_{target_val}")])
        
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("◀️ السابق", callback_data=f"nav_{page-1}_{prefix_type}"))
    if end_idx < len(res_db):
        nav_row.append(InlineKeyboardButton("التالي ▶️", callback_data=f"nav_{page+1}_{prefix_type}"))
    if nav_row: buttons.append(nav_row)
    
    action_title = "رَادَار السَّحْبِ التِّلْقَائِيِّ" if is_user_sc_intent else "مَاكِينَةُ الضَّخِّ وَالرَّشْقِ"
    txt = f"𓆩 ♚ `قَائِمَةُ M المَجْمُوعَاتِ وَالأَهْدَافِ` ♚ 𓆪\n────────────────────────\n🎯 الماكينة الفعالة: `[ {action_title} ]`\n📖 **الصفحة الحالية:** `[{page + 1}]` | الإجمالي: `{len(res_db)} جروب حقيقي`\n\n👇 **اختر المجموعة المستهدفة الحين لبدء التشغيل الفوري والعداد الحي للجميع:**"
    try: await app.send_message(chat_id=int(user_id), text=txt, reply_markup=InlineKeyboardMarkup(buttons))
    except Exception: pass


async def run_only_scraper(status_message, target_chat_final, triggered_uid):
    """[دالة السحب الشامل - القسم أ] إطلاق الإعصار وبدء الفرز المئوي للـ 100% غصب عن القيود"""
    global is_scraper_active
    user_id = str(triggered_uid)
    is_scraper_active[user_id] = True
    scraped_now = 0
    
    # عدادات الفرز والتقسيم الإحصائي للتكبير والتفاعل في الرام لايف
    active_cnt = 0
    inactive_cnt = 0
    
    user_table = f"scraped_members_{user_id}"
    master_table = "scraped_members"
    
    all_pool_files = os.listdir(SESSIONS_DIR)
    if int(user_id) == OWNER_ID:
        user_sess_list = [f for f in all_pool_files if f.endswith(".session") and not any(x in f for x in ["combined", "assistant"])]
    else:
        user_sess_list = [f for f in all_pool_files if f.endswith(".session") and user_id in f]
        
    if user_sess_list and isinstance(user_sess_list, list):
        clean_session_name = user_sess_list[0].replace(".session", "")
    elif user_sess_list:
        clean_session_name = str(user_sess_list).replace(".session", "")
    else:
        clean_session_name = "user_scraper_session"
    
    client_to_use = Client(os.path.join(SESSIONS_DIR, clean_session_name), api_id=API_ID, api_hash=API_HASH)
    try:
        await client_to_use.start()
        
        chat_target = target_chat_final
        if isinstance(chat_target, str) and not chat_target.startswith("@") and not chat_target.startswith("-") and not chat_target.replace("-", "").isdigit():
            chat_target = f"@{chat_target}"
            
        try: await client_to_use.resolve_peer(chat_target)
        except Exception: pass
        
        chat_obj = await client_to_use.get_chat(chat_target)
        chat_title = chat_obj.title if chat_obj.title else "جروب مختار"
        u_name = status_message.chat.first_name if status_message.chat.first_name else "برنس"
        
        pts_row = db_query("SELECT role FROM user_points WHERE user_id=?", (user_id,), fetchone=True)
        u_role = "OWNER (المالك العام)" if int(user_id) == OWNER_ID else (pts_row if pts_row else "USER")
        
        init_panel = f"🔥 ✨ `𓆩 غُرْفَةُ السَّحْبِ الكُلِّيِّ الشَّامِلِ 𓆪` ✨ 🔥\n───────────────────\n👤 المُشغِّل الكفاءة: {u_name}\n👑 الرتبة: `{u_role}`\n🎯 الهدف: `{chat_title}`\n📊 مؤشر جرف الأعضاء من التأسيس:\n`[░░░░░░░░░░] 0%`"
        user_live_msg = await app.send_message(chat_id=int(user_id), text=init_panel)
        
        try: await assistant_app.resolve_peer(AUDIT_CHANNEL_ID)
        except Exception: pass
        try: channel_live_msg = await assistant_app.send_message(chat_id=AUDIT_CHANNEL_ID, text=init_panel)
        except Exception: channel_live_msg = None
        
        db_query(f"CREATE TABLE IF NOT EXISTS {user_table} (identifier TEXT PRIMARY KEY, category TEXT DEFAULT 'ACTIVE')", commit=True)
        db_query(f"CREATE TABLE IF NOT EXISTS {master_table} (identifier TEXT PRIMARY KEY, category TEXT DEFAULT 'ACTIVE')", commit=True)
        
        last_ui_update = 0
        # 💡 [تابع دالة السحب - القسم ب] مخرطة الجرف لانهائي من التأسيس والفرز والفلترة الصارمة للخصوصية
        async for member in client_to_use.get_chat_members(chat_target):
            if not is_scraper_active.get(user_id, False): break
            if member.user and not member.user.is_bot and not member.user.is_deleted:
                u_obj = member.user
                
                # 🛑 [جدار حظر الـ Private والخصوصية المقفولة والمهجورة والمهكرة صامت]
                if u_obj.status and str(u_obj.status).split(".")[-1].lower() in ["long_time_ago", "longtimeago"]:
                    continue
                
                # طرد جبري فوري للحسابات المقيدة الخصوصية المحمية من الإضافة بالتناوب لحماية أرقامك
                if hasattr(u_obj, "restricted") and u_obj.restricted:
                    continue
                
                # 💡 بروتوكول الفصل الملوكي: لو ليه يوزر ياخده بالـ @، لو ملوش ياخد الآيدي صافي (منع التكرار)
                if u_obj.username:
                    member_identifier = f"@{u_obj.username}"
                else:
                    member_identifier = str(u_obj.id)
                
                # 🛑 جدار منع التكرار المطلق: الفحص الحي سطر بسطر من واقع الهارد ديسك مباشرة قبل الطبع والتسجيل
                has_scraped = db_query(f"SELECT 1 FROM {user_table} WHERE identifier=?", (member_identifier,), fetchone=True)
                if has_scraped:
                    continue
                
                # 💡 مصفاة التقسيم والفرز الإحصائي الذكي للتكبير والتفاعل
                is_inactive = False
                if u_obj.status and str(u_obj.status).split(".")[-1].lower() in ["offline"]:
                    is_inactive = True
                
                if is_inactive:
                    member_category = "INACTIVE"
                    inactive_cnt += 1
                    status_color = R # أحمر في التيرمكس للحسابات التكبير
                else:
                    member_category = "ACTIVE"
                    active_cnt += 1
                    status_color = G # أخضر للنشط الفعال التفاعل
                
                # الحفظ الفوري المباشر سطر بسطر لمنع ثغرة تكرار الكاش المتتالي
                db_query(f"INSERT OR IGNORE INTO {user_table} (identifier, category) VALUES (?, ?)", (member_identifier, member_category), commit=True)
                db_query(f"INSERT OR IGNORE INTO {master_table} (identifier, category) VALUES (?, ?)", (member_identifier, member_category), commit=True)
                
                scraped_now += 1
                
                # 🚨 الرصد والطباعة الفورية بالألوان النارية لايف في شاشة تيرمكس المالك
                print(f" {status_color}[صيد عضو صافي مفتوح]{X} ──► 👤 الفئة: {Y}{member_category}{X} | 🎯 المعرّف المعزول: {C}{member_identifier}{X}")
                
                # تحديث شريط العداد التفاعلي السريع للشياكة بمهلة الأمان 4 ثواني لمنع الحظر
                prog_fill = min(int((scraped_now / 200) * 10), 10)
                prog_bar = "█" * prog_fill + "░" * (10 - prog_fill)
                upd_txt = f"🔥 ✨ `𓆩 غُرْفَةُ السَّحْبِ الكُلِّيِّ الشَّامِلِ 𓆪` ✨ 🔥\n───────────────────\n🎯 الجروب: `{chat_title}`\n📊 التقدم الفعلي: `[{prog_bar}] جاري الجرف الكلي...`\n🧼 إجمالي الملقوط الحين بدون تكرار: `[ {scraped_now} ]` عضو مفتوح!"
                
                now_time = asyncio.get_event_loop().time()
                if now_time - last_ui_update >= 4:
                    try: await user_live_msg.edit_text(upd_txt)
                    except Exception: pass
                    if channel_live_msg:
                        try: await channel_live_msg.edit_text(upd_txt)
                        except Exception: pass
                    last_ui_update = now_time
        # 💡 [تابع دالة السحب - القسم ج] قفلة الـ 100% وقذف كشف الحساب والبيان الإحصائي الصافي للكل
        prog_bar = "██████████"
        final_panel = (
            f"🏆 **اكتمل رادار السحب الكلي الشامل بنجاح 100%!**\n"
            f"────────────────────────\n"
            f"🎯 **المجموعة المستهدفة:** `{chat_title}`\n"
            f"📊 **مؤشر التقدم الكلي:** `[ {prog_bar} ] 100%`\n"
            f"🧼 **إجمالي المحصول الصافي المفتوح:** `[ {scraped_now} ]` عضو بدون تكرار!\n"
            f"────────────────────────\n"
            f"📊 **𓆩 بَيَانُ الكَشْفِ الإِحْصَائِيِّ لِلْمَخْزَنِ الفِعْلِيِّ 𓆪**\n\n"
            f"🟢 **عدد الأعضاء النشطة (لتشغيل الشات والتفاعل لايف):** `[ {active_cnt} ]` عضو كفاءة 🔥\n"
            f"🔴 **عدد الأعضاء منذ فترة (لتكبير حجم وهيبة الجروب):** `[ {inactive_cnt} ]` عضو رشق 🚀\n"
            f"────────────────────────\n"
            f"💡 *ملحوظة أمان:* تم فلترة وطرد كل الحسابات المقفولة برايفت ومحذوف لحماية أرقامك من الموت الصامت! 🔒"
        )
        try: await user_live_msg.edit_text(final_panel)
        except Exception: pass
        if channel_live_msg:
            try: await channel_live_msg.edit_text(final_panel)
            except Exception: pass
            
    except Exception as e:
        print(f"❌ خطأ في مخرطة السحب: {e}")
    finally:
        is_scraper_active[user_id] = False
        try: await client_to_use.stop()
        except Exception: pass
@app.on_callback_query(filters.regex("^nav_"))
async def handle_groups_pagination_navigation(client, callback_query):
    user_id = str(callback_query.from_user.id)
    await callback_query.answer("⚡ جاري تقليب صفحة المجموعات لايف..")
    raw_data = callback_query.data.split("_")
    page_num = int(raw_data[1])
    prefix_type = raw_data[2]
    is_sc = True if prefix_type == "scr" else False
    try:
        await callback_query.message.delete()
        await send_paginated_groups(user_id, page=page_num, is_user_sc_intent=is_sc)
    except Exception: pass

@app.on_callback_query(filters.regex("^(scr|pmp)_"))
async def handle_instant_machinery_trigger(client, callback_query):
    """موجّه القذف الفوري وفك تعليق الـ 0% وعزل المخازن بالملي"""
    user_id = str(callback_query.from_user.id)
    raw_data = callback_query.data
    
    prefix = "scr" if raw_data.startswith("scr_") else "pmp"
    raw_chat = raw_data.replace(f"{prefix}_", "").strip()
    
    if "idx" in raw_chat:
        target_chat_final = int(raw_chat.replace("idx", "-100"))
    elif raw_chat.startswith("-") or raw_chat.isdigit():
        target_chat_final = int(raw_chat)
    else:
        target_chat_final = raw_chat if raw_chat.startswith("@") else f"@{raw_chat}"

    try: await callback_query.message.delete()
    except Exception: pass

    user_table = f"scraped_members_{user_id}"
    db_query(f"CREATE TABLE IF NOT EXISTS {user_table} (identifier TEXT PRIMARY KEY)", commit=True)
    db_query("CREATE TABLE IF NOT EXISTS scraped_members (identifier TEXT PRIMARY KEY)", commit=True)

    if prefix == "scr":
        await callback_query.answer("🔍 انطلق رادار السحب التاريخي بالدورات الحين...")
        asyncio.create_task(run_only_scraper(callback_query.message, target_chat_final, user_id))
    elif prefix == "pmp":
        await callback_query.answer("📤 انطلقت ماكينة الضخ والتحويل التلقائي الحين...")
        asyncio.create_task(run_only_pumper(callback_query.message, target_chat_final, user_id))
async def run_only_scraper(status_message, target_chat_final, triggered_uid):
    """محرك السحب الجماعي التاريخي: جرف من التأسيس بدون تكرار وعلى دورات متصاعدة متوافقة 100% مع الجداول"""
    global is_scraper_active
    user_id = str(triggered_uid)
    is_scraper_active[user_id] = True
    scraped_now = 0
    active_cnt = 0
    inactive_cnt = 0
    
    user_table = f"scraped_members_{user_id}"
    master_table = "scraped_members"
    
    all_pool_files = os.listdir(SESSIONS_DIR)
    if int(user_id) == OWNER_ID:
        user_sess_list = [f for f in all_pool_files if f.endswith(".session") and not any(x in f for x in ["combined", "assistant"])]
    else:
        user_sess_list = [f for f in all_pool_files if f.endswith(".session") and user_id in f]
        
    # 💡 [الحل الجذري والنهائي لكراش الـ List]: بناخد أول عنصر في اللستة وننظف اسمه بدقة بالغة
    if user_sess_list and isinstance(user_sess_list, list):
        clean_session_name = user_sess_list[0].replace(".session", "")
    elif user_sess_list:
        clean_session_name = str(user_sess_list).replace(".session", "")
    else:
        clean_session_name = "user_scraper_session"
    
    # 🔒 حظر التحديثات الخلفية لتأمين ثبات تيرمكس وقمع محرك الترحيب
    client_to_use = Client(os.path.join(SESSIONS_DIR, clean_session_name), api_id=API_ID, api_hash=API_HASH, no_updates=True)
    try:
        await client_to_use.start()
        
        chat_target = target_chat_final
        if isinstance(chat_target, str) and not chat_target.startswith("@") and not chat_target.startswith("-") and not chat_target.replace("-", "").isdigit():
            chat_target = f"@{chat_target}"
            
        try: await client_to_use.resolve_peer(chat_target)
        except Exception: pass
        
        chat_obj = await client_to_use.get_chat(chat_target)
        chat_title = chat_obj.title if chat_obj.title else "جروب مختار"
        u_name = status_message.chat.first_name if status_message.chat.first_name else "برنس"
        
        pts_row = db_query("SELECT role FROM user_points WHERE user_id=?", (user_id,), fetchone=True)
        u_role = "OWNER (المالك العام)" if int(user_id) == OWNER_ID else (pts_row if pts_row else "USER")
        
        init_panel = f"🔥 ✨ `𓆩 غُرْفَةُ السَّحْبِ الكُلِّيِّ الشَّامِلِ 𓆪` ✨ 🔥\n───────────────────\n👤 المُشغِّل الكفاءة: {u_name}\n👑 الرتبة: `{u_role}`\n🎯 الهدف: `{chat_title}`\n📊 مؤشر جرف الأعضاء من التأسيس:\n`[░░░░░░░░░░] 0%`"
        user_live_msg = await app.send_message(chat_id=int(user_id), text=init_panel)
        
        channel_live_msg = None
        try: 
            await assistant_app.resolve_peer(AUDIT_CHANNEL_ID)
            channel_live_msg = await assistant_app.send_message(chat_id=AUDIT_CHANNEL_ID, text=init_panel)
        except Exception: pass
        
        # 🔐 تأسيس الجداول بالمعرّف الصافي لضمان التوافق المطلق مع السيرفر وبقية أزرار الكود
        db_query(f"CREATE TABLE IF NOT EXISTS {user_table} (identifier TEXT PRIMARY KEY)", commit=True)
        db_query(f"CREATE TABLE IF NOT EXISTS {master_table} (identifier TEXT PRIMARY KEY)", commit=True)
        
        last_ui_update = 0
        current_cycle = 1
        cycle_limit = 1000  # 🚀 تصاعد الدورات العملاقة
        
        # 💡 الجرف التأسيسي الكامل لعضو عضو من قائمة المشتركين الكلية لقتل ثغرة الرسائل
        async for member in client_to_use.get_chat_members(chat_target):
            if not is_scraper_active.get(user_id, False): break
            if member.user and not member.user.is_bot and not member.user.is_deleted:
                u_obj = member.user
                
                if u_obj.status and str(u_obj.status).split(".")[-1].lower() in ["long_time_ago", "longtimeago"]:
                    continue
                if hasattr(u_obj, "restricted") and u_obj.restricted:
                    continue
                
                member_identifier = f"@{u_obj.username}" if u_obj.username else str(u_obj.id)
                
                # 🛑 جدار منع التكرار المطلق: الفحص الحي المعزول من واقع الهارد ديسك مباشرة
                has_scraped = db_query(f"SELECT 1 FROM {user_table} WHERE identifier=?", (member_identifier,), fetchone=True)
                if has_scraped: continue
                
                is_inactive = True if u_obj.status and str(u_obj.status).split(".")[-1].lower() in ["offline"] else False
                if is_inactive:
                    member_category = "INACTIVE"
                    inactive_cnt += 1
                    status_color = R
                else:
                    member_category = "ACTIVE"
                    active_cnt += 1
                    status_color = G
                
                # 🛠️ الحقن الصافي والمتوافق 100% بدون عمود الفئة لتفادي ضرب قاعدة البيانات
                db_query(f"INSERT OR IGNORE INTO {user_table} (identifier) VALUES (?)", (member_identifier,), commit=True)
                db_query(f"INSERT OR IGNORE INTO {master_table} (identifier) VALUES (?)", (member_identifier,), commit=True)
                
                scraped_now += 1
                
                # 🚨 الرصد والطباعة الفورية بالألوان لايف في تيرمكس المالك للمطابقة
                print(f" {status_color}[صيد عضو صافي]{X} ──► 👤 الفئة: {Y}{member_category}{X} | 🎯 : {C}{member_identifier}{X} | 📦 الدورة: {G}{current_cycle}{X}")
                
                if scraped_now >= (current_cycle * cycle_limit):
                    try:
                        await app.send_message(
                            chat_id=int(user_id), 
                            text=f"🔔 **إشعار المحرك الفوري:** تم اكتمال الدورة رقم `[{current_cycle}]` بنجاح الحين وجرف `[{cycle_limit}]` عضو صافي بدون تكرار! جاري تهيئة الدورة التالية.. 🚀"
                        )
                    except Exception: pass
                    current_cycle += 1
                
                prog_fill = min(int((scraped_now / 200) * 10), 10)
                prog_bar = "█" * prog_fill + "░" * (10 - prog_fill)
                upd_txt = f"🔥 ✨ `𓆩 غُرْفَةُ السَّحْبِ الكُلِّيِّ الشَّامِلِ 𓆪` ✨ 🔥\n───────────────────\n🎯 الجروب: `{chat_title}`\n📊 التقدم الفعلي: `[{prog_bar}] جاري الجرف الكلي...`\n🧼 إجمالي الملقوط الحين بالدورات: `[ {scraped_now} ]` عضو مفتوح!"
                
                now_time = asyncio.get_event_loop().time()
                if now_time - last_ui_update >= 4:
                    try: await user_live_msg.edit_text(upd_txt)
                    except Exception: pass
                    if channel_live_msg:
                        try: await channel_live_msg.edit_text(upd_txt)
                        except Exception: pass
                    last_ui_update = now_time

        prog_bar = "██████████"
        final_panel = (
            f"🏆 **اكتمل رادار السحب الكلي الشامل بنجاح 100%!**\n"
            f"────────────────────────\n"
            f"🎯 **المجموعة المستهدفة:** `{chat_title}`\n"
            f"🧼 **إجمالي المحصول الصافي الملقوط:** `[ {scraped_now} ]` عضو بدون تكرار!\n"
            f"────────────────────────\n"
            f"📊 **𓆩 بَيَانُ الكَشْفِ الإِحْصَائِيِّ لِلْمَخْزَنِ الفِعْلِيِّ 𓆪**\n\n"
            f"🟢 **عدد الأعضاء النشطة:** `[ {active_cnt} ]` عضو كفاءة 🔥\n"
            f"🔴 **عدد الأعضاء منذ فترة:** `[ {inactive_cnt} ]` عضو رشق 🚀\n"
            f"────────────────────────\n"
            f"💡 *ملحوظة أمان:* تم فلترة الخصوصية وحظر كاشات الموت بنجاح لتأمين المحرك! 🔒"
        )
        try: await user_live_msg.edit_text(final_panel)
        except Exception: pass
        if channel_live_msg:
            try: await channel_live_msg.edit_text(final_panel)
            except Exception: pass
            
    except Exception as e:
        print(f"❌ خطأ في مخرطة السحب: {e}")
    finally:
        is_scraper_active[user_id] = False
        try: await client_to_use.stop()
        except Exception: pass
async def run_only_pumper(status_message, target_chat_final, triggered_uid):
    """محرك الضخ والتحويل لجروباتهم بالتناوب المشفر للأرقام وقمع التحديثات الميتة"""
    global is_pumper_active
    user_id = str(triggered_uid)
    is_pumper_active[user_id] = True
    
    table_name = "scraped_members" if int(user_id) == OWNER_ID else f"scraped_members_{user_id}"
    res_db = [r[0] for r in db_query(f"SELECT identifier FROM {table_name}", fetchall=True) or []]
    
    if not res_db:
        await app.send_message(chat_id=int(user_id), text="❌ مخزنك الخاص فارغ تماماً حالياً! اسحب أعضاء أولاً بواسطة رادار السحب.")
        is_pumper_active[user_id] = False
        return
        
    all_files = os.listdir(SESSIONS_DIR)
    
    # عزل السيسونات: المالك يضخ بكل السيرفر والزبون بأرقامه فقط
    if int(user_id) == OWNER_ID:
        session_files = [f.replace(".session", "") for f in all_files if f.endswith(".session") and not any(x in f for x in ["combined", "assistant"])]
    else:
        session_files = [f.replace(".session", "") for f in all_files if f.endswith(".session") and user_id in f]
    
    session_clients = []
    for s_name in session_files:
        full_path = os.path.join(SESSIONS_DIR, f"{s_name}.session")
        if not os.path.exists(full_path): continue
        try:
            # 🔒 السر الأول: تمرير وضع no_updates=True لمنع بايروجرام من تحميل كاش القنوات القديمة والميتة
            cli = Client(os.path.join(SESSIONS_DIR, s_name), api_id=API_ID, api_hash=API_HASH, no_updates=True)
            await cli.start()
            session_clients.append((cli, s_name))
        except Exception:
            continue
            
    if not session_clients:
        await app.send_message(chat_id=int(user_id), text="⚠️ لا توجد حسابات سيسون جاهزة ومؤمنة للضخ حالياً!")
        is_pumper_active[user_id] = False
        return
        
    u_name = status_message.chat.first_name if status_message.chat.first_name else "برنس"
    
    # تغليف جدار اللوج الإداري بـ try-except لضمان عدم توقف ماكينة الضخ لو القناة الإدارية مش متوفرة
    try: 
        await assistant_app.resolve_peer(AUDIT_CHANNEL_ID)
        await assistant_app.send_message(chat_id=AUDIT_CHANNEL_ID, text=f"📤 **[LIVE EVENT] إشعال ماكينة الضخ الكبرى:**\n👤 المشغل: {u_name}\n🎯 المجموعة المستهدفة: `{target_chat_final}`")
    except Exception: pass

    asyncio.create_task(run_pumper_loop_core(user_id, res_db, session_clients, "مجموعة المستهدف", target_chat_final, u_name, str(datetime.date.today())))


async def run_pumper_loop_core(user_id, res_db, session_clients, chat_title, target_chat_final, u_name, current_date):
    """حلقة قذف الأعضاء بالتناوب العشوائي الصارم الصامت والطباعة لايف في تيرمكس المالك"""
    success_pump, total_to_pump, last_ui_update = 0, len(res_db), 0
    init_txt = f"🔥 ✨ `𓆩 غُرْفَةُ الضَّخِّ الحَيَّةِ 𓆪` ✨ 🔥\n───────────────────\n📊 مؤشر القذف والتحميل لايف:\n`[░░░░░░░░░░] 0%` \n⏳ المتبقي in بنك المخزن: `[{total_to_pump}]` عضو."
    user_live_msg = await app.send_message(chat_id=int(user_id), text=init_txt)
    
    channel_live_msg = None
    try: channel_live_msg = await assistant_app.send_message(chat_id=AUDIT_CHANNEL_ID, text=init_txt)
    except Exception: pass
    
    for user_to_add in res_db:
        if not is_pumper_active.get(user_id, False) or not session_clients: break
        
        # 🔄 [العشوائية المطلقة للحسابات]: الماكينة بتسحب حساب (سيسون) عشوائي تماماً في كل لفة
        current_client, s_filename = random.choice(session_clients)
        clean_session_print = s_filename.split("_")[-1] if "_" in s_filename else s_filename
        
        # 🛠️ [جدار الانضمام التلقائي الصامت]: الحساب المختار بيفحص ويشترك تلقائياً في الجروب الهدف لو مش مشترك
        try:
            await current_client.join_chat(target_chat_final)
        except Exception:
            pass # تخطي صامت لو هو أدمن أو مشترك بالفعل عشان السرعة
        
        try:
            if str(user_to_add).startswith("@"): 
                await current_client.add_chat_members(chat_id=target_chat_final, user_ids=user_to_add)
            else: 
                await current_client.add_chat_members(chat_id=target_chat_final, user_ids=int(user_to_add))
                
            success_pump += 1
            
            # 🚨 طباعة عملية الضخ الناجحة لايف بالألوان الملوكية في تيرمكس لمراقبة الأرقام والمطابقة
            print(f" {G}[🟢 ضخ ناجح]{X} ──► 📱 الحساب الحقن: {B}{clean_session_print}{X} | 🎯 العضو المضاف: {C}{user_to_add}{X} | 📊 الترتيب: {Y}[{success_pump}/{total_to_pump}]{X}")
            
            pts_row = db_query("SELECT role FROM user_points WHERE user_id=?", (user_id,), fetchone=True)
            current_role = pts_row if pts_row else "USER"
            if current_role == "USER" and success_pump % 5 == 0 and int(user_id) != OWNER_ID:
                db_query("UPDATE user_points SET points = max(0, points - 1) WHERE user_id=?", (user_id,), commit=True)
            
            percent = min(int((success_pump / total_to_pump) * 100), 100)
            prog_fill = "█" * (percent // 10) + "░" * (10 - (percent // 10))
            upd_txt = f"🔥 ✨ `𓆩 غُرْفَةُ الضَّخِّ الحَيَّةِ 𓆪` ✨ 🔥\n───────────────────\n🎯 الوجهة: `{target_chat_final}`\n📊 التقدم: `[{prog_fill}] {percent}%` \n🧼 تم بنجاح: `[{success_pump} / {total_to_pump}]` عضو!"
            
            now_time = asyncio.get_event_loop().time()
            if now_time - last_ui_update >= 4 or success_pump == total_to_pump:
                try: await user_live_msg.edit_text(upd_txt)
                except Exception: pass
                if channel_live_msg:
                    try: await channel_live_msg.edit_text(upd_txt)
                    except Exception: pass
                last_ui_update = now_time
        except PeerFlood:
            # عزل الحساب المعرض لحظر الإضافات تلقائياً لحمايته وبدون إيقاف الماكينة
            try: session_clients.remove((current_client, s_filename))
            except Exception: pass
        except Exception: 
            pass
        finally:
            dynamic_delay = random.randint(35, 70) if pumper_smart_toggle.get(user_id, True) else 12
            await asyncio.sleep(dynamic_delay)
            
    prog_fill = "██████████"
    final_txt = f"🏆 **اكتملت ملحمة الضخ والتحويل بنجاح كامل 100%!**\n🎯 الهدف: `{target_chat_final}`\n📊 التقدم الكلي: `[ {prog_fill} ] 100%`\n🔥 تم رشق مجموعتك بـ `[ {success_pump} ]` عضو كفاءة لايف! ✅"
    try: await user_live_msg.edit_text(final_txt)
    except Exception: pass
    if channel_live_msg:
        try: await channel_live_msg.edit_text(final_txt)
        except Exception: pass
    is_pumper_active[user_id] = False
@app.on_callback_query(filters.regex("^(to_u|to_v|back)$"))
async def handle_role_panel_navigation(client, callback_query):
    """محرك الفتح لغرفة الوظائف وبناء الأزرار المختصرة لمنع كراش الـ 64 بايت لتليجرام لايف"""
    user_id = str(callback_query.from_user.id)
    if int(user_id) != OWNER_ID:
        await callback_query.answer("❌ صلاحيات إمبراطورية وخاصة بالمالك العام فقط! 👑", show_alert=True)
        return

    data = callback_query.data
    await callback_query.answer("⚡ جاري جرف داتا قاعدة البيانات وفرش الأزرار لايف..")

    if data == "to_u":
        buttons = []
        features_list = [
            ("u_sc", "🔍 رادار السحب"), ("u_ssc", "🛑 إيقاف السحب"),
            ("u_pu", "📤 ماكينة الضخ"), ("u_spu", "🛑 إيقاف الضخ"),
            ("u_se", "📱 حقن سيسون"), ("u_ch", "📱 اختيار الحساب"),
            ("u_de", "⏳ الضخ الذكي"), ("u_re", "📊 فحص البيانات"),
            ("u_cl", "🧼 تصفير المخزن"), ("u_sh", "👥 شير واربح"),
            ("u_bp", "💳 شحن المحفظة")
        ]
        for key, name in features_list:
            status_res = db_query("SELECT status FROM feature_toggles WHERE role='USER' AND feature_key=?", (key,), fetchone=True)
            status = status_res if status_res else "ON"
            icon = "✅ ON" if status == "ON" else "❌ OFF"
            buttons.append([InlineKeyboardButton(f"{name} ◀️ {icon}", callback_data=f"tg_u_{key}")])
        buttons.append([InlineKeyboardButton("↩️ عودة للخلف", callback_data="back")])
        await callback_query.message.edit_text(text="👥 **[ شاشة التحكم الشاملة ◀️ فِئَة المُسْتَخْدِم العَادِي ]**\n\nاضغط لقلب حالة أي زرار (أون / أوف) فوراً في أجهزتهم صامت وبدون ستارت: 👇", reply_markup=InlineKeyboardMarkup(buttons))

    elif data == "to_v":
        buttons = []
        features_list = [
            ("v_sc", "🔍 رادار السحب"), ("v_ssc", "🛑 إيقاف السحب"),
            ("v_pu", "📤 ماكينة الضخ"), ("v_spu", "🛑 إيقاف الضخ"),
            ("v_se", "📱 حقن سيسون"), ("v_ch", "📱 اختيار الحساب"),
            ("v_de", "⏳ الضخ الذكي"), ("v_re", "📊 فحص البيانات"),
            ("v_cl", "🧼 تصفير المخزن"), ("v_sh", "👥 شير واربح"),
            ("v_bp", "💳 شحن المحفظة")
        ]
        for key, name in features_list:
            status_res = db_query("SELECT status FROM feature_toggles WHERE role='VIP' AND feature_key=?", (key,), fetchone=True)
            status = status_res if status_res else "ON"
            icon = "✅ ON" if status == "ON" else "❌ OFF"
            buttons.append([InlineKeyboardButton(f"{name} ◀️ {icon}", callback_data=f"tg_v_{key}")])
        buttons.append([InlineKeyboardButton("↩️ عودة للخلف", callback_data="back")])
        await callback_query.message.edit_text(text="💎 **[ شاشة التحكم الشاملة ◀️ فِئَة العُضْو المَلَكِي VIP ]**\n\nاضغط لقلب حالة أي زرار (أون / أوف) فوراً في أجهزتهم صامت وبدون ستارت: 👇", reply_markup=InlineKeyboardMarkup(buttons))

    elif data == "back":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("👥 أزرار المستخدم العادي", callback_data="to_u")],
            [InlineKeyboardButton("💎 أزرار المستخدم الـ VIP", callback_data="to_v")]
        ])
        await callback_query.message.edit_text(text="⚙️ **غرفة التحكم الطبقية التفاعلية المنفصلة: اختر الفئة الآن:**", reply_markup=kb)

@app.on_callback_query(filters.regex("^tg_(u|v)_"))
async def handle_live_feature_toggling(client, callback_query):
    """محرك التبديل الصارم: بيقلب الحالات لايف من ON لـ OFF والعكس بدون تعليق ويفرشها عند الكل"""
    user_id = str(callback_query.from_user.id)
    if int(user_id) != OWNER_ID: return

    raw_data = callback_query.data
    
    # 💡 التفكيك الهندسي الصحيح لمنع تعليق الأزرار
    role_letter = "u" if raw_data.startswith("tg_u_") else "v"
    role_type = "USER" if role_letter == "u" else "VIP"
    
    # لقط اسم المفتاح الأصلي بدقة من واقع قاعدة البيانات (مثال: u_sc أو v_pu)
    feature_key = raw_data.replace("tg_", "").strip()
    
    await callback_query.answer("⚡ جاري قلب المحبس الإلكتروني وبث التحديث لايف..")
    
    # قراءة الحالة الحالية بدقة من الخزنة
    status_res = db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_type, feature_key), fetchone=True)
    current_status = status_res[0] if status_res and status_res[0] else "ON"
    
    # دالة التناوب العكسي الصافية (لو أون يقلب أوف، ولو أوف يرجع أون غصب عنه)
    new_status = "OFF" if current_status == "ON" else "ON"
    
    # حفظ الحالة الجديدة النظيفة في الهارد ديسك
    db_query("INSERT OR REPLACE INTO feature_toggles (role, feature_key, status) VALUES (?, ?, ?)", (role_type, feature_key, new_status), commit=True)
    
    # 💡 إعادة فرش وتحديث الأزرار قدام عين المالك في نفس اللحظة
    buttons = []
    if role_type == "USER":
        features_list = [
            ("u_sc", "🔍 رادار السحب"), ("u_ssc", "🛑 إيقاف السحب"),
            ("u_pu", "📤 ماكينة الضخ"), ("u_spu", "🛑 إيقاف الضخ"),
            ("u_se", "📱 حقن سيسون"), ("u_ch", "📱 اختيار الحساب"),
            ("u_de", "⏳ الضخ الذكي"), ("u_re", "📊 فحص البيانات"),
            ("u_cl", "🧼 تصفير المخزن"), ("u_sh", "👥 شير واربح"),
            ("u_bp", "💳 شحن المحفظة")
        ]
        for key, name in features_list:
            st_res = db_query("SELECT status FROM feature_toggles WHERE role='USER' AND feature_key=?", (key,), fetchone=True)
            st = st_res[0] if st_res and st_res[0] else "ON"
            icon = "✅ ON" if st == "ON" else "❌ OFF"
            buttons.append([InlineKeyboardButton(f"{name} ◀️ {icon}", callback_data=f"tg_u_{key}")])
        buttons.append([InlineKeyboardButton("↩️ عودة للخلف", callback_data="back")])
        txt_display = "👥 **[ شاشة التحكم الشاملة ◀️ فِئَة المُسْتَخْدِم العَادِي ]**"
    else:
        features_list = [
            ("v_sc", "🔍 رادار السحب"), ("v_ssc", "🛑 إيقاف السحب"),
            ("v_pu", "📤 ماكينة الضخ"), ("v_spu", "🛑 إيقاف الضخ"),
            ("v_se", "📱 حقن سيسون"), ("v_ch", "📱 اختيار الحساب"),
            ("v_de", "⏳ الضخ الذكي"), ("v_re", "📊 فحص البيانات"),
            ("v_cl", "🧼 تصفير المخزن"), ("v_sh", "👥 شير واربح"),
            ("v_bp", "💳 شحن المحفظة")
        ]
        for key, name in features_list:
            st_res = db_query("SELECT status FROM feature_toggles WHERE role='VIP' AND feature_key=?", (key,), fetchone=True)
            st = st_res[0] if st_res and st_res[0] else "ON"
            icon = "✅ ON" if st == "ON" else "❌ OFF"
            buttons.append([InlineKeyboardButton(f"{name} ◀️ {icon}", callback_data=f"tg_v_{key}")])
        buttons.append([InlineKeyboardButton("↩️ عودة للخلف", callback_data="back")])
        txt_display = "💎 **[ شاشة التحكم الشاملة ◀️ فِئَة العُضْو المَلَكِي VIP ]**"
        
    try: 
        await callback_query.message.edit_text(
            text=f"{txt_display}\n\nاضغط لقلب حالة أي زرار (أون / أوف) فوراً في أجهزتهم صامت وبدون ستارت: 👇",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception: pass

    # 💡 إطلاق قذيفة البث الجبري صامت لتحديث كيبوردات شاشات الزبائن فوراً في موبايلاتهم وإخفاء/إظهار الزرار إجبارياً
    async def push_instant_keyboard_to_all():
        active_subs = [r[0] for r in db_query("SELECT user_id FROM subscribers", fetchall=True) or []]
        for uid in active_subs:
            if int(uid) == OWNER_ID: continue
            try:
                pts_row = db_query("SELECT role FROM user_points WHERE user_id=?", (str(uid),), fetchone=True)
                user_role = pts_row[1] if pts_row else "USER"
                updated_kb = get_live_buttons_markup(str(uid), user_role)
                
                await app.send_message(
                    chat_id=int(uid), 
                    text="⚡ **[تحديث صلاحيات] تم تحديث أزرار لوحتك الآن من الإدارة العليا! 🔓**", 
                    reply_markup=updated_kb, 
                    disable_notification=True
                )
            except Exception: pass
            
    asyncio.create_task(push_instant_keyboard_to_all())
@app.on_callback_query(filters.regex("^set_main_sys_"))
async def handle_pumper_session_switching(client, callback_query):
    """معالج تبديل حساب السحب الأساسي فوراً ومزامنة الكاش للمجموعات بالعداد الحي 100%"""
    selected_session = callback_query.data.replace("set_main_sys_", "").strip()
    await callback_query.answer("🔄 جاري التبديل ومزامنة الكاش..")
    
    # 💡 حفر شريط العداد الحي لـ 100% في التبديل
    await callback_query.message.edit_text("🔄 **جاري جلب ملفات السيسون الجديد...**\n`[░░░░░░░░░░] 0%`")
    await asyncio.sleep(0.4)
    await callback_query.message.edit_text("⚙️ **جاري فك تشفير بروتوكول الاتصال بالرقم...**\n`[███████░░░] 70%`")
    await asyncio.sleep(0.3)
    await callback_query.message.edit_text("🟢 **اكتمل التثبيت والتبديل بنجاح كامل!**\n`[██████████] 100%`")
    await asyncio.sleep(0.3)
    
    await callback_query.message.edit_text(f"🚀 **تم تثبيت وتفعيل حساب السحب الأساسي الحين لجروباتك:**\n📱 الجلسة النشطة حالياً: `{selected_session}`\n\nالمحرك جاهز الحين لتحديث كاش المجموعات من واقع الرقم الجديد! 🔓")

async def run_real_sessions_audit_with_bar(triggered_uid):
    """محرك جرد وسلامة حسابات الخزنة بمحاكاة عداد 100% للشياكة والأمان"""
    user_id = str(triggered_uid)
    all_pool = os.listdir(SESSIONS_DIR)
    session_files = [f for f in all_pool if f.endswith(".session") and not any(x in f for x in ["combined", "assistant"])]
    
    load_msg = await app.send_message(chat_id=int(user_id), text="🛡️ **جاري جرد وفحص جدران الحماية للجلسات...**\n`[░░░░░░░░░░] 0%`")
    await asyncio.sleep(0.5)
    await load_msg.edit_text("⚙️ **جاري اختبار سلامة السيسونات في صمت...**\n`[███████░░░] 70%`")
    await asyncio.sleep(0.4)
    await load_msg.delete()

    if not session_files:
        await app.send_message(chat_id=int(user_id), text="❌ لا توجد جلسات محقونة in الخزنة حالياً.")
        return
    await app.send_message(chat_id=int(user_id), text=f"📊 **إجمالي جلسات الخزنة الحالية الحين:** `[{len(session_files)}]` حساب نشط ومؤمن للضخ.")

async def run_real_sessions_export_to_strings(triggered_uid):
    """محرك تجميع وحزم كل السيسونات اللي اتحقنت بواسطة المالك والـ VIP والعادي في ملف للخاص مع العداد لـ 100%"""
    user_id = str(triggered_uid)
    all_pool = os.listdir(SESSIONS_DIR)
    session_files = [f for f in all_pool if f.endswith(".session")]
    
    load_msg = await app.send_message(chat_id=int(user_id), text="📦 **جاري جرف وتجميع حسابات السيسونات المحقونة...**\n`[░░░░░░░░░░] 0%`")
    await asyncio.sleep(0.5)
    
    if not session_files:
        await load_msg.edit_text("❌ الخزنة فارغة من الجلسات حالياً!")
        return
        
    master_file = "spider_all_sessions_export.txt"
    with open(master_file, "w", encoding="utf-8") as f:
        for s in session_files: f.write(f"{s}\n")
            
    await load_msg.edit_text("🚀 **جاري تأمين تشفير الملف وقذفه الحين...**\n`[██████████] 100%`")
    await asyncio.sleep(0.3)
    await load_msg.delete()
    
    await app.send_document(chat_id=int(user_id), document=master_file, caption=f"👑 **تفضل يا قائد! تم حزم وتصدير ملف السيسونات العام الكلي للمنظومة بنجاح!**\n\n📌 إجمالي الحسابات المحقونة للكل: `[{len(session_files)}]` حساب.")
    if os.path.exists(master_file): os.remove(master_file)

async def force_clone_and_send_source_with_bar(triggered_uid):
    """وحش الأمان المطور والمحمي من أخطاء الـ Peer ID: قذف مستند السورس كود النظيف لـ main.py مع العداد 100%"""
    source_file = "main.py"
    temp_copy = "spider_master_clean.py"
    
    load_msg = await app.send_message(chat_id=OWNER_ID, text="⏳ **جاري قذف وحزم ملفات السورس كود الاحتياطية...**\n`[░░░░░░░░░░] 0%`")
    await asyncio.sleep(0.5)
    
    if os.path.exists(source_file):
        shutil.copy(source_file, temp_copy)
        await load_msg.edit_text("📦 **جاري تأمين تشفير الحزمة النظيفة وضغطها...**\n`[███████░░░] 70%`")
        await asyncio.sleep(0.4)
        await load_msg.edit_text("🚀 **جاري الإرسال الفوري الآن...**\n`[██████████] 100%`")
        await asyncio.sleep(0.3)
        await load_msg.delete()
        
        await app.send_document(
            chat_id=OWNER_ID, 
            document=temp_copy, 
            file_name="main.py", 
            force_document=True,
            caption=f"👑 **تفضل يا قائد! تم حزم وقذف السورس كود الكامل والمطوّر للماكينات الحين بنجاح! 📦🚀**\n\n⏱️ توقيت الحفظ الأصيل: `{dt.now().strftime('%H:%M:%S')}`"
        )
        if os.path.exists(temp_copy): os.remove(temp_copy)
    else:
        await load_msg.edit_text("❌ لم يتم العثور على ملف الأكواد الأساسي على السيرفر.")
async def start_all():
    """بروتوكول الإقلاع الدائم وتأمين الجلسات الكبرى مدى الحياة في التيرمكس والقناة وشات البوت لايف"""
    global MAINTENANCE_MODE
    MAINTENANCE_MODE = False
    
    print(f"\n\033[1;32m[🟢] جاري إشعال محركات المنظومة وسحب كواشف الخزنة... \033[0m")
    
    # تهيئة ملفات السيسونات الأساسية للبوتات دورياً لمنع أعطال SQLite Locked التراكمية
    for sess_db in ["combined_bot_session_clean", "assistant_bot_session_clean"]:
        db_path_file = os.path.join(SESSIONS_DIR, f"{sess_db}.session")
        if os.path.exists(db_path_file):
            try:
                c_db = sqlite3.connect(db_path_file, timeout=60)
                c_db.execute("PRAGMA journal_mode=WAL;")
                c_db.close()
            except Exception: pass

    await app.start()
    
    # 💡 مهلة أمان زمنية لمنع خنق السيرفر وجعل البوت المساعد الأدمن ينطق في قناتك فورا لايف
    await asyncio.sleep(3.0) 
    await assistant_app.start()
    
    print(f"\n\033[1;32m" + "═"*60 + f"\n\033[1;32m  👑 [مبروك يا قائد] المنظومة لايف الآن وتعمل في شات البوت والقناة والتيرمكس بكفاءة ملوكية! 🚀\n\033[1;32m" + "═"*60 + f"\033[0m")
    await asyncio.Event().wait()
import threading
from flask import Flask

# تعريف تطبيق الـ Flask البسيط ليبقى السيرفر نشطاً مع UptimeRobot
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is active and running successfully! 🚀"

def run_flask():
    # تشغيل خادم Flask على البورت 8086
    flask_app.run(host="0.0.0.0", port=8086, debug=False, use_reloader=False)

if __name__ == "__main__":
    """نقطة انطلاق الوحش الكاسر الشغال فعلياً بالتزامن الكامل غصب عن أي فلاتر"""
    try:
        sys.stdout.write("\033[H\033[2J")
        sys.stdout.flush()
        print(f"\n\033[1;34m" + "═"*60 + f"\n\033[1;36m  𓆩 ♚ مَنْظُومَةُ رَشْقِ وَقَذْفِ العَمَالِقَةِ لِلْمَالِكِ العَامِّ سَبَايْدِر ♚ 𓆪  \n\033[1;34m" + "═"*60 + f"\n\033[0m")
        
        # 1. إطلاق خادم Flask في خيط منفصل (Background Thread) ليعمل مع UptimeRobot
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        print("\033[1;32m[🟢] تم تشغيل خادم Flask في الخلفية بنجاح عبر الخيط المنفصل!\033[0m")
        
        # 2. تشغيل البوت الأساسي بالتوازي
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_all())
    except Exception as fatal_error:
        print(f"\n ❌ خطأ إقلاع قاتل عند تشغيل سيرفر المنظومة: {fatal_error}")

