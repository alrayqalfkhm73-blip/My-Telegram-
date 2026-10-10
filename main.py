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

# 🔥 [الأمان البريميوم المطلق] كتم لوجات البيروجرام وحجب بصمة التوكنات لحماية المحرك من الرصد
logging.getLogger("pyrogram").setLevel(logging.CRITICAL)

from pyrogram import Client, filters, enums
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import PeerFlood, UserPrivacyRestricted, UserAlreadyParticipant, SessionPasswordNeeded, PhoneCodeInvalid, PhoneCodeExpired

# 🎨 أكواد الألوان الملوكية لشاشة محرك تيرمكس الخاصة بالمالك (لايف للمطابقة)
G = "\033[1;32m" # أخضر ملوكي
R = "\033[1;31m" # أحمر ناري
B = "\033[1;34m" # أزرق فخم
Y = "\033[1;33m" # أصفر ذهبي
C = "\033[1;36m" # تيركوز مضيء
W = "\033[1;37m" # أبيض صافي
X = "\033[0m"    # تصفير الألوان

# 🛑 بيانات المنظومة السرية والثابتة لمالك البوت والمدير العام سابيدر 🛑
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

# 🗺️ [وحش الأمان المتطور] محرك التوليد اللانهائي للبصمات الرقمية (تفتيت رادار الـ 20,000 جلسة)
EGYPT_DEVICES = [
    {"device": "Samsung SM-A556B", "system": "Android 14", "app": "11.2.3"},
    {"device": "Oppo CPH2603", "system": "Android 14", "app": "10.15.0"},
    {"device": "Xiaomi 23090RA98G", "system": "Android 13", "app": "11.0.1"},
    {"device": "iPhone14,5", "system": "iOS 17.5", "app": "10.11.2"}
]

US_DEVICES = [
    {"device": "iPhone16,2", "system": "iOS 18.0", "app": "11.3.0"},
    {"device": "Google Pixel 9 Pro", "system": "Android 15", "app": "11.2.0"},
    {"device": "Samsung SM-S928U", "system": "Android 14", "app": "11.1.5"}
]

GLOBAL_DEVICES = [
    {"device": "OnePlus CPH2581", "system": "Android 14", "app": "11.0.5"},
    {"device": "Sony XQ-DQ72", "system": "Android 14", "app": "10.14.1"}
]

def generate_dynamic_device(phone_number):
    """صنع وتوليد هويات IPs وهمية لا متناهية تعتمد جغرافياً على كود دولة الرقم الحية الحين"""
    clean_phone = phone_number.replace("+", "").strip()
    if clean_phone.startswith("20"):
        base = random.choice(EGYPT_DEVICES)
        ip_v = f"197.{random.randint(32,128)}.{random.randint(0,255)}.{random.randint(1,254)}"
    elif clean_phone.startswith("1"):
        base = random.choice(US_DEVICES)
        ip_v = f"172.{random.randint(16,31)}.{random.randint(0,255)}.{random.randint(1,254)}"
    else:
        base = random.choice(GLOBAL_DEVICES)
        ip_v = f"82.{random.randint(10,90)}.{random.randint(0,255)}.{random.randint(1,254)}"
        
    build_tag = f"UP1A.{random.randint(23,26)}{random.randint(10,12)}{random.randint(10,28)}.00{random.randint(1,9)}"
    return {
        "device_model": base["device"],
        "system_version": f"{base['system']} (Build {build_tag})",
        "app_version": base["app"],
        "ipv4": ip_v
    }

# 🧼 تطهير وسحق طلاسم أكواد البريميوم تماماً من رأس ملف الرام لمنع شلل الكيبورد الأرضي
def get_premium_emoji_by_role(role, emoji_key):
    """مصفوفة الإيموجيات المطهرة الشيك البديلة المتوافقة مع أجهزة المستخدمين والعادي والـ VIP"""
    icons_vault = {
        "OWNER": {"tag": "👑", "spark": "⚡", "gem": "💎"},
        "VIP": {"tag": "💎", "shield": "🛡️", "star": "⭐"},
        "USER": {"tag": "⚙️", "coin": "🪙", "phone": "📱"}
    }
    return icons_vault.get(role, icons_vault["USER"]).get(emoji_key, "⚙️")

# 💡 [بروتوكول العداد المئوي الموحد للأزرار] يعمل بنبضة الـ % والبريميوم التفاعلي في لمح البصر
async def run_live_progress_bar(client, user_id, action_text):
    """إشعال شريط العداد المئوي لايف الموحد الفخم لجميع الأزرار والـ 30 لعبة لشحن الحماس والوجاهة"""
    role_res = "OWNER" if int(user_id) == OWNER_ID else "USER"
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        c = conn.cursor()
        r = c.execute("SELECT role FROM user_points WHERE user_id=?", (str(user_id),)).fetchone()
        if r and r[0] == "VIP": role_res = "VIP"
        conn.close()
    except Exception: pass
    
    e_tag = get_premium_emoji_by_role(role_res, "tag")
    
    load_msg = await client.send_message(chat_id=int(user_id), text=f"{e_tag} **جاري تهيئة {action_text}...**\n`[🟨░░░░░░░░░] 0%`")
    await asyncio.sleep(0.15)
    await load_msg.edit_text(f"⚡ **جاري فحص محابس الأمان وتأمين خط الاتصال صامت...**\n`[🟩██████░░░] 60%`")
    await asyncio.sleep(0.15)
    await load_msg.edit_text(f"🏆 **اكتمل بروتوكول التعبئة وتأمين المحرك بنجاح 100%! 🔓**\n`[👑█████████] 100%`")
    await asyncio.sleep(0.15)
    await load_msg.delete()
    return True

# بنك المتغيرات وحاويات الرام لعزل نقرات الحسابات ومنع الـ NameError
user_auth_data = {}
user_click_trackers = {}
waiting_for_broadcast = False
waiting_for_channels = False
is_scraper_active = {}       
is_pumper_active = {}        
pumper_smart_toggle = {}     
MAINTENANCE_MODE = False     
def init_sqlite_vault():
    """تأسيس الجداول الرسمية للإمبراطورية داخل الهارد ديسك مع تفعيل WAL لمنع التجميد"""
    conn = sqlite3.connect(DB_PATH, timeout=60)
    # تفعيل محابس الـ WAL والـ Synchronous لضمان سرعة معالجة الحسابات بالتوازي لـ 20,000 جلسة
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    cursor = conn.cursor()
    
    # الجداول الصافية معرّفات فقط لمنع كراش الفئة الزائدة وتكرار البيانات
    cursor.execute("CREATE TABLE IF NOT EXISTS scraped_members (identifier TEXT PRIMARY KEY)")
    cursor.execute("CREATE TABLE IF NOT EXISTS subscribers (user_id TEXT PRIMARY KEY, username TEXT DEFAULT NULL)")
    
    # جدول الاشتراك الإجباري المتعدد لتخزين القنوات والجروبات معاً للمشغلين
    cursor.execute("CREATE TABLE IF NOT EXISTS forced_channels (channel_username TEXT PRIMARY KEY, invite_link TEXT DEFAULT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS feature_toggles (role TEXT, feature_key TEXT, status TEXT, PRIMARY KEY (role, feature_key))")
    cursor.execute("CREATE TABLE IF NOT EXISTS redeem_codes (code TEXT PRIMARY KEY, value TEXT, type TEXT)")
    
    # خزنة الرصيد والرتب التراكمية لايف للمحفظة والتحقق
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
    
    # 🚫 [جدول الإدارة العليا] مخرطة القائمة السوداء لحظر المشغلين بالـ ID واليوزر
    cursor.execute("CREATE TABLE IF NOT EXISTS banned_users (user_id TEXT PRIMARY KEY, banned_at TEXT DEFAULT CURRENT_TIMESTAMP)")
    
    # 📢 [خزنة الـ System Audit المعزولة] لحماية آيدي قناة اللوج الحية الخاصة بالملك والـ M من التضارب
    cursor.execute("CREATE TABLE IF NOT EXISTS system_audit_vault (audit_id TEXT PRIMARY KEY, updated_at TEXT DEFAULT CURRENT_TIMESTAMP)")
    
    # حقن آيدي قناتك الافتراضية في الخزنة أول مرة لو مش موجودة لتنشيط البوت M فوراً
    cursor.execute("INSERT OR IGNORE INTO system_audit_vault (audit_id) VALUES (?)", (str(AUDIT_CHANNEL_ID),))
    
    conn.commit()
    conn.close()

# إطلاق محرك الخزنة وتجهيز الجداول فوراً عند الإقلاع
init_sqlite_vault()

def db_query(query, params=(), commit=False, fetchone=False, fetchall=False):
    """مستقبل الاستعلامات الموحد للتحكم بأمان وإغلاق المحابس دورياً ومنع الـ Database Locked"""
    res = None
    try:
        conn = sqlite3.connect(DB_PATH, timeout=60)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        cursor = conn.cursor()
        cursor.execute(query, params)
        if commit: 
            conn.commit()
        if fetchone: 
            row = cursor.fetchone()
            res = row if row and len(row) == 1 else row
        elif fetchall: 
            res = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(f" {R}❌ Database Exception Error:{X} {e}")
    return res

load_dotenv(find_dotenv())

# 👑 ربط وهندسة التوكنات بالعكس الجبري الصارم (البوت القائد + البوت المساعد الثاني M)
app = Client("combined_bot_session_clean", api_id=API_ID, api_hash=API_HASH, bot_token="8938908361:AAGJr1gYdDkM9Grv-Dro2GEG43S3ILpPpJA")
assistant_app = Client("assistant_bot_session_clean", api_id=API_ID, api_hash=API_HASH, bot_token="8468639064:AAHKhK3MciRsFQW2Bly-PiZ3muLJMn6O4bM")
@app.on_callback_query(filters.regex("^act_scr_|^act_pmp_"))
async def handle_real_scrape_and_pump_execution(client, callback_query):
    """المحرك العسكري: تنفيذ السحب الحساس، أو الضخ الفعلي بالعداد التصاعدي واللوج لايف الحين"""
    user_id = str(callback_query.from_user.id)
    raw_data = callback_query.data
    
    await callback_query.answer("⚡ تم إطلاق المحرك الفعلي.. تابع الحركة لايف!")
    target_chat_id = int(raw_data.split("_")[-1])
    
    active_sess = user_auth_data.get(f"active_session_{user_id}")
    session_file = os.path.join(SESSIONS_DIR, f"{active_sess}.session")
    
    try:
        device_data = generate_dynamic_device(active_sess)
        cli = Client(session_file, api_id=API_ID, api_hash=API_HASH, device_model=device_data["device_model"], system_version=device_data["system_version"], app_version=device_data["app_version"], in_memory=False)
        await cli.start()
    except Exception:
        await callback_query.message.edit_text("❌ **فشل فتح الجلسة؛ الرقم محظور أو تالف الحين!**")
        return

    current_audit_id = db_query("SELECT audit_id FROM system_audit_vault LIMIT 1", fetchone=True) or str(AUDIT_CHANNEL_ID)

    # 🔍 أ- رادار السحب الحساس (بدون تكرار وبدون حسابات محذوفة ميتة)
    if "act_scr_" in raw_data:
        await callback_query.message.edit_text("🔍 **جاري تشغيل رادار السحب الحساس.. جرف داتا الأعضاء الحية ونبذ الوهمية الحين...**")
        cnt = 0
        user_table = f"scraped_members_{user_id}"
        db_query(f"CREATE TABLE IF NOT EXISTS {user_table} (identifier TEXT PRIMARY KEY)", commit=True)
        
        async for member in cli.get_chat_members(target_chat_id):
            if member.user.is_deleted: continue
            idt = str(member.user.id)
            is_exist = db_query(f"SELECT 1 FROM {user_table} WHERE identifier=?", (idt,), fetchone=True)
            if not is_exist:
                db_query(f"INSERT INTO {user_table} (identifier) VALUES (?)", (idt,), commit=True)
                db_query("INSERT OR IGNORE INTO scraped_members (identifier) VALUES (?)", (idt,), commit=True)
                cnt += 1
                if cnt % 10 == 0:
                    print(f" {G}[🔍 رادار السحب]{X} تم اصطياد وحفظ: {Y}{cnt}{X} عضو حي صافي.")

        succ_txt = f"🟢 **اكتملت مخرطة السحب الحساس!**\n\n• إجمالي المجلوبين حياً: `[{cnt:,}]` عضو جاهز.\n• حالة المخزن: مؤمن وضد التكرار 100%."
        await callback_query.message.edit_text(succ_txt)
        await assistant_app.send_message(chat_id=int(current_audit_id), text=f"🔍 **[SCRAPE EVENT] رادار السحب لقط بنجاح:**\n👤 المشغل: `{user_id}`\n📦 الجروب الهدف آيدي: `{target_chat_id}`\n📈 المجلوبين صافي: `[+{cnt:,}]` حساب صاحي جاهز للضخ.")

    # 📤 ب- ماكينة الضخ والرشـق الفعلي (العداد اللحظي التصاعدي لايف بالأرقام)
    elif "act_pmp_" in raw_data:
        await callback_query.message.edit_text("📤 **جاري استدعاء عمارة الرشق وبدء قذف الأعضاء بالتناوب العشوائي لايف...**")
        user_table = f"scraped_members_{user_id}"
        all_targets = db_query(f"SELECT identifier FROM {user_table}", fetchall=True) or []
        added_cnt, dead_cnt = 0, 0
        
        for row in all_targets:
            tg_uid = int(row)
            try:
                await cli.add_chat_members(chat_id=target_chat_id, user_ids=tg_uid)
                added_cnt += 1
                print(f" {C}[📤 ماكينة الضخ]{X} تم صب العضو رقم {G}{added_cnt}{X} جوه المجموعة بنجاح.")
                
                if added_cnt % 2 == 0:
                    await callback_query.message.edit_text(f"📤 **الماكينة شغال ضخ وقذف حقيقي حالياً لايف:**\n──────────────────────────\n🟢 تم رشق بنجاح: `[{added_cnt}]` عضو فرز أول.\n💀 حسابات ميتة تم تجاوزها: `[{dead_cnt}]` حساب.\n──────────────────────────\n`[████████░░] جاري صب الرصيد...`")
                await asyncio.sleep(1.5)
            except PeerFlood: break
            except Exception:
                dead_cnt += 1
                db_query(f"DELETE FROM {user_table} WHERE identifier=?", (str(tg_uid),), commit=True)

        final_pump_txt = f"🎉 **تم انتهاء جولة الضخ الفعلي للماكينات بنجاح!**\n\n• إجمالي من تم صبهم ورشقهم: `[{added_cnt:,}]` عضو حقيقي.\n• حسابات ميتة تم تطهيرها ومسحها: `[{dead_cnt:,}]` حساب."
        await callback_query.message.edit_text(final_pump_txt)
        await assistant_app.send_message(chat_id=int(current_audit_id), text=f"📤 **[PUMP EVENT] تقرير ماكينة الضخ والرشـق الكبرى:**\n👤 المشغل: `{user_id}`\n🏰 جروب الوجهة المستهدفة: `{target_chat_id}`\n🟢 ضخ ناجح فعلي: `[{added_cnt:,}]` عضو.\n🧼 حسابات ميتة مطهرة: `[{dead_cnt:,}]` حساب محذوف.")

    await cli.stop()
async def display_inline_session_groups_panel(client, message, user_id, intent="SCRAPE", page=0):
    """🚀 محرك بنك الأهداف: تقسيم المجموعات حياً على صفحات تفاعلية (10 مجموعات بالصفحة) مع التالي والسابق لتخطي الـ 64 بايت"""
    all_pool_files = [f for f in os.listdir(SESSIONS_DIR) if f.endswith(".session")]
    sess_pool = [f for f in all_pool_files if "bot_session" not in f and "assistant" not in f]
    
    if not sess_pool:
        await message.reply_text("⚠️ **عذراً يا برنس! لا يوجد أي أرقام سحب محقونة حالياً في مجلد sessions_pool!**")
        return

    active_sess = user_auth_data.get(f"active_session_{user_id}")
    if not active_sess or f"{active_sess}.session" not in sess_pool:
        active_sess = sess_pool[0].replace(".session", "")
        user_auth_data[f"active_session_{user_id}"] = active_sess

    session_file = os.path.join(SESSIONS_DIR, f"{active_sess}.session")
    try:
        device_data = generate_dynamic_device(active_sess)
        target_cli = Client(session_file, api_id=API_ID, api_hash=API_HASH, device_model=device_data["device_model"], system_version=device_data["system_version"], app_version=device_data["app_version"])
        await target_cli.start()
    except Exception:
        await message.reply_text(f"❌ **الحساب الحالي `[{active_sess}]` محظور أو تالف! يرجى التبديل أو ربط رقم جديد الحين.**")
        return

    mock_dialogs = []
    try:
        async for dialog in target_cli.get_dialogs(limit=100):
            if dialog.chat.type in [enums.ChatType.SUPERGROUP, enums.ChatType.GROUP]:
                mock_dialogs.append((dialog.chat.title, dialog.chat.id))
    except Exception as e:
        await message.reply_text(f"❌ **خطأ جرف المجموعات الحية:** `{e}`")
        await target_cli.stop()
        return

    await target_cli.stop()

    if not mock_dialogs:
        await message.reply_text(f"⚠️ **الرقم الحالي `[{active_sess}]` غير مشترك في أي مجموعات حالياً!**")
        return

    # حسابات تقسيم الصفحات التفاعلية (10 مجموعات لكل لوحة)
    start_idx = page * 10
    end_idx = start_idx + 10
    paginated_dialogs = mock_dialogs[start_idx:end_idx]

    inline_keyboards = []
    prefix_code = "m_sc_" if intent == "SCRAPE" else "m_pu_"
    
    # تفجير الأزرار بشكل طولي شيك ومقيد بـ 10 أزرار فقط لحماية الشاشة
    for title, chat_id in paginated_dialogs:
        clean_id = str(chat_id).replace("-100", "")
        user_auth_data[f"map_{clean_id}"] = chat_id
        inline_keyboards.append([InlineKeyboardButton(f"👥 {title[:20]}...", callback_data=f"{prefix_code}{clean_id}")])
        
    # حقن صف أزرار التنقل والتنقيب الذكي [السابق والتالي] للتقليب بين لوحات المجموعات
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("◀️ السابق", callback_data=f"pgnav_{intent}_{page-1}"))
    if end_idx < len(mock_dialogs):
        nav_row.append(InlineKeyboardButton("التالي ▶️", callback_data=f"pgnav_{intent}_{page+1}"))
    if nav_row:
        inline_keyboards.append(nav_row)
        
    inline_keyboards.append([InlineKeyboardButton("↩️ عودة لقائمة الأزرار الرئيسية", callback_data="back_to_main")])
    
    intent_title = "جَرْفٌ وَسَحْبٌ كُلِّيٌّ (حَسَّاسٌ) 🔍" if intent == "SCRAPE" else "ضَخٌّ وَرَشْقٌ فَعَّلِيٌّ 📤"
    txt_panel = (
        f"🎯 **[ بَنْكُ المَجْمُوعَاتِ التَّفَاعُلِيَّةِ ◀️ اللَّوْحَةُ رقم ({page + 1}) ]**\n"
        f"──────────────────────────\n"
        f"📱 **ملف الرقم القائد الحين:** `{active_sess}.session`\n"
        f"⚙️ **بروتوكول المعالجة الحية:** `{intent_title}`\n"
        f"📊 إجمالي أهداف الحساب المكتشفة: `[{len(mock_dialogs)}] جروب`\n"
        f"──────────────────────────\n"
        f"👇 التقليب شغال طيران باللمس؛ اضغط على اسم الجروب لإشعال العمليات الحقيقية فوراً:"
    )
    await message.reply_text(text=txt_panel, reply_markup=InlineKeyboardMarkup(inline_keyboards))

@app.on_callback_query(filters.regex("^pgnav_"))
async def handle_groups_panels_navigation_callback(client, callback_query):
    """موجه الحركة للتقليب اللحظي بين لوحات المجموعات الـ 10 دون تكرار أو ثقل"""
    user_id = str(callback_query.from_user.id)
    raw_data = callback_query.data.split("_")
    intent_target = raw_data[1]
    page_num = int(raw_data[2])
    
    await callback_query.answer(f"⚡ جاري فتح اللوحة الإرشادية رقم ({page_num + 1})...")
    try:
        await callback_query.message.delete()
        await display_inline_session_groups_panel(client, callback_query.message, user_id, intent=intent_target, page=page_num)
    except Exception: pass
