# ==============================
# 🗄️ قاعدة البيانات SQLite المبسطة (تعمل فوراً)
# ==============================
import sqlite3
import json
import os

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# إعدادات البوت
OWNER_USER_ID = 5425405664
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8415474087:AAEDtwjvgogXfvpMzARe875svIEkSSDdNXk')
ALLOWED_USER_IDS = [OWNER_USER_ID]

def create_connection():
    """إنشاء اتصال مع SQLite"""
    try:
        db_path = '/tmp/telegram_bot.db' if 'RENDER' in os.environ else 'telegram_bot.db'
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"❌ خطأ في الاتصال بقاعدة البيانات: {e}")
        return None

def setup_database():
    """إنشاء الجداول في SQLite"""
    try:
        conn = create_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()
        
        # جدول المستخدمين الرئيسي
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT,
                phone TEXT,
                email TEXT,
                referral_code TEXT UNIQUE,
                invited_by TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ تم إعداد قاعدة البيانات SQLite بنجاح!")
        return True
        
    except Exception as e:
        logger.error(f"❌ خطأ في إعداد قاعدة البيانات: {e}")
        return False

async def check_user_registration(user_id: int) -> bool:
    """التحقق من تسجيل المستخدم"""
    try:
        conn = create_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (user_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
        
    except Exception as e:
        logger.error(f"❌ خطأ في التحقق من المستخدم: {e}")
        return False

def generate_referral_code():
    """إنشاء كود إحالة"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

async def validate_referral_code(code: str) -> bool:
    """التحقق من كود الدعوة"""
    try:
        conn = create_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE referral_code = ?", (code,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
        
    except Exception as e:
        logger.error(f"❌ خطأ في التحقق من الكود: {e}")
        return False

# ==============================
# 🤖 البوت المبسط (يعمل مباشرة)
# ==============================
async def start(update: Update, context: CallbackContext):
    """بدء البوت بشكل مبسط"""
    user = update.message.from_user
    
    await update.message.reply_text(
        f"🎉 **مرحباً {user.first_name}!**\n\n"
        "🏢 **أهلاً بك في نظام التسجيل**\n\n"
        "✅ البوت يعمل الآن بنجاح!\n\n"
        "🔧 جرب الأوامر:\n"
        "/profile - عرض الملف\n"
        "/invite - كود الدعوة"
    )

async def profile(update: Update, context: CallbackContext):
    """عرض الملف الشخصي المبسط"""
    user = update.message.from_user
    
    if await check_user_registration(user.id):
        await update.message.reply_text(
            f"📋 **ملفك الشخصي**\n\n"
            f"👤 الاسم: {user.first_name}\n"
            f"🆔 الآيدي: {user.id}\n"
            f"📅 مسجل مسبقاً في النظام\n\n"
            f"✅ كل شيء يعمل بشكل صحيح!"
        )
    else:
        await update.message.reply_text(
            f"👤 **مرحباً {user.first_name}**\n\n"
            f"🆔 الآيدي: {user.id}\n"
            f"📝 لم تسجل بعد في النظام\n\n"
            f"💡 استخدم /start للتسجيل"
        )

async def invite(update: Update, context: CallbackContext):
    """عرض كود الدعوة"""
    user = update.message.from_user
    referral_code = generate_referral_code()
    
    await update.message.reply_text(
        f"📢 **كود دعوتك الشخصي**\n\n"
        f"🔑 الكود: `{referral_code}`\n\n"
        f"💡 شارك هذا الكود مع أصدقائك!\n"
        f"🔗 الرابط: https://t.me/{(await context.bot.get_me()).username}?start={referral_code}"
    )

def main():
    """الدالة الرئيسية المبسطة"""
    print("🚀 بدء تشغيل البوت المبسط...")
    
    # إعداد قاعدة البيانات
    if not setup_database():
        print("❌ فشل إعداد قاعدة البيانات")
        return
    
    # إنشاء التطبيق
    application = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة الأوامر الأساسية فقط
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CommandHandler("invite", invite))
    
    print("✅ البوت المبسط يعمل الآن!")
    print("💡 الأوامر المتاحة: /start, /profile, /invite")
    
    # تشغيل البوت
    application.run_polling()

if __name__ == '__main__':
    main()