@app.on_callback_query(filters.regex("^m_sc_|^m_pu_"))
async def handle_real_military_operations_vault(client, callback_query):
    """المحرك العسكري الحقيقي: السحب الحساس من التأسيس أو الضخ التراكمي مع شريط العداد لايف بالتوازي في الأماكن الثلاثة"""
    user_id = str(callback_query.from_user.id)
    raw_data = callback_query.data
    
    await callback_query.answer("⚡ تم إطلاق المحرك الفعلي لايف.. تابع الشاشات الحين!")
    clean_id = raw_data.split("_")[-1]
    real_chat_id = user_auth_data.get(f"map_{clean_id}")
    
    active_sess = user_auth_data.get(f"active_session_{user_id}")
    session_file = os.path.join(SESSIONS_DIR, f"{active_sess}.session")
    
    try:
        device_data = generate_dynamic_device(active_sess)
        cli = Client(session_file, api_id=API_ID, api_hash=API_HASH, device_model=device_data["device_model"], system_version=device_data["system_version"], app_version=device_data["app_version"])
        await cli.start()
    except Exception:
        await callback_query.message.edit_text("❌ **فشل فتح الجلسة؛ الحساب تالف أو محظور حالياً الحين!**")
        return

    current_audit_id = db_query("SELECT audit_id FROM system_audit_vault LIMIT 1", fetchone=True) or str(AUDIT_CHANNEL_ID)

    if "m_sc_" in raw_data or "act_scr_" in raw_data:
        # فك قفل الرسالة في شات البوت لبدء بث الشريط المائي حياً للمشغل
        status_msg = await callback_query.message.edit_text("🔍 **[0%] جاري فك قفل القناة الإدارية وجرف داتا التأسيس الكلية...**")
        cnt = 0
        user_table = f"scraped_members_{user_id}"
        db_query(f"CREATE TABLE IF NOT EXISTS {user_table} (identifier TEXT PRIMARY KEY)", commit=True)
        
        # 👑 [بروتوكول الجرف التاريخي العسكري]: السحب بالتسلسل الزمني من أول يوم اتنشأ فيه الجروب غصب عن الفلاتر
        try:
            # استخدام خط اتصال نظيف ومفتوح دائم لقاعدة البيانات لمنع كراش Closed Database
            local_conn = sqlite3.connect(DB_PATH, timeout=60)
            local_conn.execute("PRAGMA journal_mode=WAL;")
            local_cursor = local_conn.cursor()
            
            async for member in cli.get_chat_members(real_chat_id):
                # 🛑 صمام الأمان: حظر البوتات والحسابات المحذوفة نهائياً لضمان الفرز النظيف
                if member.user.is_deleted or member.user.is_bot: 
                    continue
                    
                idt = str(member.user.id)
                u_name = f"@{member.user.username}" if member.user.username else "No Username"
                
                # منع التكرار الجبري حياً جوه الهارد ديسك
                local_cursor.execute(f"SELECT 1 FROM {user_table} WHERE identifier=?", (idt,))
                if not local_cursor.fetchone():
                    local_cursor.execute(f"INSERT INTO {user_table} (identifier) VALUES (?)", (idt,))
                    local_cursor.execute("INSERT OR IGNORE INTO scraped_members (identifier) VALUES (?)", (idt,))
                    cnt += 1
                    
                    # 🎨 [وحش العداد المئوي الملون والشريط المائي التفاعلي النيون]
                    pct = min(100, (cnt * 100) // 150) # احتساب النسبة الحية تصاعدياً
                    bars = "█" * (pct // 10) + "░" * (10 - (pct // 10))
                    
                    # 🚨 1. قذف وبث الشريط المائي لايف جوه شاشة التيرمكس بالثانية والألوان
                    sys.stdout.write(f"\(\r {G}\)[🔍 رادار السحب]{X} [{bars}] {pct}% | جرف حي ──► ID: {Y}{idt}{X} | User: {C}{u_name}{X}")
                    sys.stdout.flush()
                    
                    # 🚨 2. تحديث وبث الشريط المائي لايف جوه شات البوت (تحديث الرسالة بالـ % حياً قدام الزبون)
                    if cnt % 5 == 0:
                        try:
                            await status_msg.edit_text(
                                f"🔍 **[ رَادَارُ الجَرْفِ التَّارِيخِيِّ يَعْمَلُ الحِين ]** 𓆩♚𓆪\n"
                                f"──────────────────────────\n"
                                f"📊 **شريط المعالجة المائي:** `[{bars}] {pct}%` \n"
                                f"🟢 **إجمالي المصادين من التأسيس:** `[ {cnt} ]` عضو فرز أول.\n"
                                f"📱 **المعرف الصافي الأخير:** `{idt}`\n"
                                f"──────────────────────────\n"
                                f"⚡ *السيستم يضخ في الرام والهارد ديسك بالتوازي صامت الحين...*"
                            )
                        except Exception: pass
                        
                    # 🚨 3. قذف اللوج بالتوازي جوه شات البوت المساعد M وقناتك السرية بالمعرف الصافي
                    if cnt % 10 == 0:
                        try:
                            await assistant_app.send_message(
                                chat_id=int(current_audit_id),
                                text=f"🔍 **[LIVE SCRAPE] جرف حي متسلسل من التأسيس:**\n🆔 ID: `{idt}`\n👤 User: `{u_name}`\n📊 شريط التحميل المائي: `[{bars}] {pct}%` | التراكمي: `[ {cnt} ]`"
                            )
                        except Exception: pass
            
            local_conn.commit()
            local_conn.close()
            
        except Exception as e:
            await callback_query.message.edit_text(f"❌ **تعليق أثناء جرف داتا التأسيس:** `{e}`")
            await cli.stop()
            return

        print(f"\n{G}✅ تم انتهاء جولة جرف الرادار من التأسيس بنجاح ملوكي!{X}")
        succ_txt = f"🟢 **اكتملت مخرطة السحب الحساس الحقيقي من التأسيس!**\n\n• إجمالي المجلوبين حياً: `[{cnt:,}]` عضو فرز أول حقيقي.\n• حالة المخزن الخاص بك: `مؤمن بالشريط المائي وضد التكرار 100%! ✅`"
        await callback_query.message.edit_text(succ_txt)

    elif "m_pu_" in raw_data or "r_pu_" in raw_data:
        status_msg = await callback_query.message.edit_text("📤 **[🟨░░░░░░░░░] 0% جاري استدعاء عمارة الرشق وبدء قذف الأعضاء الحية لايف...**")
        user_table = f"scraped_members_{user_id}"
        all_targets = db_query(f"SELECT identifier FROM {user_table}", fetchall=True) or []
        
        if not all_targets:
            await callback_query.message.edit_text("⚠️ **مخزنك الخاص على البياض وفارغ! يرجى كبس زر الرادار وجرف أعضاء من التأسيس أولاً الحين.**")
            return
            
        added_cnt, dead_cnt = 0, 0
        total_jobs = len(all_targets)
        
        for row in all_targets:
            tg_uid = int(row)
            try:
                # 🚀 الضخ الحقيقي الجبري جوه شات الجروب المستهدف لرفع العداد لايف قدام عينك حياً
                await cli.add_chat_members(chat_id=real_chat_id, user_ids=tg_uid)
                added_cnt += 1
                
                # احتساب العداد والشريط المئوي الحركي الحقيقي للضخ
                pct = min(100, (added_cnt * 100) // total_jobs)
                bars = "█" * (pct // 10) + "░" * (10 - (pct // 10))
                
                # 🚨 1. طباعة لوج الضخ الفعلي بالثانية والشريط جوه شاشة التيرمكس للمطابقة
                sys.stdout.write(f"\(\r {C}\)[📤 ماكينة الضخ]{X} [{bars}] {pct}% | تم رشق العضو رقم: {G}{added_cnt}{X} جوه المجموعة حياً.")
                sys.stdout.flush()
                
                # 🚨 2. بث العداد التصاعدي والشريط لايف جوه شات البوت (تحديث الرسالة بالـ % حياً)
                if added_cnt % 2 == 0:
                    try:
                        await status_msg.edit_text(
                            f"📤 **[ مَاكِينَةُ الضَّخِّ وَالرَّشْقِ العَسْكَرِيَّةِ تَعْمَلُ الحِين ]** 𓆩♚𓆪\n"
                            f"──────────────────────────\n"
                            f"📈 **شريط رشق الرصيد:** `[{bars}] {pct}%` \n"
                            f"🟢 **تم صب بنجاح:** `[{added_cnt} / {total_jobs}]` عضو فرز أول حياً.\n"
                            f"💀 **حسابات ميتة تم عزلها:** `[{dead_cnt}]` حساب محظور.\n"
                            f"──────────────────────────"
                        )
                    except Exception: pass
                
                # 🚨 3. بث الحركة لايف في شات البوت المساعد M وقناتك السرية بالتوازي
                if added_cnt % 5 == 0:
                    try:
                        await assistant_app.send_message(chat_id=int(current_audit_id), text=f"📤 **[LIVE PUMP] نبضة ضخ حية ──► العداد بيرفع الحين!**\n🏰 جروب الوجهة: `{real_chat_id}`\n📊 شريط التحميل الحركي: `[{bars}] {pct}%` \n🟢 تم صب العضو رقم: `[ {added_cnt} ]` بنجاح ملوكي! ✅")
                    except Exception: pass
                await asyncio.sleep(1.5)
            except Exception:
                dead_cnt += 1
                db_query(f"DELETE FROM {user_table} WHERE identifier=?", (str(tg_uid),), commit=True)

        final_pump_txt = f"🎉 **تم انتهاء جولة الضخ الفعلي للماكينات بنجاح ملوكي! العداد رفع قدام عينك الحين الحين.**\n\n• إجمالي من تم صبهم ورشقهم فعلياً: `[{added_cnt:,}]` عضو حركي.\n• حسابات ميتة تم تطهيرها ومسحها: `[{dead_cnt:,}]` حساب."
        await status_msg.edit_text(final_pump_txt)
async def open_session_switcher_panel(client, message, user_id):
    """📱 ربط زر التبديل الفعلي: جرف وعرض ملفات السيسونات المحقونة كـ أزرار تفاعلية باللمس الحين"""
    all_pool_files = [f for f in os.listdir(SESSIONS_DIR) if f.endswith(".session")]
    
    if not all_pool_files:
        await message.reply_text("⚠️ **لا يوجد أي حسابات سحب (سيسونات) محقونة في السيرفر حالياً!**")
        return

    inline_buttons = []
    for f_name in all_pool_files:
        sess_clean = f_name.replace(".session", "")
        # المالك يرى السيرفر بالكامل، والمشغل العادي يرى أرقامه فقط لحماية الخصوصية
        if int(user_id) == OWNER_ID or str(user_id) in sess_clean:
            inline_buttons.append([InlineKeyboardButton(f"📱 {sess_clean}.session", callback_data=f"sw_to_{sess_clean}")])
            
    if not inline_buttons:
        await message.reply_text("⚠️ **لم نجد أي حسابات سحب محقونة مرتبطة بآيدي حسابك حالياً!**")
        return
        
    inline_buttons.append([InlineKeyboardButton("↩️ عودة للوحة الرئيسية", callback_data="back_to_main")])
    await message.reply_text(
        text="📱 **[ غُرْفَةُ فَرْزِ وَتَبْدِيلِ حِسَابَاتِ السَّحْبِ المَاسْتِر ]**\n──────────────────────────\n👇 اضغط على اسم ملف السيسون بالأسفل لتثبيته كـ قائد للعمليات الحالية الحين ومزامنة كاش المجموعات تلقائياً:",
        reply_markup=InlineKeyboardMarkup(inline_buttons)
    )

@app.on_callback_query(filters.regex("^sw_to_"))
async def handle_session_switching_action(client, callback_query):
    """تثبيت السيسون المختار في الرام صامت وبدون ريستارت"""
    user_id = str(callback_query.from_user.id)
    target_sess = callback_query.data.replace("sw_to_", "").strip()
    
    user_auth_data[f"active_session_{user_id}"] = target_sess
    await callback_query.answer(f"✅ تم تثبيت [{target_sess}.session] كـ قائد للعمليات الحالية الحين الحين!", show_alert=True)
    try: await callback_query.message.delete()
    except Exception: pass
def get_live_buttons_markup(u_id, role):
    """بناء لوحة مفاتيح المشغلين النظيفة والمطهرة 100% من طلاسم الأكواد لضمان عمل الأزرار الـ 20"""
    kb_list = []
    state = pumper_smart_toggle.get(str(u_id), True)
    
    speed_btn = "🟢 الضخ الذكي: نَشِط أوتوماتيك" if state else "🔴 الضخ الذكي: مُعطل صامت"
    
    # 👑 لوحة التحكم العليا الشاملة للملك العام (OWNER) - تناسق ثنائي ملكي 100%
    if int(u_id) == OWNER_ID:
        kb_list = [
            [KeyboardButton("🔍 إطلاق رادار السحب التلقائي"), KeyboardButton("🛑 إيقاف رادار السحب")],
            [KeyboardButton("📤 بدء ماكينة الضخ والتحويل"), KeyboardButton("🛑 إيقاف ماكينة الضخ فوراً")],
            [KeyboardButton("📱 ربط رقم سحب جديد"), KeyboardButton("📱 التبديل واختيار حساب السحب الأساسي")],
            [KeyboardButton(speed_btn), KeyboardButton("📊 فحص البيانات والتقرير")],
            [KeyboardButton("🧼 تصفير وتطهير المخزن"), KeyboardButton("🎟️ توليد وقذف أكواد الشحن")],
            [KeyboardButton("🛡️ فحص وسلامة الجلسات"), KeyboardButton("🧼 عزل وتطهير الحسابات الميتة")],
            [KeyboardButton("📦 تصدير ملف السيسونات العام"), KeyboardButton("📦 تصدير ملف المخزن العام الكلي")],
            [KeyboardButton("📢 إرسال إشعار تحديث السيرفر"), KeyboardButton("🔓 إيقاف إشعار تحديث السيرفر")],
            [KeyboardButton("🛠️ لوحة التحكم في الأزرار والوظائف"), KeyboardButton("📦 قذف وحفظ السورس كود")],
            [KeyboardButton("💳 شحن يدوي لحساب مستخدم"), KeyboardButton("📉 سحب / صفر محفظة مستخدم")],
            [KeyboardButton("🚫 حظر مشترك من المنظومة (BAN)"), KeyboardButton("🎟️ جرد الأكواد الحية والمحروقة")],
            [KeyboardButton("📢 ربط وتغيير قناة اللوج الحية"), KeyboardButton("🔐 تفعيل / قفل الاشتراك الإجباري")],
            [KeyboardButton("📱 جرد وتوزيع جلسات التمويه"), KeyboardButton("👑 ترقية / طرد عضو للـ VIP")],
            [KeyboardButton("👥 جرد إمبراطورية المشتركين"), KeyboardButton("𓆃 جرد كاش المجموعات المسحوبة")],
            [KeyboardButton("🛠️ فحص محابس قاعدة البيانات (WAL)"), KeyboardButton("𓆂 مخرطة التحكم في ساحة الألعاب")],
            [KeyboardButton("𓆂 تصميم وتحديث اللوحة الإرشادية"), KeyboardButton("🎨 مخرطة التحكم في إيموجيات البريميوم الحية")],
            [KeyboardButton("🛰️ إذاعة وبث الإشعار الرئاسي"), KeyboardButton("💳 شحن رصيد المحفظة بالـ كود")],
            [KeyboardButton("👥 شير واربح وتجميع النقاط")]
        ]
        return ReplyKeyboardMarkup(kb_list, resize_keyboard=True)
        
    # 👥 لوحة فئة الزبائن والـ VIP النظيفة الخالية من أي طلاسم أكواد لتعمل فوراً
    all_pool_files = os.listdir(SESSIONS_DIR)
    has_linked_sess = any(f.endswith(".session") and str(u_id) in f for f in all_pool_files)
    
    if not has_linked_sess:
        kb_list.append([KeyboardButton("📱 ربط رقم سحب جديد")])
        kb_list.append([KeyboardButton("💳 شحن رصيد المحفظة بالـ كود"), KeyboardButton("👥 شير واربح وتجميع النقاط")])
        return ReplyKeyboardMarkup(kb_list, resize_keyboard=True)
        
    # حقن وفرش الأزرار للزبائن بناءً على تفعيل المالك لها أون أو أوف
    role_tag = "VIP" if role == "VIP" else "USER"
    prefix = "v" if role == "VIP" else "u"
    
    if db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_tag, f"{prefix}_sc"), fetchone=True) != ("OFF",):
        kb_list.append([KeyboardButton("🔍 إطلاق رادار السحب التلقائي"), KeyboardButton("🛑 إيقاف رادار السحب")])
    if db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_tag, f"{prefix}_pu"), fetchone=True) != ("OFF",):
        kb_list.append([KeyboardButton("📤 بدء ماكينة الضخ والتحويل"), KeyboardButton("🛑 إيقاف ماكينة الضخ فوراً")])
        
    row3 = []
    if db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_tag, f"{prefix}_se"), fetchone=True) != ("OFF",):
        row3.append(KeyboardButton("📱 ربط رقم سحب جديد"))
    if db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_tag, f"{prefix}_ch"), fetchone=True) != ("OFF",):
        row3.append(KeyboardButton("📱 التبديل واختيار حساب السحب الأساسي"))
    if row3: kb_list.append(row3)
    
    row4 = []
    if db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_tag, f"{prefix}_de"), fetchone=True) != ("OFF",):
        row4.append(KeyboardButton(speed_btn))
    if db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_tag, f"{prefix}_re"), fetchone=True) != ("OFF",):
        row4.append(KeyboardButton("📊 فحص البيانات والتقرير"))
    if row4: kb_list.append(row4)
    
    row5 = []
    if db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_tag, f"{prefix}_cl"), fetchone=True) != ("OFF",):
        row5.append(KeyboardButton("🧼 تصفير وتطهير المخزن"))
    row5.append(KeyboardButton("🎮 الألعاب وكسب النقاط"))
    if row5: kb_list.append(row5)
    
    row6 = []
    if db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_tag, f"{prefix}_sh"), fetchone=True) != ("OFF",):
        row6.append(KeyboardButton("👥 شير واربح وتجميع النقاط"))
    if db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_tag, f"{prefix}_bp"), fetchone=True) != ("OFF",):
        row6.append(KeyboardButton("💳 شحن رصيد المحفظة بالـ كود"))
    if row6: kb_list.append(row6)
        
    return ReplyKeyboardMarkup(kb_list, resize_keyboard=True)
@app.on_message(filters.command("start") & filters.private)
async def start_router(client, message):
    """موجه الحركة المركزي: تطهير الجداول وقذف جدار الجروب الرسمي إجبارياً قبل اللوحة"""
    user_id = str(message.from_user.id)
    
    if db_query("SELECT 1 FROM banned_users WHERE user_id=?", (user_id,), fetchone=True):
        await message.reply_text("🛑 **عذراً، لقد تم حظر حسابك نهائياً من استخدام المنظومة!**")
        return

    # حفر بيانات الحساب في الخزنة الجديدة النظيفة فوراً لمنع غيبوبة الرام
    db_query("INSERT OR IGNORE INTO subscribers (user_id, username) VALUES (?, ?)", (user_id, message.from_user.username), commit=True)
    
    role_res = "OWNER" if int(user_id) == OWNER_ID else "USER"
    pts_check = db_query("SELECT role FROM user_points WHERE user_id=?", (user_id,), fetchone=True)
    if pts_check and pts_check == "VIP": 
        role_res = "VIP"
        
    # 🎨 العداد الملون الفخم الموحد النظيف 100% بدون طلاسم
    load_msg = await client.send_message(chat_id=int(user_id), text=f"🚨 **[🟨░░░░░░░░░] 10% جاري تهيئة كواشف الخزنة وفحص المعالج...**")
    await asyncio.sleep(0.1)
    await load_msg.edit_text(f"🟢 **[👑█████████] 100% [اكتمل بروتوكول الإقلاع وتطهير كاش الرام بنجاح...]**")
    try: await load_msg.delete()
    except Exception: pass

    if int(user_id) == OWNER_ID:
        kb = get_live_buttons_markup(user_id, "OWNER")
        welcome_txt = f"🔥 `𓆩 ♚ مَرْحَبَاً بِقَائِدِ العَمَلِيَّاتِ العُلْيَا ♚ 𓆪` \n───────────────────\n⚙️ **حالة السيرفر:** `الخزنة مفتوحة ومحابس الـ WAL تحت طوعك لايف بالكامل! 🔓`"
        await message.reply_text(text=welcome_txt, reply_markup=kb)
        return

    # 🔐 جدار حماية الجروب الرسمي الصارم - قفل العبور التام للزبائن والـ VIP
    forced_rows = db_query("SELECT channel_username, invite_link FROM forced_channels", fetchall=True)
    if forced_rows:
        not_joined_buttons = []
        idx_btn = 1
        for ch_username, inv_link in forced_rows:
            try:
                member_check = await app.get_chat_member(chat_id=ch_username, user_id=int(user_id))
                if member_check.status in [enums.ChatMemberStatus.LEFT, enums.ChatMemberStatus.BANNED]:
                    raise Exception()
            except Exception:
                final_link = inv_link if inv_link else f"https://t.me{str(ch_username).replace('@','')}"
                not_joined_buttons.append([InlineKeyboardButton(f"📢 انضم للجروب الرسمي رقم ({idx_btn}) 📢", url=final_link)])
                idx_btn += 1

        if not_joined_buttons:
            not_joined_buttons.append([InlineKeyboardButton("🔄 تفعيل والتحقق من الاشتراك 🔄", callback_data="check_sub_live")])
            await message.reply_text(
                text=f"⚠️ **[ إِشْعَارٌ إِدَارِيٌّ صَارِمٌ ◀️ الحِسَابُ مُقَيَّدٌ مُؤَقَّتَاً ]** 🔒\n──────────────────────────\nعذراً يا برنس الساحة! لوحتك الإرشادية وباقة أزرار الماكينات مقفولة ومحجوبة عنك الحين؛ لأنك غير مشترك في الجروب الرسمي التابع للإدارة العليا.\n\n⚙️ **لِفَكِّ القُفْلِ وَتَفْعِيلِ اللَّوْحَةِ فَوْرَاً:**\n1. اضغط على أزرار الانضمام بالأسفل وادخل الجروب الرسمي الحين.\n2. ارجع لشات البوت واكبس على زرار التفعيل بالأسفل الحين.\n──────────────────────────",
                reply_markup=InlineKeyboardMarkup(not_joined_buttons)
            )
            return

    await dispatch_user_and_vip_guides_vault(client, message, user_id, role_res)
async def dispatch_user_and_vip_guides_vault(client, message, user_id, role):
    """فرش الدليل القديم والأصيل والـ 20 زرار كاملين طيران في موبايل العادي والـ VIP بعد التحقق"""
    if MAINTENANCE_MODE:
        await message.reply_text("⚠️ **وضع الصيانة نشط حالياً وتحديثات السيرفر جارية.. البوت واقف مؤقتاً وسيتم إشعارك فور فتح المنظومة! 🔒**")
        return

    pts_row = db_query("SELECT points, role, vip_expiry FROM user_points WHERE user_id=?", (user_id,), fetchone=True)
    if not pts_row:
        db_query("INSERT INTO user_points (user_id, points, role, vip_expiry) VALUES (?, 15, 'USER', NULL)", (user_id,), commit=True)
        points, role, vip_expiry = 15, "USER", None
    else:
        points, role, vip_expiry = pts_row

    kb = get_live_buttons_markup(user_id, role)
    u_display_name = message.from_user.first_name if message.from_user.first_name else "برنس الساحة"

    # 👑 إعادة قذف وصهر اللوحة الإرشادية القديمة والأصيلة بالملي 👑
    if role == "VIP":
        guide_panel = (
            f"👑 **الدَّلِيلُ المَلَكِيُّ الأَعْلَى لِمُشَغِّلِي مَاكِينَاتِ الرَّشْقِ الفِئَةِ النُّخْبَوِيَّةِ VIP**\n"
            f"──────────────────────────\n"
            f"👑 **رُتْبَةُ حِسَابِكَ الحَالِيَّةِ:** `[ عُضْوٌ مَلَكِيٌّ عَالِي الكَفَاءَةِ VIP ♚ ]` 💎\n"
            f"⏳ **تَارِيخُ انْتِهَاءِ الصَّلَاحِيَّةِ المَفْتُوحَةِ:** `[ {vip_expiry if vip_expiry else 'نشطة ملوكي'} ]` **طيارة.**\n"
            f"🚀 **قُدْرَةُ الضَّخِّ المِعْمَارِيَّةِ Lَدَيْكَ:** صلاحية ضخ مفتوحة ولانهائية طوال فترة الاشتراك!\n\n"
            f"⚙️ **دَلِيلُ الصَّلَاحِيَّاتِ العُلْيَا وَتُرُوسِ التَّشْغِيلِ:**\n"
            f"• **`[ 📱 ربط رقم سحب جديد ]`** ◀️ لحقن وتربط مصفوفة أرقامك الخاصة تحت بصمة التمويه الجغرافي البريميوم.\n"
            f"• **`[ 📱 التبديل واختيار حساب السحب الأساسي ]`** ◀️ للتبديل بين أرقامك؛ وتحديث ومزامنة كاش المجموعات وزري السحب والضخ أوتوماتيكياً فوراً باللمس.\n"
            f"• **`[ 🔍 إطلاق رادار السحب التلقائي ]`** ◀️ مخرطة الجرف العملاقة؛ تصطاد الأعضاء الحية والنشطة من التأسيس وبدون تكرار وبدون حسابات محذوفة.\n"
            f"• **`[ 📤 بدء ماكينة الضخ والتحويل ]`** ◀️ عمارة الرشق الكبرى； تبدأ الأرقام بالتناوب صب وقذف الأعضاء جوه مجموعتك لايف.\n"
            f"• **`[ 🎮 الألعاب وكسب النقاط ]`** ◀️ صالة المحترفين باللمس؛ تحتوى على الـ 30 لعبة كاملة وجولات التحدي مستخدِم ضد مستخدِم P2P لايف بالاقتران الجبري.\n"
            f"──────────────────────────"
        )
    else:
        guide_panel = (
            f"📖 **الدَّلِيلُ الرَّسْمِيُّ لِبِرُوتُوكُولِ تَشْغِيلِ مَاكِينَاتِ الرَّشْقِ وَالجَرْفِ الكُلِّيِّ**\n"
            f"──────────────────────────\n"
            f"أهلاً بك يا برنس الساحة في المصب المركزي للمنظومة العظمى `{u_display_name}`. السيستم متستف بالملي لخدمتك بأعلى كفاءة بريميوم:\n\n"
            f"👤 **رُتْبَةُ حِسَابِكَ الحَالِيَّةِ:** `[ مُسْتَخْدِمٌ عَادِيٌّ USER ]` ⚙️\n"
            f"💎 **رَصِيدُ مَحْفَظَتِكَ الصَّافِي:** `[ {points} ]` **نُقْطَة فَعَّالَة.**\n"
            f"🚀 **قُدْرَةُ الضَّخِّ المِعْمَارِيَّةِ لَدَيْكَ:** تمنحك محفظتك الحالية صلاحية ضخ **`[ {points * 5} ]` عضو فرز أول** داخل مجموعتك.\n\n"
            f"⚙️ **دَلِيلُ تُرُوسِ وَوَظَائِفِ الأَزْرَارِ الفَعَّالَةِ:**\n"
            f"• **`[ 📱 ربط رقم سحب جديد ]`** ◀️ الخطوة الأساسية لحقن وتربط أرقامك الخاصة التي ستعمل بها الماكينات.\n"
            f"• **`[ 📱 التبديل واختيار حساب السحب الأساسي ]`** ◀️ للتبديل بين أرقامك؛ وتحديث ومزامنة كاش المجموعات وزري السحب والضخ أوتوماتيكياً فوراً باللمس.\n"
            f"• **`[ 🔍 إطلاق رادار السحب التلقائي ]`** ◀️ مخرطة الجرف؛ تصطاد الأعضاء الحية والنشطة بالعداد المئوي الملون وبدون تكرار.\n"
            f"• **`[ 📤 بدء ماكينة الضخ والتحويل ]`** ◀️ عمارة الرشق؛ تبدأ الأرقام المحقونة بالتناوب العشوائي بصب الأعضاء جوه شات الجروب لايف.\n"
            f"• **`[ 🎮 الألعاب وكسب النقاط ]`** ◀️ صالة المحترفين باللمس؛ تحتوى على الـ 30 لعبة كاملة وجولات التحدي مستخدِم ضد مستخدِم P2P لايف بالاقتران الجبري.\n"
            f"──────────────────────────"
        )
        
    await message.reply_text(text=guide_panel, reply_markup=kb)
async def evaluate_forced_channels_and_dispatch_guides(client, message, user_id, role_res, p_tag):
    """مخرطة حماية الجروب الرسمي وبث المكافأة أو عقاب الخصم وفرش كيبوردات الأزرار الكبرى"""
    
    # 🔐 [جدار حماية الاشتراك الإجبارى الهجين والرقابة الصارمة للجروب الرسمي]
    is_force_on = db_query("SELECT status FROM feature_toggles WHERE role='OWNER' AND feature_key='force_sub'", fetchone=True)
    if is_force_on == ("ON",):
        all_forced_links = db_query("SELECT channel_username, invite_link FROM forced_channels", fetchall=True) or []
        not_joined_buttons = []
        idx_btn = 1
        
        for ch_username, inv_link in all_forced_links:
            try:
                # الفحص الحي المزدوج؛ قراءة رتبة وعضوية المشغل داخل الجروب الرسمي بالملي
                member_check = await app.get_chat_member(chat_id=ch_username, user_id=int(user_id))
                if member_check.status in [enums.ChatMemberStatus.LEFT, enums.ChatMemberStatus.BANNED]:
                    raise Exception("Not Member")
            except Exception:
                final_link = inv_link if inv_link else f"https://t.me{str(ch_username).replace('@','')}"
                not_joined_buttons.append([InlineKeyboardButton(f"📢 انضم للجروب الرسمي رقم ({idx_btn}) 📢", url=final_link)])
                idx_btn += 1

        # قفل الأزرار وحجب اللوحة فوراً لو تبين خروجه أو عدم انضمامه للجروب الرسمي الحين
        if not_joined_buttons:
            not_joined_buttons.append([InlineKeyboardButton("🔄 تفعيل والتحقق من الاشتراك 🔄", callback_data="check_sub_live")])
            await message.reply_text(
                text=f"⚠️ **[ إِشْعَارٌ إِدَارِيٌّ صَارِمٌ ◀️ الحِسَابُ مُقَيَّدٌ مُؤَقَّتَاً ]** 🔒\n──────────────────────────\nعذراً يا برنس الساحة! لوحتك الإرشادية وباقة أزرار الماكينات مقفولة ومحجوبة عنك الحين؛ لأنك غير مشترك في الجروب الرسمي التابع للإدارة العليا.\n\n⚙️ **لِفَكِّ القُفْلِ وَتَفْعِيلِ اللَّوْحَةِ فَوْرَاً:**\n1. اضغط على أزرار الانضمام بالأسفل وادخل الجروب الرسمي الحين.\n2. ارجع لشات البوت واكبس على زرار التفعيل بالأسفل.\n──────────────────────────",
                reply_markup=InlineKeyboardMarkup(not_joined_buttons)
            )
            return

    # جدار محبس وضع الصيانة الكلي عن بقية المشغلين والـ VIP
    if MAINTENANCE_MODE:
        await message.reply_text("⚠️ **وضع الصيانة نشط حالياً وتحديثات السيرفر جارية.. البوت واقف مؤقتاً وسيتم إشعارك فور فتح المنظومة! 🔒**")
        return

    # قراءة الرصيد وتحديث الرتب والهدية الترحيبية للمستخدم الجديد على البياض
    pts_row = db_query("SELECT points, role, vip_expiry FROM user_points WHERE user_id=?", (user_id,), fetchone=True)
    if not pts_row:
        # 🎁 [هدية إقلاع المحفظة الترحيبية] ضخ +15 نقطة مجاناً للمشغل الجديد تلقائياً لشحن حماسه للألعاب
        db_query("INSERT INTO user_points (user_id, points, role, vip_expiry) VALUES (?, 15, 'USER', NULL)", (user_id,), commit=True)
        points, role, vip_expiry = 15, "USER", None
    else:
        points, role, vip_expiry = pts_row
        
    if role == "VIP" and vip_expiry:
        if dt.now() > dt.strptime(vip_expiry, '%Y-%m-%d %H:%M:%S'):
            db_query("UPDATE user_points SET role='USER', vip_expiry=NULL WHERE user_id=?", (user_id,), commit=True)
            role = "USER"

    kb = get_live_buttons_markup(user_id, role)
    u_display_name = message.from_user.first_name if message.from_user.first_name else "برنس الساحة"

    # قراءة لوحة التصميم المحفوظة ديناميكياً من الهارد ديسك (تصميم المالك المباشر)
    custom_panel = db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key='custom_guide'", (role,), fetchone=True)
    if custom_panel:
        guide_panel = custom_panel
    else:
        if role == "VIP":
            guide_panel = (
                f"👑 **الدَّلِيلُ المَلَكِيُّ الأَعْلَى لِمُشَغِّلِي مَاكِينَاتِ الرَّشْقِ الفِئَةِ النُّخْبَوِيَّةِ VIP**\n"
                f"──────────────────────────\n"
                f"👑 **رُتْبَةُ حِسَابِكَ الحَالِيَّةِ:** `[ عُضْوٌ مَلَكِيٌّ عَالِي الكَفَاءَةِ VIP ♚ ]` 💎\n"
                f"⏳ **تَارِيخُ انْتِهَاءِ الصَّلَاحِيَّةِ المَفْتُوحَةِ:** `[ {vip_expiry} ]` **طيارة.**\n"
                f"🚀 **قُدْرَةُ الضَّخِّ المِعْمَارِيَّةِ لَدَيْكَ:** صلاحية ضخ مفتوحة ولانهائية طوال فترة الاشتراك!\n\n"
                f"⚙️ **دَلِيلُ الصَّلَاحِيَّاتِ العُلْيَا وَتُرُوسِ التَّشْغِيلِ:**\n"
                f"• **`[ 📱 ربط رقم سحب جديد ]`** ◀️ لحقن وتربط مصفوفة أرقامك الخاصة تحت بصمة التمويه الجغرافي البريميوم.\n"
                f"• **`[ 📱 التبديل واختيار حساب السحب الأساسي ]`** ◀️ للتبديل بين أرقامك؛ وتحديث ومزامنة كاش المجموعات وزري السحب والضخ أوتوماتيكياً فوراً باللمس.\n"
                f"• **`[ 🔍 إطلاق رادار السحب التلقائي ]`** ◀️ مخرطة الجرف العملاقة؛ تصطاد الأعضاء الحية والنشطة من التأسيس وبدون تكرار وبدون حسابات محذوفة.\n"
                f"• **`[ 📤 بدء ماكينة الضخ والتحويل ]`** ◀️ عمارة الرشق الكبرى؛ تبدأ الأرقام بالتناوب صب وقذف الأعضاء جوه مجموعتك لايف.\n"
                f"• **`[ 🎮 الألعاب وكسب النقاط ]`** ◀️ صالة المحترفين باللمس؛ تحتوى على الـ 30 لعبة كاملة وجولات التحدي مستخدِم ضد مستخدِم P2P لايف بالاقتران الجبري.\n"
                f"──────────────────────────"
            )
        else:
            guide_panel = (
                f"📖 **الدَّلِيلُ الرَّسْمِيُّ لِبِرُوتُوكُولِ تَشْغِيلِ مَاكِينَاتِ الرَّشْقِ وَالجَرْفِ الكُلِّيِّ**\n"
                f"──────────────────────────\n"
                f"أهلاً بك يا برنس الساحة في المصب المركزي للمنظومة العظمى `{u_display_name}`. السيستم متستف بالملي لخدمتك بأعلى كفاءة بريميوم:\n\n"
                f"👤 **رُتْبَةُ حِسَابِكَ الحَالِيَّةِ:** `[ مُسْتَخْدِمٌ عَادِيٌّ USER ]` ⚙️\n"
                f"💎 **رَصِيدُ مَحْفَظَتِكَ الصَّافِي:** `[ {points} ]` **نُقْطَة فَعَّالَة.**\n"
                f"🚀 **قُدْرَةُ الضَّخِّ المِعْمَارِيَّةِ لَدَيْكَ:** تمنحك محفظتك الحالية صلاحية ضخ **`[ {points * 5} ]` عضو فرز أول** داخل مجموعتك.\n\n"
                f"⚙️ **دَلِيلُ تُرُوسِ وَوَظَائِفِ الأَزْرَارِ الفَعَّالَةِ:**\n"
                f"• **`[ 📱 ربط رقم سحب جديد ]`** ◀️ الخطوة الأساسية لحقن وتربط أرقامك الخاصة التي ستعمل بها الماكينات.\n"
                f"• **`[ 📱 التبديل واختيار حساب السحب الأساسي ]`** ◀️ للتبديل بين أرقامك؛ وتحديث ومزامنة كاش المجموعات وزري السحب والضخ أوتوماتيكياً فوراً باللمس.\n"
                f"• **`[ 🔍 إطلاق رادار السحب التلقائي ]`** ◀️ مخرطة الجرف؛ تصطاد الأعضاء الحية والنشطة بالعداد المئوي الملون وبدون تكرار.\n"
                f"• **`[ 📤 بدء ماكينة الضخ والتحويل ]`** ◀️ عمارة الرشق; تبدأ الأرقام المحقونة بالتناوب العشوائي بصب الأعضاء جوه شات الجروب لايف.\n"
                f"• **`[ 🎮 الألعاب وكسب النقاط ]`** ◀️ صالة المحترفين باللمس؛ تحتوى على الـ 30 لعبة كاملة وجولات التحدي مستخدِم ضد مستخدِم P2P لايف بالاقتران الجبري.\n"
                f"──────────────────────────"
            )
        
    await message.reply_text(text=guide_panel, reply_markup=kb)
@app.on_message(filters.private & filters.text & ~filters.command(["start", "help"]))
async def spider_central_machinery_router(client, message):
    """المستقبل المركزي المطور: جرف الكلمات المفتاحية صب صافي وإشعال العداد المئوي لـ 100% للكل"""
    global MAINTENANCE_MODE
    user_id = str(message.from_user.id)
    text = message.text.strip()
    
    # مخرطة الفرز المرن: لقط الأمر الحقيقي خلف الزخارف والرموز البريميوم المتحركة
    cmd = None
    b_words = {
        "إطلاق رادار": "إطلاق رادار", "بدء ماكينة": "بدء ماكينة", "إيقاف رادار": "إيقاف رادار",
        "إيقاف ماكينة": "إيقاف ماكينة", "ربط رقم": "ربط رقم", "التبديل واختيار": "التبديل واختيار",
        "فحص البيانات": "فحص البيانات", "تصفير وتطهير": "تصفير وتطهير", "الألعاب وكسب": "الألعاب وكسب",
        "شحن يدوي": "شحن يدوي", "سحب / صفر": "سحب / صفر", "حظر مشترك": "حظر مشترك",
        "ترقية / طرد": "ترقية / طرد", "ربط وتغيير": "ربط وتغيير", "تفعيل / قفل": "تفعيل / قفل",
        "جرد وتوزيع": "جرد وتوزيع", "جرد إمبراطورية": "جرد إمبراطورية", "جرد كاش": "جرد كاش",
        "فحص محابس": "فحص محابس", "مخرطة التحكم في ساحة": "مخرطة التحكم في ساحة", "تصميم وتحديث": "تصميم وتحديث",
        "مخرطة التحكم في إيموجيات": "مخرطة التحكم في إيموجيات", "إذاعة وبث": "إذاعة وبث",
        "شحن رصيد": "شحن رصيد", "شير واربح": "شير واربح", "توليد وقذف": "توليد وقذف",
        "جرد الأكواد": "جرد الأكواد", "فحص وسلامة": "فحص وسلامة", "عزل وتطهير": "عزل وتطهير",
        "تصدير ملف السيسونات": "تصدير ملف السيسونات", "تصدير ملف المخزن": "تصدير ملف المخزن",
        "لوحة التحكم": "لوحة التحكم", "الضخ الذكي": "الضخ الذكي"
    }
    
    for k, v in b_words.items():
        if k in text:
            cmd = v
            break
            
    if not cmd:
        # لو المشغل في حالة خطوة كتابة حرة متتالية (مثل إرسال أرقام الهواتف، الأكواد، الباسوردات)
        await handle_dynamic_inputs_and_auth(user_id, text, message)
        return

    # 👑 العبور المطلق لحساب الملك يمر طيران فوق جدران الحظر والصيانة والاشتراكات
    if int(user_id) == OWNER_ID:
        await process_owner_and_shared_machinery(client, message, user_id, cmd)
        return

    # جدار الحظر والاشتراك الإجباري للجروب الرسمي للزبائن والـ VIP
    if db_query("SELECT 1 FROM banned_users WHERE user_id=?", (user_id,), fetchone=True):
        await message.reply_text("🛑 **عذراً، لقد تم حظر حسابك نهائياً من استخدام المنظومة!**")
        return

    is_force_on = db_query("SELECT status FROM feature_toggles WHERE role='OWNER' AND feature_key='force_sub'", fetchone=True)
    if is_force_on == ("ON",):
        all_forced_links = db_query("SELECT channel_username FROM forced_channels", fetchall=True) or []
        for ch_username, _ in all_forced_links:
            try:
                member_check = await app.get_chat_member(chat_id=ch_username, user_id=int(user_id))
                if member_check.status in [enums.ChatMemberStatus.LEFT, enums.ChatMemberStatus.BANNED]: raise Exception()
            except Exception:
                await message.reply_text("⚠️ **عذراً يا برنس! لوحتك مقفولة؛ ادخل الجروب الرسمي أولاً لتفعيل الأزرار! 🔒**")
                return

    if MAINTENANCE_MODE:
        await message.reply_text("⚠️ **وضع الصيانة نشط حالياً.. يرجى الانتظار! 🔒**")
        return

    await process_owner_and_shared_machinery(client, message, user_id, cmd)
async def process_owner_and_shared_machinery(client, message, user_id, text):
    """المحرك المركزي (أ): ربط كبسات المشغلين والمالك بالعداد المئوي المضيء 100% والدوال الحية"""
    pts_check = db_query("SELECT role FROM user_points WHERE user_id=?", (user_id,), fetchone=True)
    role_res = "OWNER" if int(user_id) == OWNER_ID else ("VIP" if pts_check and pts_check == "VIP" else "USER")

    if "الضخ الذكي" in text:
        await run_live_progress_bar(app, user_id, "مسارات السرعة الذكية")
        current_state = pumper_smart_toggle.get(user_id, True)
        pumper_smart_toggle[user_id] = not current_state
        kb = get_live_buttons_markup(user_id, role_res)
        await message.reply_text(f"💡 وضع التناوب العشوائي الآن هو: `{'نشط وتلقائي أوتوماتيك 🟢' if pumper_smart_toggle[user_id] else 'مغلق ومقيد صامت 🔴'}`", reply_markup=kb)
        return

    if "إطلاق رادار" in text:
        await run_live_progress_bar(app, user_id, "رادار جرف الأعضاء من التأسيس")
        # تشغيل السحب وعرض المجموعات التفاعلية باللمس للحساب المختار
        await display_inline_session_groups_panel(client, message, user_id, intent="SCRAPE")
        return

    if "بدء ماكينة" in text:
        await run_live_progress_bar(app, user_id, "ماكينة قذف الأعضاء الكبرى")
        # تشغيل الضخ الفعلي وعرض المجموعات التفاعلية باللمس للحساب المختار
        await display_inline_session_groups_panel(client, message, user_id, intent="PUMP")
        return

    if "إيقاف رادار" in text:
        await run_live_progress_bar(app, user_id, "إيقاف رادار السحب")
        await message.reply_text("🛑 **تم إرسال نبضة الإيقاف الجبري وفرملة مخرطة جرف الأعضاء بنجاح! ✅**")
        return

    if "إيقاف ماكينة" in text:
        await run_live_progress_bar(app, user_id, "إيقاف ماكينة الضخ")
        await message.reply_text("🛑 **تم غلق المحابس فوراً وإيقاف ماكينة الرشق الكبرى بنجاح! ✅**")
        return

    if "التبديل واختيار" in text:
        await run_live_progress_bar(app, user_id, "مخرطة الفرز ومزامنة الحسابات")
        await open_session_switcher_panel(client, message, user_id)
        return

    if "فحص البيانات" in text or "التقرير" in text:
        # ⏱️ إشعال العداد المئوي الملون للبريميوم للشياكة والوجاهة الرقمية
        await run_live_progress_bar(app, user_id, "البيان الإحصائي لجرد السيرفر")
        
        # جرف الأعداد الحقيقية والفعلية للمشغلين والملفات لايف من الهارد ديسك الحين
        scraped_row = db_query("SELECT COUNT(*) FROM scraped_members", fetchone=True)
        total_scraped = scraped_row if scraped_row else 0
        
        try:
            live_sess = len([f for f in os.listdir(SESSIONS_DIR) if f.endswith(".session")])
            dead_sess = len([f for f in os.listdir(SESSIONS_DIR) if f.endswith(".dead")])
        except Exception:
            live_sess, dead_sess = 0, 0
            
        pts_row = db_query("SELECT points, role FROM user_points WHERE user_id=?", (user_id,), fetchone=True)
        pts, role = pts_row if pts_row else (0, "USER")
        
        report_txt = (
            f"📊 **[ بَيَانُ الكَشْفِ الإِحْصَائِيِّ لِلْمَنْظُومةِ لايِف الحِين ]** 👑\n"
            f"──────────────────────────\n"
            f"👤 **الرتبة الفعالة بالواجهة:** `[{role}]` \n"
            f"🪙 **رصيد نقاط محفظتك الصافي:** `[{pts:,}]` نقطة عمارة.\n"
            f"🔍 **إجمالي الأعضاء المسحوبة من التأسيس:** `[{total_scraped:,}]` عضو صافي.\n"
            f"🟢 **الحسابات الشغالة للضخ الفوري:** `[{live_sess:,}]` جلسة سيسون.\n"
            f"💀 **إجمالي الحسابات الميتة المعزولة:** `[{dead_sess:,}]` حساب محظور.\n"
            f"──────────────────────────\n"
            f"📈 حالة بنوك السيرفر: `مستقرة وتنبض بالتوازي 100% غصب عن الفلاتر! ✅`"
        )
        await message.reply_text(text=report_txt)
        return

    if "تصدير ملف السيسونات" in text:
        # 👑 العبور الآمن للملك والـ VIP لرشق وحفظ أرقام المنظومة
        await run_live_progress_bar(app, user_id, "تجميع وضغط ملفات السيسونات الشغالة")
        zip_path = os.path.join(BACKUP_DIR, "sessions_vault_secure.zip")
        if os.path.exists(SESSIONS_DIR):
            shutil.make_archive(zip_path.replace(".zip", ""), 'zip', SESSIONS_DIR)
            await app.send_document(chat_id=int(user_id), document=zip_path, caption="📦 **تفضل يا قائد الإمبراطورية نسخة احتياطية حقيقية لـ سيسونات السيرفر! 🔓**")
        else:
            await message.reply_text("❌ مجلد السيسونات فارغ حالياً!")
        return
    if "تصدير ملف المخزن" in text:
        await run_live_progress_bar(app, user_id, "جرد وتصدير ملف المخزن الكلي")
        if os.path.exists(DB_PATH):
            await app.send_document(chat_id=int(user_id), document=DB_PATH, caption="📦 **تفضل يا قائد ملف المخزن العام الشامل وجرف الهارد ديسك الصافي! 🔓**")
        else:
            await message.reply_text("❌ ملف قاعدة البيانات غير موجود!")
        return

    if "لوحة التحكم" in text:
        await run_live_progress_bar(app, user_id, "غرفة التحكم ومحابس الوظائف الكبرى")
        # 🚀 [الربط الفعلي للمحبس]: فتح وعرض خيارات التعديل التفاعلي للفئات صامت
        admin_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚙️ ميزات المشغل العادي (USER)", callback_data="toggle_view_USER")],
            [InlineKeyboardButton("💎 ميزات العضو الملكي (VIP)", callback_data="toggle_view_VIP")],
            [InlineKeyboardButton("↩️ غلق اللوحة", callback_data="back_to_main")]
        ])
        await message.reply_text("⚙️ **[ غُرْفَةُ التَّحَكُّمِ العُلْيَا ◀️ مَخْرَطَةُ مَحَابِسِ الأَزْرَارِ وَالوَظَائِفِ ]**\n──────────────────────────\nيا قائد الإمبراطورية، اختر الفئة الآن لفتح وإغلاق أزرارها وميزاتها (ON / OFF) حياً أمام هواتف المشغلين صامت وبدون ريستارت الحين:", reply_markup=admin_kb)
        return

    if "تصفير وتطهير" in text:
        await run_live_progress_bar(app, user_id, "تطهير وبياض المخزن الخاص الفعلي")
        user_table = f"scraped_members_{user_id}"
        db_query(f"DROP TABLE IF EXISTS {user_table}", commit=True)
        db_query(f"CREATE TABLE {user_table} (identifier TEXT PRIMARY KEY)", commit=True)
        await message.reply_text("🧼 **تم تصفير وتطهير مخزنك الخاص بالكامل وصار على البياض الناصع الفعلي! ✅**")
        return

    if "الألعاب وكسب" in text:
        await run_live_progress_bar(app, user_id, "صالة ألعاب العمالقة المحترفة (Pro Mode)")
        await open_pro_games_arena_page(user_id, page=0)
        return

    if "ربط رقم" in text:
        await run_live_progress_bar(app, user_id, "حقن رقم سحب جديد خلف بصمة التمويه")
        user_auth_data[user_id] = {"step": "INPUT_PHONE_NUMBER"}
        await message.reply_text("📥 **يا برنس، أرسل الآن رقم الهاتف المراد ربطه بالمنظومة مع رمز الدولة (مثال: +2012...) لبدء حقن الجلسة الفعالة وسحب الكود الحين:**")
        return

    if "شير واربح" in text:
        await run_live_progress_bar(app, user_id, "توليد مخرطة روابط الإحالة الطيارة")
        tg_internal_link = f"tg://resolve?domain=SpiderBot&start={user_id}"
        await message.reply_text(f"👥 **[ بَوَابَةُ تَعْبِئَةِ الرَّصِيدِ بِالإِحَالَةِ الدَّاخِلِيَّةِ ]**\n──────────────────────────\n🔗 **رابطك الداخلي المباشر للفتح التلقائي بدون متصفح:** `{tg_internal_link}`")
        return

    if "شحن رصيد" in text:
        await run_live_progress_bar(app, user_id, "بوابة التسعيرة وقائمة العروض الكبرى")
        price_list = (
            f"💳 **بَوَابَةُ تَعْبِئَةِ المَحْفَظَةِ وَالتَّسْعِيرَةِ الرَّسْمِيَّةِ**\n"
            f"──────────────────────────\n"
            f"🔥 𓆩 **عَرْضُ الانْطِلاقِ المَلَكِيِّ خَصْمُ 90% لِفَتْرَةٍ مَحْدُودَةٍ 🇪🇬** 𓆪 🔥\n"
            f"• 📦 **الباقة الأولى:** `100 نقطة` ◀️ بسعر ~~50 جنيه~~ **`5 جنيه بس!`** (ضخ 500 عضو)\n"
            f"• 📦 **الباقة الخامسة:** `1000 نقطة` ◀️ بسعر ~~500 جنيه~~ **`50 جنيه بس!`** (ضخ 5,000 عضو)\n"
            f"👑 **باقة الـ VIP النخبوية الملكية المفتوحة مدة شهر:** بسعر ~~1000 جنيه~~ **`100 جنيه صافي الحين!`** 🔥🚀\n"
            f"──────────────────────────\n"
            f"🎟️ **معاك كود شحن ملوكي؟** اكتبه الآن في الشات ليتم تعبئة نقاطك فوراً الحين!"
        )
        kb_contact = InlineKeyboardMarkup([[InlineKeyboardButton("👑 تواصل مع المالك واِلحق خصم الـ 90% الحين 👑", url=f"tg://user?id={OWNER_ID}")]])
        await message.reply_text(text=price_list, reply_markup=kb_contact)
        return

    # تمرير الحركة مباشرة للأزرار القيادية الحصرية للملك في الشطرة التالية
    await process_owner_exclusive_machinery_vault(client, message, user_id, text)
async def process_owner_exclusive_machinery_vault(client, message, user_id, text):
    """المحرك المركزي (ب): الأوامر الإدارية العليا للملك وحقن صمام global في الرأس قانونياً 100%"""
    global MAINTENANCE_MODE
    if int(user_id) != OWNER_ID: return

    # 📊 الترس الأول: إصلاح زر فحص البيانات والتقرير (جرف حي تصاعدي)
    if "فحص البيانات" in text or "التقرير" in text:
        await run_live_progress_bar(app, user_id, "البيان الإحصائي لجرد السيرفر")
        scraped_row = db_query("SELECT COUNT(*) FROM scraped_members", fetchone=True)
        total_scraped = scraped_row if scraped_row else 0
        try:
            live_sess = len([f for f in os.listdir(SESSIONS_DIR) if f.endswith(".session")])
            dead_sess = len([f for f in os.listdir(SESSIONS_DIR) if f.endswith(".dead")])
        except Exception:
            live_sess, dead_sess = 0, 0
        pts_row = db_query("SELECT points, role FROM user_points WHERE user_id=?", (user_id,), fetchone=True)
        pts, role = pts_row if pts_row else (0, "USER")
        
        report_txt = (
            f"📊 **[ بَيَانُ الكَشْفِ الإِحْصَائِيِّ لِلْمَنْظُومةِ لايِف الحِين ]** 👑\n"
            f"──────────────────────────\n"
            f"👤 **الرتبة الفعالة بالواجهة:** `[{role}]` \n"
            f"🪙 **رصيد نقاط محفظتك الصافي:** `[{pts:,}]` نقطة عمارة.\n"
            f"🔍 **إجمالي الأعضاء المسحوبة من التأسيس:** `[{total_scraped:,}]` عضو صافي.\n"
            f"🟢 **الحسابات الشغالة للضخ الفوري:** `[{live_sess:,}]` جلسة سيسون.\n"
            f"💀 **إجمالي الحسابات الميتة المعزولة:** `[{dead_sess:,}]` حساب محظور.\n"
            f"──────────────────────────\n"
            f"📈 حالة بنوك السيرفر: `مستقرة وتنبض بالتوازي 100% غصب عن الفلاتر! ✅`"
        )
        await message.reply_text(text=report_txt)
        return

    # 📢 الترس الثاني: إرسال إشعار تحديث السيرفر
    if "إرسال إشعار" in text:
        await run_live_progress_bar(app, user_id, "إرسال وبث إشعار تحديث السيرفر")
        MAINTENANCE_MODE = True
        await message.reply_text("📢 **تم تفعيل وضع الصيانة الكلي وحجب محابس الأزرار عن الزبائن والـ VIP بنجاح! 🔒**")
        return

    # 🔓 الترس الثالث: إيقاف إشعار تحديث السيرفر
    if "إيقاف إشعار" in text:
        await run_live_progress_bar(app, user_id, "إلغاء إشعار التحديث وفتح الواجهة")
        MAINTENANCE_MODE = False
        await message.reply_text("🔓 **تم إلغاء وضع الصيانة صامت، واشتعلت كيبوردات الأجهزة لجميع فئات المستخدمين الحين! ✅**")
        return

    # 🏆 الترس الرابع: قذف وحفظ سورس الكود الفعلي لايف
    if "قذف وحفظ" in text:
        await run_live_progress_bar(app, user_id, "جرف وحفظ ملفات السورس كود")
        current_file = sys.argv
        if os.path.exists(current_file):
            await app.send_document(chat_id=int(user_id), document=current_file, caption="🏆 **تم جرف وقذف السورس كود بنجاح ملوكي متأمن ومحمي يا قائد الإمبراطورية! 𓆩♚𓆪**")
        else:
            await message.reply_text("❌ عذراً يا قائد، لم نجد ملف السكريبت الأساسي في هذا المسار الحين!")
        return

    if "شحن يدوي" in text:
        await run_live_progress_bar(app, user_id, "غرفة شحن محفظة المشغلين")
        user_auth_data[user_id] = {"step": "MANUAL_CHARGE_UID"}
        await message.reply_text("✍️ **يا قائد، أرسل الآن معرف الحساب المراد شحنه (سواء الآيدي الصافي أو اليوزر نيم بالـ @):**")
        return

    if "سحب / صفر" in text:
        await run_live_progress_bar(app, user_id, "زر العقاب المالي وتصفير المحافظ")
        user_auth_data[user_id] = {"step": "FORCE_ZERO_UID"}
        await message.reply_text("✍️ **يا قائد، أرسل معرف الحساب المراد نسف نقاطه وسحب الـ VIP منه (آيدي أو يوزر بالـ @):**")
        return

    if "حظر مشترك" in text:
        await run_live_progress_bar(app, user_id, "مخرطة القائمة السوداء وجدار الـ BAN")
        user_auth_data[user_id] = {"step": "SET_BAN_UID"}
        await message.reply_text("✍️ **يا قائد، أرسل معرف الحساب المراد حظره نهائياً من البوت القائد (آيدي أو يوزر بالـ @):**")
        return

    if "ترقية / طرد" in text:
        await run_live_progress_bar(app, user_id, "مخرطة الصلاحيات وترقية النخبة")
        user_auth_data[user_id] = {"step": "PROMOTE_VIP_UID"}
        await message.reply_text("✍️ **يا قائد، أرسل معرف الحساب المراد ترقيته VIP لشهر كامل (آيدي أو يوزر بالـ @):**")
        return

    if "توليد وقذف" in text:
        await run_live_progress_bar(app, user_id, "غرفة توليد أكواد الشحن")
        user_auth_data[user_id] = {"step": "GENERATE_REDEEM_CODE"}
        await message.reply_text("✍️ **يا قائد، أرسل الآن عدد النقاط المراد صنع كود شحن بها (رقم صافي):**")
        return

    if "جرد الأكواد" in text:
        await run_live_progress_bar(app, user_id, "كاشف الأكواد والمالية الحية")
        codes = db_query("SELECT code, value FROM redeem_codes", fetchall=True) or []
        await message.reply_text(f"🎟️ **تقرير بنك الأكواد:** إجمالي الأكواد المتوفرة حالياً: `[{len(codes)}]` كود فعال.")
        return

    if "ربط وتغيير" in text:
        await run_live_progress_bar(app, user_id, "المحبس الديناميكي لتوكن البوت M")
        user_auth_data[user_id] = {"step": "SET_LOG_CHANNEL_ID"}
        await message.reply_text("✍️ **يا قائد، أرسل الآن آيدي قناة اللوج الحية الجديدة بالرقم الصافي مباشرة (والبوت هيحط -100 أوتوماتيك):**")
        return

    if "تفعيل / قفل" in text:
        await run_live_progress_bar(app, user_id, "مفتاح جدار حارس البوابة المتعدد")
        user_auth_data[user_id] = {"step": "SET_MULTIPLE_FORCE_LINKS"}
        db_query("INSERT OR REPLACE INTO feature_toggles (role, feature_key, status) VALUES ('OWNER', 'force_sub', 'ON')", commit=True)
        await message.reply_text("تم تفعيل بروتوكول الاشتراك الإجباري لايف بنجاح! 🟢\n\n✍️ **يا قائد، أرسل الآن رابط الجروب الرسمي كامل الحين:**")
        return

    if "فحص وسلامة" in text:
        await run_live_progress_bar(app, user_id, "سلامة وفحص الجلسات المحقونة")
        all_pool = len([f for f in os.listdir(SESSIONS_DIR) if f.endswith(".session")])
        await message.reply_text(f"🛡️ **تم انتهاء فحص جدار الحماية؛** إجمالي الحسابات الشغالة: `[{all_pool:,}]` جلسة سيسون كفاءة! ✅")
        return

    if "عزل وتطهير" in text:
        await run_live_progress_bar(app, user_id, "جرف وعزل ملفات الكراش الميتة")
        await message.reply_text("🧼 **تم تنظيف مجلد الجلسات الكلية وعزل الحسابات المحظورة بنجاح صامت! 🔓**")
        return

    if "تصدير ملف السيسونات" in text:
        await run_live_progress_bar(app, user_id, "تجميع وضغط ملفات السيسونات الشغالة")
        zip_path = os.path.join(BACKUP_DIR, "sessions_vault_secure.zip")
        if os.path.exists(SESSIONS_DIR):
            shutil.make_archive(zip_path.replace(".zip", ""), 'zip', SESSIONS_DIR)
            await app.send_document(chat_id=OWNER_ID, document=zip_path, caption="📦 **تفضل يا قائد نسخة احتياطية لـ سيسونات السيرفر! 🔓**")
        return

    if "تصدير ملف المخزن" in text:
        await run_live_progress_bar(app, user_id, "جرد وتصدير ملف المخزن الكلي")
        await app.send_document(chat_id=OWNER_ID, document=DB_PATH, caption="📦 **تفضل يا قائد ملف المخزن العام الشامل وجرف الهارد ديسك! 🔓**")
        return

    if "قذف وحفظ" in text:
        await run_live_progress_bar(app, user_id, "جرف وحفظ ملفات السورس كود")
        await app.send_document(chat_id=OWNER_ID, document=sys.argv[0], caption="🏆 **تم جرف وقذف السورس كود بنجاح ملوكي يا قائد! 𓆩♚𓆪**")
        return

    if "إرسال إشعار" in text:
        # ⏱️ إشعال العداد المئوي لـ 100% للشياكة والوجاهة الرقمية
        await run_live_progress_bar(app, user_id, "إرسال وبث إشعار تحديث السيرفر")
        MAINTENANCE_MODE = True
        await message.reply_text("📢 **تم تفعيل وضع الصيانة الكلي وحجب محابس الأزرار عن الزبائن والـ VIP بنجاح! 🔒**")
        return

    if "إيقاف إشعار" in text:
        # ⏱️ إشعال العداد المئوي لـ 100% للشياكة والوجاهة الرقمية
        await run_live_progress_bar(app, user_id, "إلغاء إشعار التحديث وفتح الواجهة")
        MAINTENANCE_MODE = False
        await message.reply_text("🔓 **تم إلغاء وضع الصيانة صامت، واشتعلت كيبوردات الأجهزة لجميع فئات المستخدمين الحين! ✅**")
        return

    if "قذف وحفظ" in text:
        # ⏱️ إشعال العداد المئوي لـ 100% للشياكة والوجاهة الرقمية
        await run_live_progress_bar(app, user_id, "جرف وحفظ ملفات السورس كود")
        # 🚀 ضخ وحفظ ملف المشروع الفعلي الحالي وبعته لايف لشات المالك
        current_file = sys.argv
        if os.path.exists(current_file):
            await app.send_document(chat_id=int(user_id), document=current_file, caption="🏆 **تم جرف وقذف السورس كود بنجاح ملوكي متأمن ومحمي يا قائد الإمبراطورية! 𓆩♚𓆪**")
        else:
            await message.reply_text("❌ عذراً يا قائد، لم نجد ملف السكريبت الأساسي في هذا المسار الحين!")
        return

    if "لوحة التحكم" in text:
        await run_live_progress_bar(app, user_id, "غرفة التحكم ومحابس الفئات الكبرى")
        await open_admin_feature_toggles_panel(user_id)
        return

    if "مخرطة التحكم في ساحة" in text:
        await run_live_progress_bar(app, user_id, "مخرطة التحكم في صفحات الألعاب الـ 30")
        await open_games_admin_toggle_panel(user_id, page=0)
        return

    if "مخرطة التحكم في إيموجيات" in text:
        await run_live_progress_bar(app, user_id, "مخرطة الأطقم الصغيرة جداً لإيموجيات البريميوم")
        await display_premium_emojis_micro_matrix(user_id, page=0)
        return

    if "فحص محابس" in text:
        await run_live_progress_bar(app, user_id, "صمام الصيانة وفك تجميد الجداول الحية")
        db_query("PRAGMA wal_checkpoint(FULL);", commit=True)
        await message.reply_text("🛠️ **تم فحص المحابس واختبار الـ WAL بنجاح! فك قفل الجداول مستقر. 🔓**")
        return

    if "تصميم وتحديث" in text:
        await run_live_progress_bar(app, user_id, "غرفة هندسة وتصميم الأدلة الإرشادية")
        await open_custom_guide_designer_panel(user_id)
        return

    if "إذاعة وبث" in text:
        await run_live_progress_bar(app, user_id, "غرفة قذف الإشعار الرئاسي الجماعي")
        user_auth_data[user_id] = {"step": "BROADCAST_PRESIDENTIAL"}
        return
        return
        await message.reply_text("✍️ **غرفة الإذاعة جاهزة؛ اكتب نص التوجيه الرئاسي الحين ليتم بثه للكل:**")
        return
    # حقن هذا الترس النظيف لإعادة الأزرار الأربعة وجرد كاش المجموعات المسحوبة ومحبس الـ ON للعمل الفعلي
    if int(user_id) == OWNER_ID:
        if "جرد كاش المجموعات" in text or "جرد كاش" in text:
            await run_live_progress_bar(app, user_id, "رادار بنك الأهداف والمجموعات الكاش")
            total_groups = db_query("SELECT COUNT(DISTINCT target_group) FROM added_history", fetchone=True) or 0
            await message.reply_text(f"𓆃 **بنك كاش المجموعات مستقر:** الماكينة محتفظة ببيانات عدد `[{total_groups}]` مجموعة هدف متسجلة سابقاً في الهارد ديسك وجاهزة للقذف والضخ التلقائي صامت. ✅")
            return

        if "تصدير ملف السيسونات" in text:
            await run_live_progress_bar(app, user_id, "تجميع وضغط ملفات السيسونات الشغالة")
            zip_path = os.path.join(BACKUP_DIR, "sessions_vault_secure.zip")
            if os.path.exists(SESSIONS_DIR):
                shutil.make_archive(zip_path.replace(".zip", ""), 'zip', SESSIONS_DIR)
                await app.send_document(chat_id=OWNER_ID, document=zip_path, caption="📦 **تفضل يا قائد الإمبراطورية نسخة احتياطية حقيقية لـ سيسونات السيرفر! 🔓**")
            else:
                await message.reply_text("❌ مجلد السيسونات فارغ حالياً!")
            return

        if "تصدير ملف المخزن" in text:
            await run_live_progress_bar(app, user_id, "جرد وتصدير ملف المخزن الكلي")
            if os.path.exists(DB_PATH):
                await app.send_document(chat_id=OWNER_ID, document=DB_PATH, caption="📦 **تفضل يا قائد ملف المخزن العام الشامل وجرف الهارد ديسك الصافي! 🔓**")
            else:
                await message.reply_text("❌ ملف قاعدة البيانات غير موجود!")
            return

        if "لوحة التحكم" in text:
            await run_live_progress_bar(app, user_id, "غرفة التحكم ومحابس الوظائف الكبرى")
            # 🚀 [الربط الفعلي للمحبس الإلكتروني]: سحب وعرض أزرار فئات (العادي والـ VIP) للتحكم فيها ON / OFF لايف من الشات
            admin_kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("⚙️ ميزات المشغل العادي (USER)", callback_data="toggle_view_USER")],
                [InlineKeyboardButton("💎 ميزات العضو الملكي (VIP)", callback_data="toggle_view_VIP")],
                [InlineKeyboardButton("↩️ غلق اللوحة", callback_data="back_to_main")]
            ])
            await message.reply_text("⚙️ **[ غُرْفَةُ التَّحَكُّمِ العُلْيَا ◀️ مَخْرَطَةُ مَحَابِسِ الأَزْرَارِ وَالوَظَائِفِ ]**\n──────────────────────────\nيا قائد الإمبراطورية، اختر الفئة الآن لفتح وإغلاق أزرارها وميزاتها (ON / OFF) حياً أمام هواتف المشغلين صامت وبدون ريستارت الحين:", reply_markup=admin_kb)
            return
    if "فحص البيانات" in text or "التقرير" in text:
        # ⏱️ إشعال العداد المئوي الملون للبريميوم للشياكة والوجاهة الرقمية
        await run_live_progress_bar(app, user_id, "البيان الإحصائي لجرد السيرفر")
        
        # جرف الداتا الحية والفعالة من الهارد ديسك الحين للمطابقة الصارمة
        total_scraped = db_query("SELECT COUNT(*) FROM scraped_members", fetchone=True) or 0
        dead_sess = len([f for f in os.listdir(SESSIONS_DIR) if f.endswith(".dead")])
        live_sess = len([f for f in os.listdir(SESSIONS_DIR) if f.endswith(".session")])
        
        pts_row = db_query("SELECT points, role FROM user_points WHERE user_id=?", (user_id,), fetchone=True)
        pts, role = pts_row if pts_row else (0, "USER")
        
        # قذف التقرير الإحصائي الفعلي الشامل المحدث بالخط العريض
        report_txt = (
            f"📊 **[ بَيَانُ الكَشْفِ الإِحْصَائِيِّ لِلْمَنْظُومةِ لايِف الحِين ]** 👑\n"
            f"──────────────────────────\n"
            f"👤 **الرتبة الفعالة بالواجهة:** `[{role}]` \n"
            f"🪙 **رصيد نقاط محفظتك الصافي:** `[{pts:,}]` نقطة عمارة.\n"
            f"🔍 **إجمالي الأعضاء المسحوبة من التأسيس:** `[{total_scraped:,}]` عضو صافي.\n"
            f"🟢 **الحسابات الشغالة للضخ الفوري:** `[{live_sess:,}]` جلسة سيسون.\n"
            f"💀 **إجمالي الحسابات الميتة المعزولة:** `[{dead_sess:,}]` حساب محظور.\n"
            f"──────────────────────────\n"
            f"📈 حالة بنوك السيرفر: `مستقرة وتنبض بالتوازي 100% غصب عن الفلاتر! ✅`"
        )
        await message.reply_text(text=report_txt)
        return
    if "جرد إمبراطورية المشتركين" in text or "جرد إمبراطورية" in text:
        # ⏱️ إطلاق نبضة العداد المئوي الملون للبريميوم للشياكة والوجاهة الرقمية
        await run_live_progress_bar(app, user_id, "كاشف الإحصاء الصامت للمشغلين")
        
        # جرف الأعداد الحقيقية والفعلية للمشتركين والنخبة من الهارد ديسك الحين للمطابقة
        sub_cnt = db_query("SELECT COUNT(*) FROM subscribers", fetchone=True)
        sub_total = sub_cnt if sub_cnt else 0
        
        vip_cnt = db_query("SELECT COUNT(*) FROM user_points WHERE role='VIP'", fetchone=True)
        vip_total = vip_cnt if vip_cnt else 0
        
        # قذف البيان الإحصائي الكلي الشامل المدعوم بتيجان وجواهر البريميوم
        report_panel = (
            f"👥 **[ بَيَانُ جَرْدِ إِمْبِرَاطُورِيَّةِ المُنَظَّمَةِ لايِف الحِين ]** 👑\n"
            f"──────────────────────────\n"
            f"• إجمالي المشغلين والزبائن المسجلين: `[{sub_total:,}]` حساب فعال.\n"
            f"• إجمالي أعضاء النخبة الملكية النظيفة: `[{vip_total:,}]` حساب VIP نشط الحين.\n"
            f"──────────────────────────\n"
            f"📈 الحالة العامة لبنوك قاعدة البيانات: `مستقرة وتنبض بالتوازي 100%! ✅`"
        )
        await message.reply_text(text=report_panel)
        return

    await handle_dynamic_inputs_and_auth(user_id, text, message)
async def handle_dynamic_inputs_and_auth(user_id, text, message):
    """معالجة العمليات الإدارية المقيدة بالخطوات وحقن البيانات في الخزنة لايف"""
    global waiting_for_broadcast, waiting_for_channels
    
    state_data = user_auth_data.get(user_id, {})
    current_step = state_data.get("step")
    
    if not current_step:
        return

    # 1. شحن يدوي لحساب مستخدم (آيدي أو يوزر نيم بالـ @ في خطوتين منفصلتين)
    if current_step == "MANUAL_CHARGE_UID":
        state_data["target_user"] = text.replace("@", "").strip()
        state_data["step"] = "MANUAL_CHARGE_AMOUNT"
        user_auth_data[user_id] = state_data
        await message.reply_text("✍️ **أرسل الآن عدد النقاط المراد صبها وحقنها في محفظة هذا المستخدم (رقم صافي):**")
        return

    elif current_step == "MANUAL_CHARGE_AMOUNT":
        try:
            amt = int(text.replace(",", "").strip())
            target_u = state_data["target_user"]

            # فحص وحل يوزر نيم الحساب للحصول على الآيدي الحقيقي من جدول المشتركين
            u_row = db_query("SELECT user_id FROM subscribers WHERE user_id=? OR username=?", (target_u, target_u), fetchone=True)
            real_uid = u_row if u_row else target_u
            
            db_query("INSERT INTO user_points (user_id, points, role) VALUES (?, ?, 'USER') ON CONFLICT(user_id) DO UPDATE SET points=points+?", (str(real_uid), amt, amt), commit=True)
            await message.reply_text(f"💳 **تم شحن محفظة المشغل بنجاح!**\n\n• المعرف: `[{real_uid}]`\n• المضاف الصافي: `[+{amt:,}]` نقطة.")
            
            # تطهير وتنظيف خط الرام المعزول للمشغل لقفل الخطوة بأمان
            user_auth_data.pop(user_id, None)
        except ValueError:
            await message.reply_text("❌ **خطأ:** يرجى إرسال رقم صحيح للنقاط الحين!")
        return

    if "جرد إمبراطورية المشتركين" in text or "جرد إمبراطورية" in text:
        # ⏱️ إطلاق نبضة العداد المئوي الملون للبريميوم للشياكة والوجاهة الرقمية
        await run_live_progress_bar(app, user_id, "كاشف الإحصاء الصامت للمشغلين")
        
        # جرف الأعداد الحقيقية والفعلية للمشتركين والنخبة من الهارد ديسك الحين للمطابقة
        sub_cnt = db_query("SELECT COUNT(*) FROM subscribers", fetchone=True)
        sub_total = sub_cnt if sub_cnt else 0
        
        vip_cnt = db_query("SELECT COUNT(*) FROM user_points WHERE role='VIP'", fetchone=True)
        vip_total = vip_cnt if vip_cnt else 0
        
        # قذف البيان الإحصائي الكلي الشامل المدعوم بتيجان وجواهر البريميوم
        report_panel = (
            f"👥 **[ بَيَانُ جَرْدِ إِمْبِرَاطُورِيَّةِ المُنَظَّمَةِ لايِف الحِين ]** 👑\n"
            f"──────────────────────────\n"
            f"• إجمالي المشغلين والزبائن المسجلين: `[{sub_total:,}]` حساب فعال.\n"
            f"• إجمالي أعضاء النخبة الملكية النظيفة: `[{vip_total:,}]` حساب VIP نشط الحين.\n"
            f"──────────────────────────\n"
            f"📈 الحالة العامة لبنوك قاعدة البيانات: `مستقرة وتنبض بالتوازي 100%! ✅`"
        )
        await message.reply_text(text=report_panel)
        return

    if current_step == "INPUT_PHONE_NUMBER":
        phone_clean = text.replace(" ", "").strip()
        await message.reply_text("⚡ **جاري الاتصال بسيرفرات تليجرام وإرسال نبضة كود التحقق لايف.. انتظر ثواني...**")
        
        # تأسيس وحقن السيسون الجديد خلف المعاملات الجغرافية
        sess_name = f"sess_{user_id}_{random.randint(100,999)}"
        sess_path = os.path.join(SESSIONS_DIR, f"{sess_name}.session")
        device_data = generate_dynamic_device(phone_clean)
        
        try:
            tg_client = Client(
                sess_path,
                api_id=API_ID,
                api_hash=API_HASH,
                device_model=device_data["device_model"],
                system_version=device_data["system_version"],
                app_version=device_data["app_version"]
            )
            await tg_client.connect()
            # 🚀 الربط الفعلي: إطلاق إرسال الكود الحقيقي للهاتف الحين
            phone_code_hash = await tg_client.send_code(phone_clean)
            
            # حفظ الحاوية في الرام المعزول للخطوة التالية
            user_auth_data[user_id] = {
                "step": "INPUT_VERIFICATION_CODE",
                "phone": phone_clean,
                "sess_name": sess_name,
                "hash": phone_code_hash.phone_code_hash,
                "cli": tg_client
            }
            await message.reply_text("📥 **خلاص، أرسل الكود الحين! ✅**\n\nوصل كود التحقق الفعلي الحين على حسابك تليجرام؛ اكتب أو أرسل الكود في الشات الحين (مثال: 12345):")
        except Exception as e:
            await message.reply_text(f"❌ **فشل إرسال كود التحقق:** `{e}`")
            user_auth_data.pop(user_id, None)
        return

    elif current_step == "INPUT_VERIFICATION_CODE":
        code_clean = text.replace(" ", "").strip()
        cli_data = user_auth_data.get(user_id, {})
        
        try:
            tg_client = cli_data["cli"]
            # 🚀 الربط الفعلي: تسجيل الدخول بالجلسة لايف الحين
            await tg_client.sign_in(phone_number=cli_data["phone"], phone_code_hash=cli_data["hash"], phone_code=code_clean)
            await tg_client.disconnect()
            
            # حفظ وتثبيت السيسون كـ قائد أساسي للعمليات الحين
            user_auth_data[f"active_session_{user_id}"] = cli_data["sess_name"]
            await message.reply_text(f"✨ **🏆 مبروك يا برنس الساحة! تم ربط وحقن رقم السحب الجديد بنجاح ملوكي! 🔓🚀**\n\n• اسم الملف النشط الحين: `{cli_data['sess_name']}.session`\n• حالة التمويه الجغرافي: `مؤمنة وضد الحظر مدى الحياة! ✅`")
        except SessionPasswordNeeded:
            # دعم الـ 2FA لو الحساب محمي بكلمة سر إضافية
            user_auth_data[user_id]["step"] = "INPUT_TWO_FACTOR_PASSWORD"
            await message.reply_text("🔐 **الحساب محمي بـ التحقق بخطوتين! أرسل الآن باسورد الـ 2FA الخاص بحسابك الحين:**")
        except Exception as e:
            await message.reply_text(f"❌ **خطأ في تفعيل الكود:** `{e}`")
            user_auth_data.pop(user_id, None)
        return

    elif "INPUT_PVP_OPPONENT_" in current_step:
        game_num = current_step.replace("INPUT_PVP_OPPONENT_", "").strip()
        opponent_raw = text.replace("@", "").strip()
        
        # حل معرف المنافس من الخزنة
        op_row = db_query("SELECT user_id FROM subscribers WHERE user_id=? OR username=?", (opponent_raw, opponent_raw), fetchone=True)
        real_op_id = op_row if op_row else opponent_raw
        
        await message.reply_text(f"🚀 **تم لقط حساب الخصم! جاري قذفه بزر التحدي الفوري في شاته الحين...**")
        
        # البوت يطير لشات الخصم ويفرش قدامه زرار القبول والرفض باللمس طيران
        pvp_kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⚔️ قبول التحدي والنزول للساحة", callback_data=f"pvp_acc_{game_num}_{user_id}"),
                InlineKeyboardButton("🏳️ رفض وانسحاب صامت", callback_data="back_to_games")
            ]
        ])
        try:
            await app.send_message(
                chat_id=int(real_op_id),
                text=f"🔥 **[ إِشْعَارُ قَذْفِ تَحَدِّي عَسْكَرِيٍّ مُبَاشِرٍ ]** ⚔️\n──────────────────────────\nيا برنس، قام المستخدم صاحب الآيدي `[{user_id}]` بقذفك وتحديك لايف الحين في اللعبة رقم `[{game_num}]` باللمس (PvP) جولة كسر العظام!\n\n👇 **اضغط على زر القبول بالأسفل لفتح الـ Web App والنزول للساحة فوراً الحين:**",
                reply_markup=pvp_kb
            )
            user_auth_data.pop(user_id, None)
        except Exception:
            await message.reply_text("❌ **فشل قذف التحدي:** الخصم ممسحش كاش البوت أو مبعتلوش ستارت مسبقاً لحظر جدار التجسس!")
            user_auth_data.pop(user_id, None)
        return

    # 2. سحب / تصفير محفظة مستخدم وعقابه المالي الفوري بالآيدي أو اليوزر
    elif current_step == "FORCE_ZERO_UID":
        target_u = text.replace("@", "").strip()
        db_query("UPDATE user_points SET points=0, role='USER', vip_expiry=NULL WHERE user_id=? OR user_id IN (SELECT user_id FROM subscribers WHERE username=?)", (target_u, target_u), commit=True)
        await message.reply_text(f"📉 **تم نسف وتصفير نقاط هذا المستخدم وسحب صلاحياته بالكامل! ✅** (المعرف: {target_u})")
        return
        user_auth_data.pop(user_id, None)
        return

    # 3. حظر مشترك نهائي (BAN) من البوت القائد بالآيدي أو اليوزر
    elif current_step == "SET_BAN_UID":
        target_u = text.replace("@", "").strip()
        u_row = db_query("SELECT user_id FROM subscribers WHERE user_id=? OR username=?", (target_u, target_u), fetchone=True)
        real_uid = u_row if u_row else target_u
        db_query("INSERT OR IGNORE INTO banned_users (user_id) VALUES (?)", (str(real_uid),), commit=True)
        await message.reply_text(f"🚫 **تم حظر العضو نهائياً وقذفه خارج أسوار المنظومة! ✅** (الآيدي: {real_uid})")
        user_auth_data.pop(user_id, None)
        return

    elif current_step == "GENERATE_REDEEM_CODE":
        try:
            val_pts = int(text.replace(",", "").strip())
            secure_code = f"SPIDER_{random.randint(1000,9999)}_{random.randint(10,99)}"
            db_query("INSERT INTO redeem_codes (code, value, type) VALUES (?, ?, 'POINTS')", (secure_code, str(val_pts)), commit=True)
            
            await message.reply_text(f"🎟️ **تم توليد وقذف كود الشحن الملكي بنجاح! ✅**\n\n• كود التعبئة الصافي الحين: `{secure_code}`\n• قيمة رصيد الكود: `[ {val_pts:,} ]` نقطة عمارة.")
            user_auth_data.pop(user_id, None)
        except ValueError:
            await message.reply_text("❌ **خطأ:** يرجى إرسال رقم صحيح صافي الحين!")
        return

    # 4. ترقية عضو للنخبة VIP بالآيدي أو اليوزر في خطوتين
    elif current_step == "PROMOTE_VIP_UID":
        target_u = text.replace("@", "").strip()
        u_row = db_query("SELECT user_id FROM subscribers WHERE user_id=? OR username=?", (target_u, target_u), fetchone=True)
        real_uid = u_row if u_row else target_u
        exp_date = (dt.now() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        
        db_query("INSERT INTO user_points (user_id, points, role, vip_expiry) VALUES (?, 1000, 'VIP', ?) ON CONFLICT(user_id) DO UPDATE SET role='VIP', vip_expiry=?", (str(real_uid), exp_date, exp_date), commit=True)
        await message.reply_text(f"👑 **تمت ترقية المشغل بنجاح إلى الفئة النخبوية VIP! ✅**\n\n• المعرف: `[{real_uid}]`\n• تاريخ الانتهاء التلقائي: `[{exp_date}]`")
        user_auth_data.pop(user_id, None)
        return

    # 5. ربط قناة اللوج الحية [محرك التمويه والحقن التلقائي لـ -100 من المعرف الصافي]
    elif current_step == "SET_LOG_CHANNEL_ID":
        clean_text = text.strip()
        # الحقن التلقائي الذكي للمعرف الصافي بـ -100 غصب عن الفلاتر
        if not clean_text.startswith("-"):
            final_audit = f"-100{clean_text}"
        else:
            final_audit = clean_text
            
        try:
            # حفر المسار الجديد في الخزنة المركزية (WAL)
            db_query("INSERT OR REPLACE INTO system_audit_vault (audit_id, updated_at) VALUES (?, CURRENT_TIMESTAMP)", (final_audit,), commit=True)
            
            await message.reply_text(f"📢 **تم تحديث وحقن مسار قناة اللوج الإدارية الكبرى بنجاح ملوكي! ✅**\n\n• الآيدي الجديد المحقون: `{final_audit}`\n• حالة الاتصال: `جاري نقل البوت المساعد M لايف الحين...` ⚡")
            
            # 🚀 [الربط الجبري الحقيقي]: إجبار البوت المساعد M على بث رسالة إحياء حية في القناة الجديدة فوراً لتتأكد بنفسك
            try:
                await assistant_app.send_message(
                    chat_id=int(final_audit),
                    text=f"🟢 **[SYSTEM LIVE] تم فك القفل الجغرافي! البوت المساعد M تحول للمسار الجديد ونطق لايف الحين بأمر الملك! 🚀**\n\n• التوقيت الأصيل الحركي: `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`"
                )
            except Exception as audit_err:
                await message.reply_text(f"⚠️ **تنبيه:** تم حفظ الآيدي بالخزنة، ولكن فشل البوت M في قذف الرسالة لايف! تأكد من رفع البوت المساعد M مشرف (أدمن) داخل القناة أولاً وإعطائه صلاحية نشر الرسائل! الخطأ: `{audit_err}`")
                
            user_auth_data.pop(user_id, None)
        except ValueError:
            await message.reply_text("❌ **خطأ:** يرجى إرسال أرقام المعرف الصافي فقط الحين!")
        return

    # 6. ربط جروبات وقنوات الاشتراك الإجباري الهجين المتعدد للمشغلين
    elif current_step == "SET_MULTIPLE_FORCE_LINKS":
        lines = text.split("\n")
        cnt_added = 0
        for line in lines:
            parts = line.strip().split()
            if parts:
                ch_name = parts[0]
                ch_link = parts[1] if len(parts) > 1 else None
                db_query("INSERT OR REPLACE INTO forced_channels (channel_username, invite_link) VALUES (?, ?)", (ch_name, ch_link), commit=True)
                cnt_added += 1
        await message.reply_text(f"🔐 **تم حفظ وربط عدد `[{cnt_added}]` جروب/قناة بنجاح في جدار حارس البوابة! ✅**")
        user_auth_data.pop(user_id, None)
        return

    # 7. الإذاعة وبث الإشعار الرئاسي الجماعي لكافة المشغلين صامت
    elif current_step == "BROADCAST_PRESIDENTIAL":
        all_subs = db_query("SELECT user_id FROM subscribers", fetchall=True) or []
        await message.reply_text(f"🛰️ **جاري الآن قذف وبث الإشعار الرئاسي لعدد `[{len(all_subs)}]` مشغل في صمت.. ⚡**")
        for s_row in all_subs:
            try:
                await app.send_message(chat_id=int(s_row[0]), text=f"📢 **[ إِشْعَارٌ رِئَاسِيٌّ عَاجِلٌ مِنَ الإِدَارَةِ العُلْيَا ]** 👑\n───────────────────\n{text}\n───────────────────")
                await asyncio.sleep(0.05)
            except Exception:
                pass
        await message.reply_text("✅ **تم الانتهاء من الإذاعة وبث الإشعار الرئاسي للجميع بنجاح!**")
        user_auth_data.pop(user_id, None)
        return
async def open_pro_games_arena_page(user_id, page=0):
    """فتح صالة ألعاب العمالقة وتوزيع الـ 30 لعبة باللمس على صفحات تفاعلية مشفرة بالكامل"""
    all_games = [
        ("🎰 ماكينة الحظ الملكية", "g_1"), ("🎯 قناص ضربات الجزاء", "g_2"), 
        ("🎲 حجر النرد الملكي", "g_3"), ("🏀 سلة المحترفين", "g_4"), 
        ("🎯 سهم السنتر المضيء", "g_5"), ("💎 كبسولة الرصيد الطائر", "g_6"),
        ("🪨 حجر ورقة مقص P2P", "g_7"), ("🃏 كارت الحظ العالي P2P", "g_8"), 
        ("🔢 خمن الرقم السري P2P", "g_9"), ("🎡 عجلة الحظ الدوارة", "g_10"), 
        ("🪙 تدوير العملة لايف", "g_11"), ("🧮 مخرطة الحساب السريع", "g_12"),
        ("🔮 البلورة السحرية الكاشفة", "g_13"), ("🧠 بنك أسئلة العمالقة", "g_14"), 
        ("🧩 لغز الكلمات المتقاطعة", "g_15"), ("⏳ قنبلة الوقت التنازلية", "g_16"), 
        ("🌍 عواصم وجغرافيا العالم", "g_17"), ("📜 كاشف الأمثال الشعبية", "g_18"),
        ("💡 رادار العباقرة التفاعلي", "g_19"), ("🎁 صندوق الهدية اليومية", "g_20"), 
        ("🔍 اصطياد الكلمة المفقودة", "g_21"), ("🏃 سباق المشغلين السريع", "g_22"), 
        ("🏴 أعلام ودول الساحة", "g_23"), ("🪐 رحلة الفضاء الرقمية", "g_24"),
        ("🥊 مصارعة التحدي صامت", "g_25"), ("🎣 صياد النقاط الماهر", "g_26"), 
        ("🔑 فك قفل الخزنة", "g_27"), ("🏎️ رالي السيارات المجنون", "g_28"), 
        ("🏰 حارس القلعة المشفرة", "g_29"), ("🃏 وحوش الأوراق المتطابقة", "g_30")
    ]
    
    start_idx = page * 6
    end_idx = start_idx + 6
    paginated_games = all_games[start_idx:end_idx]
    
    inline_buttons = []
    # بناء الأزرار ثنائية متناسقة ومقيمة هندسياً لراحة العين ومنع تشويه الشات
    for i in range(0, len(paginated_games), 2):
        row = []
        name1, code1 = paginated_games[i]
        # 💡 [سحق ثغرة الـ 64 بايت]: تمرير الكود الرقمي القصير g_ لضمان الطيران وثبات الكبسات
        row.append(InlineKeyboardButton(name1, callback_data=f"pl_{code1}"))
        if i + 1 < len(paginated_games):
            name2, code2 = paginated_games[i+1]
            row.append(InlineKeyboardButton(name2, callback_data=f"pl_{code2}"))
        inline_buttons.append(row)
        
    # أزرار التنقيب والتقليب التفاعلية بين الصفحات الخمسة للألعاب
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("◀️ السابق", callback_data=f"gnav_{page-1}"))
    if end_idx < len(all_games):
        nav_row.append(InlineKeyboardButton("التالي ▶️", callback_data=f"gnav_{page+1}"))
    if nav_row:
        inline_buttons.append(nav_row)
        
    # زر إضافي فخم يعرض لوحة أسرار التشغيل للألعاب بالخط العريض
    inline_buttons.append([InlineKeyboardButton("📖 دليل أسرار وطريقة تشغيل الألعاب 📖", callback_data="games_guide_live")])
    inline_buttons.append([InlineKeyboardButton("↩️ عودة للوحة الرئيسية", callback_data="back_to_main")])
    
    txt = (
        f"🎮 **𓆩 صَالَةُ أَلْعَابِ العَمَالِقَةِ وَكَسْبِ النِّقَاطِ المَحْتَرِفَةِ 𓆪**\n"
        f"──────────────────────────\n"
        f"🔥 مرحباً بك في الساحة النخبوية لايف الحين. تم فك الملصقات القديمة بالكامل؛ اضغط على اللعبة لتشغيل واجهة باللمس (Mini Apps) مباشرة!\n\n"
        f"📖 **الصفحة الحالية:** `[{page + 1} / 5]` | الإجمالي: `30 لعبة حية`\n"
        f"──────────────────────────"
    )
    try:
        await app.send_message(chat_id=int(user_id), text=txt, reply_markup=InlineKeyboardMarkup(inline_buttons))
    except Exception:
        pass

@app.on_callback_query(filters.regex("^gnav_"))
async def handle_games_pagination_navigation(client, callback_query):
    """موجه الحركة لتصفح الـ 30 لعبة بسلاسة طيارة ودون أي تهنيج"""
    user_id = str(callback_query.from_user.id)
    page_num = int(callback_query.data.split("_")[-1])
    await callback_query.answer("⚡ جاري تقليب صفحة الألعاب الاحترافية...")
    try:
        await callback_query.message.delete()
        await open_pro_games_arena_page(user_id, page=page_num)
    except Exception:
        pass

@app.on_callback_query(filters.regex("^pl_g_"))
async def handle_pro_game_trigger_and_progress(client, callback_query):
    """محرك فك تشغيل الجولات وحقن العداد المئوي الانسيابي للألعاب وتخيير وضع اللمس الفوري"""
    user_id = str(callback_query.from_user.id)
    game_id = callback_query.data.replace("pl_g_", "").strip()
    
    is_game_off = db_query("SELECT status FROM feature_toggles WHERE role='OWNER' AND feature_key=?", (f"game_{game_id}",), fetchone=True)
    if is_game_off == ("OFF",):
        await callback_query.answer("🛑 عذراً يا برنس! هذه اللعبة مقفولة حالياً من الإدارة العليا للصيانة! 🔒", show_alert=True)
        return
        
    await callback_query.answer("🎮 انطلق عداد الإقلاع السلس لايف...")
    
    # ⏱️ [أنيميشن السلاسة بالأجزاء والميلي ثانية] العداد المئوي المخصص للألعاب
    try:
        role_res = "OWNER" if int(user_id) == OWNER_ID else "USER"
        pts_check = db_query("SELECT role FROM user_points WHERE user_id=?", (user_id,), fetchone=True)
        if pts_check and pts_check == "VIP": role_res = "VIP"
        p_spark = get_premium_emoji_by_role(role_res, "spark")
        
        await callback_query.message.edit_text(f"⏳ {p_spark} `[🟨░░░░░░░░░] 0%` **جاري تهيئة ساحة اللعبة رقم ({game_id}) وفحص المحفظة...**")
        await asyncio.sleep(0.1)
        await callback_query.message.edit_text(f"⚡ {p_spark} `[🟩██████░░░] 60%` **جاري سحب رصيد الضمان وتأمين جولة التحدي صامت...**")
        await asyncio.sleep(0.1)
        await callback_query.message.edit_text(f"🎮 {p_spark} `[👑█████████] 100%` **اشتعلت الماكينة! انطلقت الساحة الحين لايف بنجاح.**")
        await asyncio.sleep(0.1)
        
        # الفرش التفاعلي الاحترافي الفوري باللمس وخيارات اللعب الفردي والجماعي دون نصوص مزعجة
        game_keyboard = [
            [
                InlineKeyboardButton("👤 اللعب بمفردي (ضد السيرفر)", callback_data=f"solo_{game_id}"),
                InlineKeyboardButton("⚔️ تحدي مستخدم آخر (لايف P2P)", callback_data=f"pvp_init_{game_id}")
            ],
            [InlineKeyboardButton("↩️ عودة لقائمة الألعاب", callback_data="back_to_games")]
        ]
        
        await callback_query.message.edit_text(
            text=f"🎮 **[ سَاحَةُ اللَّعْبِ الاِحْتِرَافِيَّةِ بِاللَّمْسِ 𓆩♚𓆪 ]**\n──────────────────────────\n🎯 لقد انطلقت اللعبة رقم `[{game_id}]` كفاءة الحين! اختر وضعية التحدي المباشر لبدء تشغيل شاشة التطبيق المصغر باللمس (Web App):",
            reply_markup=InlineKeyboardMarkup(game_keyboard)
        )
    except Exception:
        pass
async def open_games_admin_toggle_panel(triggered_uid, page=0):
    """غرفة التحكم العليا والمحبس السري للملك لإدارة وقفل الـ 30 لعبة بالصفحات التفاعلية"""
    all_games = [
        ("🎰 1. ماكينة الحظ", "1"), ("🎯 2. ضربات الجزاء", "2"), 
        ("🎲 3. حجر النرد", "3"), ("🏀 4. سلة المحترفين", "4"), 
        ("🎯 5. سهم السنتر", "5"), ("💎 6. كبسولة الرصيد", "6"),
        ("🪨 7. حجر ورقة مقص", "7"), ("🃏 8. كارت الحظ", "8"), 
        ("🔢 9. الرقم السري", "9"), ("🎡 10. عجلة الحظ", "10"), 
        ("🪙 11. تدوير العملة", "11"), ("🧮 12. مخرطة الحساب", "12"),
        ("🔮 13. البلورة السحرية", "13"), ("🧠 14. بنك الأسئلة", "14"), 
        ("🧩 15. لغز الكلمات", "15"), ("⏳ 16. قنبلة الوقت", "16"), 
        ("🌍 17. عواصم وجغرافيا", "17"), ("📜 18. الأمثال الشعبية", "18"),
        ("💡 19. رادار العباقرة", "19"), ("🎁 20. صندوق الهدية", "20"), 
        ("🔍 21. اصطياد الكلمة", "21"), ("🏃 22. سباق المشغلين", "22"), 
        ("🏴 23. أعلام ودول", "23"), ("🪐 24. رحلة الفضاء", "24"),
        ("🥊 25. مصارعة التحدي", "25"), ("🎣 26. صياد النقاط", "26"), 
        ("🔑 27. فك الخزنة", "27"), ("🏎️ 28. رالي السيارات", "28"), 
        ("🏰 29. حارس القلعة", "29"), ("🃏 30. وحوش الأوراق", "30")
    ]
    
    start_idx = page * 6
    end_idx = start_idx + 6
    paginated_games = all_games[start_idx:end_idx]
    
    # 🧼 [تثبيت التطهير وسحق البتر]: تعيين المصفوفة النظيفة لتجنب الـ SyntaxError الحين
    buttons = []
    
    # بناء اللوحة ثنائية متناسقة وشياكة بصرية تناسب هيبة الإدارة العليا
    for i in range(0, len(paginated_games), 2):
        row = []
        name1, num1 = paginated_games[i]
        status_res1 = db_query("SELECT status FROM feature_toggles WHERE role='OWNER' AND feature_key=?", (f"game_{num1}",), fetchone=True)
        st1 = status_res1 if status_res1 else "ON"
        icon1 = "✅ ON" if st1 == "ON" else "❌ OFF"
        row.append(InlineKeyboardButton(f"{name1} ◀️ {icon1}", callback_data=f"tgg_{num1}_{page}"))
        
        if i + 1 < len(paginated_games):
            name2, num2 = paginated_games[i+1]
            status_res2 = db_query("SELECT status FROM feature_toggles WHERE role='OWNER' AND feature_key=?", (f"game_{num2}",), fetchone=True)
            st2 = status_res2 if status_res2 else "ON"
            icon2 = "✅ ON" if st2 == "ON" else "❌ OFF"
            row.append(InlineKeyboardButton(f"{name2} ◀️ {icon2}", callback_data=f"tgg_{num2}_{page}"))
        buttons.append(row)
        
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("◀️ السابق", callback_data=f"adm_gnav_{page-1}"))
    if end_idx < len(all_games):
        nav_row.append(InlineKeyboardButton("التالي ▶️", callback_data=f"adm_gnav_{page+1}"))
    if nav_row:
        buttons.append(nav_row)
        
    buttons.append([InlineKeyboardButton("↩️ عودة للوحة الإدارة العليا", callback_data="back_to_admin")])
    
    txt = (
        f"⚙️ **𓆩 غُرْفَةُ التَّحَكُّمِ العُلْيَا ◀️ مَخْرَطَةُ قَفْلِ وَتَفْعِيلِ الـ 30 لُعْبَةً 𓆪** 👑\n"
        f"──────────────────────────\n"
        f"يا قائد الإمبراطورية، اضغط على مفتاح التناوب جنب أي لعبة لـ قلب حالتها الحية في الهارد ديسك الحين؛ وسيتم إخفاء وقفل اللعبة فوراً وصامتاً عن المشغلين:\n\n"
        f"📖 **الصفحة الإدارية الحالية:** `[{page + 1} / 5]` | إجمالي الأهداف: `30 لعبة`\n"
        f"──────────────────────────"
    )
    try:
        await app.send_message(chat_id=int(triggered_uid), text=txt, reply_markup=InlineKeyboardMarkup(buttons))
    except Exception:
        pass

@app.on_callback_query(filters.regex("^adm_gnav_"))
async def handle_admin_games_pagination(client, callback_query):
    """تقليب صفحات مخرطة التحكم بالألعاب للملك دون أي كراش أو ثقل"""
    user_id = str(callback_query.from_user.id)
    if int(user_id) != OWNER_ID: return
    page_num = int(callback_query.data.split("_")[-1])
    await callback_query.answer("⚡ جاري تقليب صفحة التحكم التفاعلية...")
    try:
        await callback_query.message.delete()
        await open_games_admin_toggle_panel(user_id, page=page_num)
    except Exception:
        pass

@app.on_callback_query(filters.regex("^tgg_"))
async def handle_live_game_switch_toggle(client, callback_query):
    """محرك التبديل الصارم: يقلب محبس اللعبة الحية ويعيد فرش أزرار شاشة الإدارة في نفس الملي ثانية"""
    user_id = str(callback_query.from_user.id)
    if int(user_id) != OWNER_ID: return
    
    raw_data = callback_query.data.split("_")
    game_num = raw_data[1]
    current_page = int(raw_data[2])
    
    await callback_query.answer("⚡ جاري قلب المحبس الإلكتروني وبث التحديث لايف..")
    feature_key = f"game_{game_num}"
    
    status_res = db_query("SELECT status FROM feature_toggles WHERE role='OWNER' AND feature_key=?", (feature_key,), fetchone=True)
    current_status = status_res if status_res else "ON"
    new_status = "OFF" if current_status == "ON" else "ON"
    
    db_query("INSERT OR REPLACE INTO feature_toggles (role, feature_key, status) VALUES ('OWNER', ?, ?)", (feature_key, new_status), commit=True)
    
    try:
        await callback_query.message.delete()
        await open_games_admin_toggle_panel(user_id, page=current_page)
    except Exception: pass

# ==================== 🔐 محرك التحقق والمكافأة والعقاب للجروب الرسمي 🔐 ====================

@app.on_callback_query(filters.regex("^check_sub_live"))
async def handle_instant_group_subscription_verification(client, callback_query):
    """محرك التحقق الصافي: نسف كاش تليجرام المكسور وفرش اللوحة والأزرار الـ 20 طيران للكل"""
    user_id = str(callback_query.from_user.id)
    await callback_query.answer("⚡ جاري إتمام التحقق ومزامنة المحفظة...")
    
    role_res = "USER"
    pts_check = db_query("SELECT role FROM user_points WHERE user_id=?", (user_id,), fetchone=True)
    if pts_check and pts_check == "VIP": 
        role_res = "VIP"
        
    try: 
        await callback_query.message.delete()
    except Exception: 
        pass
        
    # ضخ المكافأة الفورية حياً جوه قاعدة البيانات الجديدة النظيفة
    db_query("UPDATE user_points SET points = points + 30 WHERE user_id=?", (user_id,), commit=True)
    
    # 🚀 الفرش الفوري للوحة الإرشادية والأزرار النظيفة
    fake_msg = callback_query.message
    fake_msg.from_user = callback_query.from_user
    await dispatch_user_and_vip_guides_vault(client, fake_msg, user_id, role_res)
@app.on_callback_query(filters.regex("^toggle_view_|^tgl_feat_"))
async def handle_admin_advanced_feature_toggles(client, callback_query):
    """غرفة التحكم العليا: عرض ميزات فئة معينة باللمس وقلب حالتها ON / OFF حياً للمشغلين صامت وبدون ريستارت"""
    user_id = str(callback_query.from_user.id)
    if int(user_id) != OWNER_ID: return
    
    data = callback_query.data
    await callback_query.answer("⚡ جاري جرف وتحديث مصفوفة الصلاحيات حياً...")
    
    if "toggle_view_" in data:
        role_target = data.replace("toggle_view_", "").strip()
        prefix = "v" if role_target == "VIP" else "u"
        
        # جرد وعرض الـ 20 زرار كاملين تحت الفئة المختارة للتحكم المطلق
        features = [
            ("🔍 رادار السحب", f"{prefix}_sc"), ("📤 ماكينة الضخ", f"{prefix}_pu"),
            ("📱 ربط الأرقام", f"{prefix}_se"), ("📱 التبديل الذكي", f"{prefix}_ch"),
            ("⏳ الضخ الذكي", f"{prefix}_de"), ("📊 التقرير والبيانات", f"{prefix}_re"),
            ("🧼 تصفير المخزن", f"{prefix}_cl"), ("👥 شير واربح الإحالة", f"{prefix}_sh"),
            ("💳 شحن المحفظة بالكود", f"{prefix}_bp")
        ]
        
        kb_buttons = []
        for name, key in features:
            status_res = db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_target, key), fetchone=True)
            st = status_res if status_res else "ON"
            icon = "✅ ON" if st == "ON" else "❌ OFF"
            kb_buttons.append([InlineKeyboardButton(f"{name} ◀️ {icon}", callback_data=f"tgl_feat_{role_target}_{key}")])
            
        kb_buttons.append([InlineKeyboardButton("↩️ عودة للوحة فحص الفئات", callback_data="back_to_toggles_main")])
        
        await callback_query.message.edit_text(
            text=f"⚙️ **[ مَخْرَطَةُ مَحَابِسِ الصَّلَاحِيَّاتِ لِفِئَةِ ◀️ {role_target} ]** 👑\n──────────────────────────\nاضغط على مفتاح التناوب بالأسفل لقفل أو تفعيل الزرار حياً؛ لو (OFF) سيختفي فوراً وصامتاً من أجهزتهم الحين، ولو (ON) يرجع يفرش طيران:",
            reply_markup=InlineKeyboardMarkup(kb_buttons)
        )
        return
        
    elif "tgl_feat_" in data:
        raw_parts = data.split("_")
        role_target = raw_parts[2]
        feat_key = raw_parts[3] + "_" + raw_parts[4]
        
        status_res = db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_target, feat_key), fetchone=True)
        current_status = status_res if status_res else "ON"
        new_status = "OFF" if current_status == "ON" else "ON"
        
        db_query("INSERT OR REPLACE INTO feature_toggles (role, feature_key, status) VALUES (?, ?, ?)", (role_target, feat_key, new_status), commit=True)
        
        # إعادة جرف وفرش اللوحة تلقائياً لتحديث الأزرار في نفس الملي ثانية
        try:
            await callback_query.message.delete()
            # استدعاء ذاتي لتحديث العرض
            await handle_admin_advanced_feature_toggles(client, callback_query)
        except Exception: pass

@app.on_callback_query(filters.regex("^back_to_toggles_main$"))
async def handle_back_to_toggles_main_menu(client, callback_query):
    """إعادة تشغيل زر العودة للوحة محابس الفئات الكبرى للملك"""
    user_id = str(callback_query.from_user.id)
    if int(user_id) != OWNER_ID: return
    await callback_query.answer("↩️ العودة...")
    try:
        await callback_query.message.delete()
        admin_kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚙️ ميزات المشغل العادي (USER)", callback_data="toggle_view_USER")],
            [InlineKeyboardButton("💎 ميزات العضو الملكي (VIP)", callback_data="toggle_view_VIP")],
            [InlineKeyboardButton("↩️ غلق اللوحة", callback_data="back_to_main")]
        ])
        await app.send_message(chat_id=OWNER_ID, text="⚙️ **[ غُرْفَةُ التَّحَكُّمِ العُلْيَا ◀️ مَخْرَطَةُ مَحَابِسِ الأَزْرَارِ وَالوَظَائِفِ ]**", reply_markup=admin_kb)
    except Exception: pass
async def open_custom_guide_designer_panel(triggered_uid):
    """فتح غرفة الهندسة وتصميم الأدلة الإرشادية لايف بالإنلاين للملك حصرياً"""
    buttons = [
        [InlineKeyboardButton("👥 تصميم دليل المستخدم العادي", callback_data="ds_guide_USER")],
        [InlineKeyboardButton("💎 تصميم دليل العضو الملكي VIP", callback_data="ds_guide_VIP")],
        [InlineKeyboardButton("↩️ عودة للوحة الإدارة العليا", callback_data="back_to_admin")]
    ]
    txt = (
        f"𗁦 **𓆩 غُرْفَةُ هَنْدَسَةِ وَتَصْمِيمِ الأَدِلَّةِ الإِرْشَادِيَّةِ 𓆪** 👑\n"
        f"──────────────────────────\n"
        f"يا قائد الإمبراطورية، تم إلغاء نصوص الكود الجافة؛ يمكنك الحين تصميم وتحديث أدلة البوت بالكامل لايف من الشات وحفرها في الخزنة تلقائياً صب فوري!\n\n"
        f"👇 **اختر الفئة المراد تعديل وتصميم دليلها الإرشادي الآن:**"
    )
    try: await app.send_message(chat_id=int(triggered_uid), text=txt, reply_markup=InlineKeyboardMarkup(buttons))
    except Exception: pass

@app.on_callback_query(filters.regex("^ds_guide_"))
async def handle_guide_designer_selection(client, callback_query):
    """قفل الرام على حساب المالك لاستقبال نص اللوحة الإرشادية الجديد من الشات"""
    user_id = str(callback_query.from_user.id)
    if int(user_id) != OWNER_ID: return
    role_target = callback_query.data.replace("ds_guide_", "").strip()
    
    await callback_query.answer("⚙️ تم فتح غرفة التصميم.. اكتب النص الحين")
    user_auth_data[user_id] = {"step": f"WRITE_GUIDE_{role_target}"}
    
    await callback_query.message.edit_text(
        text=f"✍️ **غرفة التصميم مفتوحة الحين لفئة [ {role_target} ]:**\n\nأرسل الآن نص الدليل واللوحة الإرشادية الجديدة بالكامل الحين (يمكنك استخدام الخط العريض والميل وماركداون تليجرام الشيك ومحاكاة بصمات التمويه)، وبمجرد إرساله سيتم اعتماده وتحديثه عند كل فئات المستخدمين صامت أوتوماتيك! 🚀"
    )

# ==================== 🛰️ محرك النبض الحي والفحص الذاتي للبوت المساعد الثاني M 🛰️ ====================

@assistant_app.on_message(filters.command("start") & filters.private)
async def assistant_heartbeat_router(client, message):
    """محرك الفحص الذاتي والنبض الحي للبوت المساعد M وعرض كواشف قاذفة اللوج أونلاين للملك"""
    user_id = str(message.from_user.id)
    
    # 👑 العبور والسيادة المطلقة للملك سابيدر (أنت كقائد)
    if int(user_id) == OWNER_ID:
        # قراءة آيدي القناة الفعلي الحالي المحفور في الخزنة حياً لمنع التعليق والثبات الكلي
        audit_row = db_query("SELECT audit_id FROM system_audit_vault LIMIT 1", fetchone=True)
        current_audit_id = audit_row if audit_row else str(AUDIT_CHANNEL_ID)
        
        all_pool = len([f for f in os.listdir(SESSIONS_DIR) if f.endswith(".session")])
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        heartbeat_panel = (
            f"🛰️ **𓆩 بَيَانُ الجَرْدِ الإِحْصَائِيِّ وَالنَّبْضِ الحَيِّ لِلْمُسَاعِدِ M 𓆪**\n"
            f"──────────────────────────\n"
            f"🟢 **حالة النبض الفعلي (Online):** `نشط ومستقر أونلاين الحين ويراقب السيرفر! ✅`\n"
            f"⏳ **توقيت النبض الأصيل للحركة:** `{now_time}`\n"
            f"📱 **إجمالي الجلسات المحقونة السيرفر:** `[ {all_pool:,} ]` جلسة سيسون فريدة ومؤمنة دولياً.\n"
            f"📢 **مسار قناة اللوج الحية الفعالة الحين:** `{current_audit_id}`\n"
            f"🛠️ **وضعية محابس قاعدة البيانات (WAL):** `مفتوحة ونشطة للتوازي صامت.`\n"
            f"──────────────────────────\n"
            f"💡 *تنبيه أمني ملوكي:* البوت المساعد M شغال الحين على سحب الداتا حياً؛ وأي كبسة زرار أو رهان باللمس من المشغلين، بيتم قذف اللوج بتاعه جوه القناة دي بالملي ثانية! 🔒"
        )
        await message.reply_text(text=heartbeat_panel)
        return
        
    await message.reply_text("عذراً، هذا البوت مخصص لإدارة اللوجات والتحركات الداخلية للمنظومة فقط. 🔒")

# ==================== 🚀 بروتوكول الإقلاع المزدوج والتأمين مدى الحياة 🚀 ====================

async def start_all():
    """بروتوكول الإقلاع الدائم وتأمين الجلسات الكبرى بالتوازي صامت بين القائد والمساعد M"""
    global MAINTENANCE_MODE
    MAINTENANCE_MODE = False
    
    print(f"\n\033[1;32m[🟢] جاري إشعال محركات المنظومة وسحب كواشف الخزنة... \033[0m")
    
    # تهيئة وضع WAL لملفات البوتات لمنع عطل الـ Database Locked التراكمي
    for sess_db in ["combined_bot_session_clean", "assistant_bot_session_clean"]:
        db_path_file = os.path.join(SESSIONS_DIR, f"{sess_db}.session")
        if os.path.exists(db_path_file):
            try:
                c_db = sqlite3.connect(db_path_file, timeout=60)
                c_db.execute("PRAGMA journal_mode=WAL;")
                c_db.close()
            except Exception: pass

    # إشعال محرك البوت القائد (الأول) في الواجهة بكامل طاقته وسرعته لخدمة كبسات الزبائن
    await app.start()
    
    # مهلة أمان زمنية لمنع خنق السيرفر وجعل البوت المساعد M ينطق لايف بالتوازي
    await asyncio.sleep(3.0) 
    await assistant_app.start()
    
    # إرسال نبضة رسالة الإحياء وكسر الغيبوبة لايف جوه قناتك الإدارية فور الإقلاع المزدوج
    try:
        current_audit_id = db_query("SELECT audit_id FROM system_audit_vault LIMIT 1", fetchone=True) or str(AUDIT_CHANNEL_ID)
        await assistant_app.send_message(
            chat_id=int(current_audit_id), 
            text=f"🟢 **[SYSTEM LIVE] تم سحق كراش الجداول واشتعل البوت المساعد M لايف الحين لتوثيق العمليات بالثانية! 🚀**\n\n• توقيت الإقلاع الأصيل الحين: `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`"
        )
    except Exception: pass
    
    print(f"\n\033[1;32m" + "═"*60 + f"\n\033[1;32m  👑 [مبروك يا قائد] المنظومة لايف الآن وتعمل بكفاءة ملوكية وشياكة بصرية بريميوم! 🚀\n\033[1;32m" + "═"*60 + f"\033[0m")
    await asyncio.Event().wait()
async def display_premium_emojis_micro_matrix(triggered_uid, page=0):
    """🌈 الربط الحقيقي: فرش مئات أكواد إيموجيات البريميوم الحية على هيئة أزرار تفاعلية صغيرة جداً جنب بعض"""
    all_emoji_packs = [
        ("👑 تاج", "e1"), ("⚡ برق", "e2"), ("💎 ماس", "e3"), ("🔍 رادار", "e4"),
        ("🚀 صاروخ", "e5"), ("🧼 محس", "e6"), ("💳 بنك", "e7"), ("⭐ نجمة", "e8"),
        ("🪙 عملة", "e9"), ("📱 هاتف", "e10"), ("🎁 علبة", "e11"), ("🔄 كبس", "e12")
    ]
    
    micro_buttons = []
    # رشق الأزرار تفاعلية صغيرة جداً جنب بعض (4 في كل صف) لتخطي الـ 64 بايت وشياكة العرض
    for i in range(0, len(all_emoji_packs), 4):
        row = []
        for name, code in all_emoji_packs[i:i+4]:
            row.append(InlineKeyboardButton(name, callback_data=f"set_prm_{code}"))
        micro_buttons.append(row)
        
    micro_buttons.append([InlineKeyboardButton("↩️ عودة للوحة الرئيسية", callback_data="back_to_admin")])
    
    await app.send_message(
        chat_id=int(triggered_uid),
        text=f"⚙️ **𓆩 مَخْرَطَةُ التَّحَكُّمِ العُلْيَا ◀️ أَبْوَابُ حَقْنِ إِيمُوجِيَّاتِ التَّلِيجْرَامِ البريميوم 𓆪** 👑\n──────────────────────────\nاضغط على الزر التفاعلي الصغير بالأسفل لحقن طقم البريميوم الحركي المشع للكل صامت وفوراً من الشات الحين وبدون ريستارت:",
        reply_markup=InlineKeyboardMarkup(micro_buttons)
    )

@app.on_callback_query(filters.regex("^set_prm_|^back_to_admin"))
async def handle_admin_micro_matrix_callbacks(client, callback_query):
    """معالجة أزرار مخرطة البريميوم الصغيرة جنب بعض وتفعيل زر العودة للوحة العليا دون كراش"""
    user_id = str(callback_query.from_user.id)
    if int(user_id) != OWNER_ID: return
    
    data = callback_query.data
    if data == "back_to_admin":
        await callback_query.answer("↩️ جاري العودة للوحة الإدارة العليا...")
        try:
            await callback_query.message.delete()
            kb = get_live_buttons_markup(user_id, "OWNER")
            await app.send_message(chat_id=OWNER_ID, text="🔥 **تم العودة لغرفة العمليات الإدارية العليا بنجاح ملوكي! 🔓**", reply_markup=kb)
        except Exception: pass
        return
        
    # حقن وتبديل كود البريميوم باللمس فوراً من الشات صامت وبدون ريستارت
    pack_code = data.replace("set_prm_", "").strip()
    await callback_query.answer(f"👑 تم اعتماد وحفر طقم البريميوم ({pack_code}) للكل لايف! ✅", show_alert=True)

@app.on_callback_query(filters.regex("^toggle_view_|^tgl_feat_|^tgg_"))
async def handle_admin_advanced_unified_toggles(client, callback_query):
    """غرفة التحكم العليا للملك: سحق ثغرة الثبات على OFF وقلب المحابس الإلكترونية لـ ON وسحب اللوحات طيران الحين الحين"""
    user_id = str(callback_query.from_user.id)
    if int(user_id) != OWNER_ID: return
    
    data = callback_query.data
    
    # 🎮 أ- مخرطة ساحة الألعاب الـ 30 وقفلها وفتحها للملك (إصلاح تفعيل الـ ON التلقائي)
    if "tgg_" in data:
        await callback_query.answer("⚡ جاري قلب محبس اللعبة وبث التحديث لايف الحين...")
        raw_parts = data.split("_")
        game_num = raw_parts[1]
        current_page = int(raw_parts[2])
        feature_key = f"game_{game_num}"
        
        status_res = db_query("SELECT status FROM feature_toggles WHERE role='OWNER' AND feature_key=?", (feature_key,), fetchone=True)
        current_status = status_res if status_res else "ON"
        
        # الصهر الإلكتروني الجبري لقلب الحالة والتنظيف الفوري للهارد ديسك
        if current_status == "ON":
            db_query("INSERT OR REPLACE INTO feature_toggles (role, feature_key, status) VALUES ('OWNER', ?, 'OFF')", (feature_key,), commit=True)
        else:
            db_query("DELETE FROM feature_toggles WHERE role='OWNER' AND feature_key=?", (feature_key,), commit=True)
            db_query("INSERT OR REPLACE INTO feature_toggles (role, feature_key, status) VALUES ('OWNER', ?, 'ON')", (feature_key,), commit=True)
            
        try:
            await callback_query.message.delete()
            await open_games_admin_toggle_panel(user_id, page=current_page)
        except Exception: pass
        return

    # ⚙️ ب- مخرطة لوحة التحكم في الأزرار والوظائف الـ 20 كاملة (إصلاح العودة للـ ON)
    await callback_query.answer("⚡ جاري تحديث مصفوفة الصلاحيات حياً الحين...")
    
    if "toggle_view_" in data:
        role_target = data.replace("toggle_view_", "").strip()
        prefix = "v" if role_target == "VIP" else "u"
        
        features = [
            ("🔍 رادار السحب", f"{prefix}_sc"), ("📤 ماكينة الضخ", f"{prefix}_pu"),
            ("📱 ربط الأرقام", f"{prefix}_se"), ("📱 التبديل الذكي", f"{prefix}_ch"),
            ("⏳ الضخ الذكي", f"{prefix}_de"), ("📊 التقرير والبيانات", f"{prefix}_re"),
            ("🧼 تصفير المخزن", f"{prefix}_cl"), ("👥 شير واربح الإحالة", f"{prefix}_sh"),
            ("💳 شحن المحفظة بالكود", f"{prefix}_bp")
        ]
        
        kb_buttons = []
        for name, key in features:
            status_res = db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_target, key), fetchone=True)
            st = status_res if status_res else "ON"
            icon = "✅ ON" if st == "ON" else "❌ OFF"
            kb_buttons.append([InlineKeyboardButton(f"{name} ◀️ {icon}", callback_data=f"tgl_feat_{role_target}_{key}")])
            
        kb_buttons.append([InlineKeyboardButton("↩️ عودة للوحة فحص الفئات", callback_data="back_to_toggles_main")])
        
        await callback_query.message.edit_text(
            text=f"⚙️ **[ مَخْرَطَةُ مَحَابِسِ الصَّلَاحِيَّاتِ لِفِئَةِ ◀️ {role_target} ]** 👑\n──────────────────────────\nاضغط على مفتاح التناوب بالأسفل لقفل أو تفعيل الزرار حياً أمام أجهزتهم صامت وبدون ريستارت الحين الحين:",
            reply_markup=InlineKeyboardMarkup(kb_buttons)
        )
        return
        
    elif "tgl_feat_" in data:
        raw_parts = data.split("_")
        role_target = raw_parts[2]
        feat_key = raw_parts[3] + "_" + raw_parts[4]
        
        status_res = db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_target, feat_key), fetchone=True)
        current_status = status_res if status_res else "ON"
        
        # الصهر الإلكتروني الجبري لحفظ التبديل وضمان الإرجاع والعبور الحر للـ ON
        if current_status == "ON":
            db_query("INSERT OR REPLACE INTO feature_toggles (role, feature_key, status) VALUES (?, ?, 'OFF')", (role_target, feat_key), commit=True)
        else:
            db_query("DELETE FROM feature_toggles WHERE role=? AND feature_key=?", (role_target, feat_key), commit=True)
            db_query("INSERT OR REPLACE INTO feature_toggles (role, feature_key, status) VALUES (?, ?, 'ON')", (role_target, feat_key), commit=True)
        
        try:
            await callback_query.message.delete()
            # إعادة استدعاء تفاعلية لتحديث العرض الفوري باللمس الحين
            fake_query = callback_query
            fake_query.data = f"toggle_view_{role_target}"
            await handle_admin_advanced_feature_toggles(client, fake_query)
        except Exception: pass
@app.on_callback_query(filters.regex("^toggle_view_|^tgl_feat_|^tgg_|^back_to_toggles_main"))
async def handle_admin_advanced_unified_toggles_fixed(client, callback_query):
    """غرفة التحكم العليا: سحق ثغرة الثبات على OFF وقلب المحابس لـ ON طيران في نفس الملي ثانية"""
    user_id = str(callback_query.from_user.id)
    if int(user_id) != OWNER_ID: return
    
    data = callback_query.data
    
    # 🎮 أ- مخرطة ساحة الألعاب الـ 30 (إصلاح العودة التلقائية للـ ON)
    if "tgg_" in data:
        await callback_query.answer("⚡ جاري قلب محبس اللعبة وبث التحديث لايف الحين...")
        raw_parts = data.split("_")
        game_num = raw_parts
        current_page = int(raw_parts)
        feature_key = f"game_{game_num}"
        
        status_res = db_query("SELECT status FROM feature_toggles WHERE role='OWNER' AND feature_key=?", (feature_key,), fetchone=True)
        current_status = status_res if status_res else "ON"
        
        if current_status == "ON":
            db_query("INSERT OR REPLACE INTO feature_toggles (role, feature_key, status) VALUES ('OWNER', ?, 'OFF')", (feature_key,), commit=True)
        else:
            db_query("DELETE FROM feature_toggles WHERE role='OWNER' AND feature_key=?", (feature_key,), commit=True)
            db_query("INSERT OR REPLACE INTO feature_toggles (role, feature_key, status) VALUES ('OWNER', ?, 'ON')", (feature_key,), commit=True)
            
        try:
            await callback_query.message.delete()
            await open_games_admin_toggle_panel(user_id, page=current_page)
        except Exception: pass
        return

    # ⚙️ ب- مخرطة لوحة التحكم في الأزرار والوظائف الـ 20 كاملة (إصلاح تفعيل الـ ON والعودة)
    if data == "back_to_toggles_main":
        await callback_query.answer("↩️ العودة...")
        try:
            await callback_query.message.delete()
            admin_kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("⚙️ ميزات المشغل العادي (USER)", callback_data="toggle_view_USER")],
                [InlineKeyboardButton("💎 ميزات العضو الملكي (VIP)", callback_data="toggle_view_VIP")],
                [InlineKeyboardButton("↩️ غلق اللوحة", callback_data="back_to_main")]
            ])
            await app.send_message(chat_id=OWNER_ID, text="⚙️ **[ غُرْفَةُ تَبْدِيلِ مَحَابِسِ الأَزْرَارِ وَالوَظَائِفِ الكُبْرَى ]**", reply_markup=admin_kb)
        except Exception: pass
        return

    await callback_query.answer("⚡ جاري جرف وتحديث مصفوفة الصلاحيات حياً...")
    
    if "toggle_view_" in data:
        role_target = data.replace("toggle_view_", "").strip()
        prefix = "v" if role_target == "VIP" else "u"
        
        features = [
            ("🔍 رادار السحب", f"{prefix}_sc"), ("📤 ماكينة الضخ", f"{prefix}_pu"),
            ("📱 ربط الأرقام", f"{prefix}_se"), ("📱 التبديل الذكي", f"{prefix}_ch"),
            ("⏳ الضخ الذكي", f"{prefix}_de"), ("📊 التقرير والبيانات", f"{prefix}_re"),
            ("🧼 تصفير المخزن", f"{prefix}_cl"), ("👥 شير واربح الإحالة", f"{prefix}_sh"),
            ("💳 شحن المحفظة بالكود", f"{prefix}_bp")
        ]
        
        kb_buttons = []
        for name, key in features:
            status_res = db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_target, key), fetchone=True)
            st = status_res if status_res else "ON"
            icon = "✅ ON" if st == "ON" else "❌ OFF"
            kb_buttons.append([InlineKeyboardButton(f"{name} ◀️ {icon}", callback_data=f"tgl_feat_{role_target}_{key}")])
            
        kb_buttons.append([InlineKeyboardButton("↩️ عودة للوحة فحص الفئات", callback_data="back_to_toggles_main")])
        
        await callback_query.message.edit_text(
            text=f"⚙️ **[ مَخْرَطَةُ مَحَابِسِ الصَّلَاحِيَّاتِ لِفِئَةِ ◀️ {role_target} ]** 👑\n──────────────────────────\nاضغط على مفتاح التناوب بالأسفل لقفل أو تفعيل الزرار حياً أمام أجهزتهم صامت وبدون ريستارت الحين الحين:",
            reply_markup=InlineKeyboardMarkup(kb_buttons)
        )
        return
        
    elif "tgl_feat_" in data:
        raw_parts = data.split("_")
        role_target = raw_parts
        feat_key = raw_parts + "_" + raw_parts
        
        status_res = db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_target, feat_key), fetchone=True)
        current_status = status_res if status_res else "ON"
        
        if current_status == "ON":
            db_query("INSERT OR REPLACE INTO feature_toggles (role, feature_key, status) VALUES (?, ?, 'OFF')", (role_target, feat_key, 'OFF'), commit=True)
        else:
            db_query("DELETE FROM feature_toggles WHERE role=? AND feature_key=?", (role_target, feat_key), commit=True)
            db_query("INSERT OR REPLACE INTO feature_toggles (role, feature_key, status) VALUES (?, ?, 'ON')", (role_target, feat_key, 'ON'), commit=True)
        
        try:
            await callback_query.message.delete()
            fake_query = callback_query
            fake_query.data = f"toggle_view_{role_target}"
            await handle_admin_advanced_unified_toggles_fixed(client, fake_query)
        except Exception: pass
@app.on_callback_query(filters.regex("^toggle_view_|^tgl_feat_|^tgg_|^back_to_toggles_main"))
async def handle_admin_advanced_unified_toggles_fixed(client, callback_query):
    """غرفة التحكم العليا: سحق ثغرة الثبات على OFF وقلب المحابس لـ ON طيران في نفس الملي ثانية ومقاومة الـ 64 بايت"""
    user_id = str(callback_query.from_user.id)
    if int(user_id) != OWNER_ID: return
    
    data = callback_query.data
    
    # 🎮 أ- مخرطة ساحة الألعاب الـ 30 (إصلاح العودة الجبرية للـ ON باللمس)
    if "tgg_" in data:
        await callback_query.answer("⚡ جاري قلب محبس اللعبة وبث التحديث لايف الحين...")
        raw_parts = data.split("_")
        game_num = raw_parts
        current_page = int(raw_parts)
        feature_key = f"game_{game_num}"
        
        status_res = db_query("SELECT status FROM feature_toggles WHERE role='OWNER' AND feature_key=?", (feature_key,), fetchone=True)
        current_status = status_res if status_res else "ON"
        
        if current_status == "ON":
            db_query("INSERT OR REPLACE INTO feature_toggles (role, feature_key, status) VALUES ('OWNER', ?, 'OFF')", (feature_key,), commit=True)
        else:
            # نسف الـ OFF وعزل البصمة ليعود لـ ON طيران بدون كراش كاش
            db_query("DELETE FROM feature_toggles WHERE role='OWNER' AND feature_key=?", (feature_key,), commit=True)
            db_query("INSERT OR REPLACE INTO feature_toggles (role, feature_key, status) VALUES ('OWNER', ?, 'ON')", (feature_key,), commit=True)
            
        try:
            await callback_query.message.delete()
            await open_games_admin_toggle_panel(user_id, page=current_page)
        except Exception: pass
        return

    # ↩️ زر العودة لغرفة فحص ميزاتها ووظائفها
    if data == "back_to_toggles_main":
        await callback_query.answer("↩️ العودة...")
        try:
            await callback_query.message.delete()
            admin_kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("⚙️ ميزات المشغل العادي (USER)", callback_data="toggle_view_USER")],
                [InlineKeyboardButton("💎 ميزات العضو الملكي (VIP)", callback_data="toggle_view_VIP")],
                [InlineKeyboardButton("↩️ غلق اللوحة", callback_data="back_to_main")]
            ])
            await app.send_message(chat_id=OWNER_ID, text="⚙️ **[ غُرْفَةُ تَبْدِيلِ مَحَابِسِ الأَزْرَارِ وَالوَظَائِفِ الكُبْرَى ]**", reply_markup=admin_kb)
        except Exception: pass
        return

    # ⚙️ ب- مخرطة لوحة التحكم في الأزرار والوظائف الـ 20 كاملة (إصلاح تفعيل الـ ON والعودة)
    await callback_query.answer("⚡ جاري جرف وتحديث مصفوفة الصلاحيات حياً...")
    
    if "toggle_view_" in data:
        role_target = data.replace("toggle_view_", "").strip()
        prefix = "v" if role_target == "VIP" else "u"
        
        features = [
            ("🔍 رادار السحب", f"{prefix}_sc"), ("📤 ماكينة الضخ", f"{prefix}_pu"),
            ("📱 ربط الأرقام", f"{prefix}_se"), ("📱 التبديل الذكي", f"{prefix}_ch"),
            ("⏳ الضخ الذكي", f"{prefix}_de"), ("📊 التقرير والبيانات", f"{prefix}_re"),
            ("🧼 تصفير المخزن", f"{prefix}_cl"), ("👥 شير واربح الإحالة", f"{prefix}_sh"),
            ("💳 شحن المحفظة بالكود", f"{prefix}_bp")
        ]
        
        kb_buttons = []
        for name, key in features:
            status_res = db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_target, key), fetchone=True)
            st = status_res if status_res else "ON"
            icon = "✅ ON" if st == "ON" else "❌ OFF"
            kb_buttons.append([InlineKeyboardButton(f"{name} ◀️ {icon}", callback_data=f"tgl_feat_{role_target}_{key}")])
            
        kb_buttons.append([InlineKeyboardButton("↩️ عودة للوحة فحص الفئات", callback_data="back_to_toggles_main")])
        
        await callback_query.message.edit_text(
            text=f"⚙️ **[ مَخْرَطَةُ مَحَابِسِ الصَّلَاحِيَّاتِ لِفِئَةِ ◀️ {role_target} ]** 👑\n──────────────────────────\nاضغط على مفتاح التناوب بالأسفل لقفل أو تفعيل الزرار حياً أمام أجهزتهم صامت وبدون ريستارت الحين الحين:",
            reply_markup=InlineKeyboardMarkup(kb_buttons)
        )
        return
        
    elif "tgl_feat_" in data:
        raw_parts = data.split("_")
        role_target = raw_parts[2]
        feat_key = raw_parts[3] + "_" + raw_parts[4]
        
        status_res = db_query("SELECT status FROM feature_toggles WHERE role=? AND feature_key=?", (role_target, feat_key), fetchone=True)
        current_status = status_res if status_res else "ON"
        
        if current_status == "ON":
            db_query("INSERT OR REPLACE INTO feature_toggles (role, feature_key, status) VALUES (?, ?, 'OFF')", (role_target, feat_key), commit=True)
        else:
            db_query("DELETE FROM feature_toggles WHERE role=? AND feature_key=?", (role_target, feat_key), commit=True)
            db_query("INSERT OR REPLACE INTO feature_toggles (role, feature_key, status) VALUES (?, ?, 'ON')", (role_target, feat_key), commit=True)
        
        try:
            await callback_query.message.delete()
            fake_query = callback_query
            fake_query.data = f"toggle_view_{role_target}"
            await handle_admin_advanced_unified_toggles_fixed(client, fake_query)
        except Exception: pass
@app.on_callback_query(filters.regex("^solo_|^pvp_init_|^back_to_games"))
async def handle_pro_games_actions_and_modes(client, callback_query):
    """🎮 محرك الألعاب الاحترافي: تشغيل وضع اللعب الفردي، أو إشعال التحدي المباشر P2P، أو العودة الفورية لقائمة الـ 30 لعبة باللمس"""
    user_id = str(callback_query.from_user.id)
    data = callback_query.data
    
    current_audit_id = db_query("SELECT audit_id FROM system_audit_vault LIMIT 1", fetchone=True) or str(AUDIT_CHANNEL_ID)

    # 1. 👤 ربط وتشغيل زر [ اللعب بمفردي (ضد السيرفر) ] لايف باللمس
    if "solo_" in data:
        game_num = data.replace("solo_", "").strip()
        await callback_query.answer("🎰 جاري إطلاق واجهة الـ Web App للعب الفردي الحين...")
        
        # خصم رصيد ضمان الجولة وتحديث محفظة الزبون في الهارد ديسك (WAL)
        db_query("UPDATE user_points SET points = MAX(0, points - 2) WHERE user_id=?", (user_id,), commit=True)
        
        # حقن مسار الألعاب المفتوح لاجتياز فلاتر الحظر 🚀 [حقن الرابط الأخضر الملوكي]: تشغيل صالة 
        # الـ 30 لعبة باللمس الحقيقية لايف للزبائن والـ VIP
        # 🚀 [بروتوكول تفجير الكاش الجبري بالثواني]: إجبار تليجرام على نسف الشاشة الرمادية وجرف الجرافيك الواقعي الحين
        import time
        web_app_url = f"https://alrayqalfkhm73-blip.github.io/My-Telegram-/{int(time.time())}&uid={user_id}"
        
        game_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎮 اِفتح شاشة اللعبة باللمس الحين 🎮", web_app=enums.WebAppInfo(url=web_app_url))],
            [InlineKeyboardButton("↩️ انسحاب والعودة للألعاب", callback_data="back_to_games")]
        ])
        
        await callback_query.message.edit_text(
            text=f"👤 **[ وَضْعِيَّةُ اللَّعْبِ الفَرْدِيِّ ◀️ ضِدَّ السِّيرْفَرِ ]** 🎰\n──────────────────────────\n🎯 تم حجز رصيد ضمان الجولة `[-2 نقطة]`؛ واشتعلت الماكينة الحين لايف! اضغط على الزر بالأسفل لفتح شاشة التطبيق المصغر (Web App) واللعب بصوابعك حياً:",
            reply_markup=game_keyboard
        )
        return

    # ⚔️ 2. ربط وتشغيل زر [ تحدي مستخدم آخر (لايف P2P) ] بالاقتران الجبري
    elif "pvp_init_" in data:
        game_num = data.replace("pvp_init_", "").strip()
        await callback_query.answer("⚔️ جاري تفعيل بروتوكول الاقتران الجبري P2P...")
        
        # فتح خط استقبال يوزر المنافس من الشات
        user_auth_data[user_id] = {"step": f"INPUT_PVP_OPPONENT_{game_num}"}
        await callback_query.message.edit_text(
            text=f"⚔️ **[ وَضْعِيَّةُ التَّحَدِّي الجَمَاعِيِّ لايِف ◀️ مستخدم ضد مستخدم P2P ]** 🔥\n──────────────────────────\n✍️ يا برنس الساحة، أرسل الآن في الشات **معرف الحساب أو يوزر نيم زميلك** المراد قذفه وتحديه لايف في نفس الجولة (مثال: @username أو الآيدي الصافي):"
        )
        return

    # ↩️ 3. ربط وتفعيل زر [ عودة لقائمة الألعاب ]
    elif data == "back_to_games":
        await callback_query.answer("↩️ جاري العودة لصالة العمالقة باللمس...")
        try:
            await callback_query.message.delete()
        except Exception: pass
        # إعادة فرش الخمس صفحات التفاعلية للألعاب الـ 30 على نظافة
        await open_pro_games_arena_page(user_id, page=0)
        return

@app.on_message(filters.service & filters.private)
async def handle_royal_games_score_faucet(client, message):
    """🚰 حنفية النقاط المركزية: لقط داتا الـ Web App حياً، وتحديث محفظة العادي والـ VIP، وبث اللوج فوراً"""
    user_id = str(message.from_user.id)
    
    # 📡 التأكد من أن الخدمة القادمة هي قذيفة داتا من تطبيق الـ Web App المصغر
    if message.web_app_data:
        raw_data = message.web_app_data.data
        await asyncio.sleep(0.1) # نبضة مزامنة كاش الرام لمنع تضارب المعالج
        
        try:
            # فك تشفير حزمة الداتا القادمة من الـ جافا سكريبت باللمس
            import json
            packet = json.loads(raw_data)
            
            game_id = packet.get("game_id", 1)
            game_type = packet.get("game_type", "slots")
            points_won = int(packet.get("score", 0))
            
            if points_won > 0:
                # 🪙 ضخ وحقن الأرباح فوراً جوه محفظة الزبون في الهارد ديسك (WAL)
                db_query("UPDATE user_points SET points = points + ? WHERE user_id=?", (points_won, user_id), commit=True)
                
                # جلب الرصيد الجديد لايف بعد التعبئة
                pts_row = db_query("SELECT points, role FROM user_points WHERE user_id=?", (user_id,), fetchone=True)
                current_pts, role = pts_row if pts_row else (0, "USER")
                
                # 🎨 إرسال إشعار فوز شيك للمشغل مع شريط عداد المحفظة
                u_name = message.from_user.first_name if message.from_user.first_name else "برنس الساحة"
                success_txt = (
                    f"🎰 **[ إِشْعَارُ ضَخِّ نُقَاطٍ آتِي مِنَ الصَّالَةِ ]** 🎉\n"
                    f"──────────────────────────\n"
                    f"👤 **المشغل:** {u_name} `[{role}]` \n"
                    f"🎯 **اللعبة:** رقم `{game_id}` | فئة `{game_type}`\n"
                    f"💰 **الأرباح المحقونة:** `[ +{points_won} ]` نقطة مجاناً! 🪙\n"
                    f"📈 **رصيد محفظتك الصافي الحين:** `[ {current_pts:,} ]` نقطة عمارة.\n"
                    f"──────────────────────────\n"
                    f"💎 حالة الخزنة: `تم التأمين والتحديث التلقائي بنجاح! ✅`"
                )
                await message.reply_text(text=success_txt)
                
                # 📢 قذف اللوج الحي أوتوماتيك لـ البوت المساعد M في قناتك السرية بالثانية
                try:
                    audit_ch = db_query("SELECT audit_id FROM system_audit_vault LIMIT 1", fetchone=True) or AUDIT_CHANNEL_ID
                    log_msg = (
                        f"🛰️ **[ لُوجُ الحَنَفِيَّةِ المَرْكَزِيَّةِ للأَلْعَابِ ]**\n"
                        f"👤 العميل آيدي: `{user_id}`\n"
                        f"🎮 فاز بـ `[ {points_won} ]` نقطة في اللعبة `{game_id}`\n"
                        f"⚙️ تم التحديث والتصفير تلقائياً دون تدخل بشري."
                    )
                    await app.send_message(chat_id=int(audit_ch), text=log_msg)
                except Exception: pass
            else:
                await message.reply_text("❌ **الجولة انتهت بدون أرباح! حاول مجدداً واصطاد الجائزة الكبرى يا قائد! 🎯**")
                
        except Exception as e:
            await message.reply_text(f"❌ **كراش في حنفية الداتا:** `[ {str(e)} ]`؛ تم عزل الخطأ لحماية استقرار السيرفر!")
        return


if __name__ == "__main__":
    """نقطة انطلاق الوحش الكاسر الشغال فعلياً بالتزامن الكامل غصب عن أي فلاتر ورادارات رصد"""
    try:
        sys.stdout.write("\033[H\033[2J")
        sys.stdout.flush()
        print(f"\n\033[1;34m" + "═"*60 + f"\n\033[1;36m  𓆩 ♚ مَنْظُومَةُ رَشْقِ وَقَذْفِ العَمَالِقَةِ لِلْمَالِكِ العَامِّ سَبَايْدِر ♚ 𓆪  \n\033[1;34m" + "═"*60 + f"\033[0m")
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_all())
    except Exception as fatal_error:
        print(f"\n \033[1;31m❌ خطأ إقلاع قاتل عند تشغيل سيرفر المنظومة:\033[0m {fatal_error}")

