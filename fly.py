import requests
import time
import re

# === কনফিগারেশন ===
BOT_TOKEN = "8088614895:AAFSaitJ0UWU95wmAwy8Ho3xsfGfRkNa6zc"
CHAT_ID = "-1002707159160"
API_TOKEN = "f3-Ydn5PUTxHTg=="
YOUR_NAME = "NAYEM"

# প্যানেল থেকে ডাটা আনার লিঙ্ক
API_URL = f"http://193.70.33.154/ints/agent/res/data_smscdr.php?token={API_TOKEN}"

def fetch_otp():
    last_sent_time = None
    print(f"🚀 {YOUR_NAME} Bot is starting... Monitoring FlySMS Panel.")

    while True:
        try:
            response = requests.get(API_URL, timeout=15)
            data = response.json()

            if "aaData" in data and len(data["aaData"]) > 0:
                latest_sms = data["aaData"][-1]
                sms_time = latest_sms[0]
                number = latest_sms[2]
                service = latest_sms[3]
                message = latest_sms[5]

                if sms_time != last_sent_time:
                    otp_code = re.findall(r'\b\d{4,8}\b', message)
                    display_otp = otp_code[0] if otp_code else "Check Message"
                    
                    text = (
                        f"📩 <b>NEW OTP RECEIVED</b>\n\n"
                        f"<b>🔑 OTP Code (Tap to Copy):</b>\n"
                        f"<code>{display_otp}</code>\n\n"
                        f"<b>📝 Full Message:</b>\n"
                        f"<i>{message}</i>\n\n"
                        f"<b>━━━━━━━━ Details ━━━━━━━━</b>\n"
                        f"<b>📞 Number:</b> <code>{number}</code>\n"
                        f"<b>🔧 Service:</b> {service}\n"
                        f"<b>⏰ Time:</b> {sms_time}\n\n"
                        f"👤 <b>Owner:</b> <b>{YOUR_NAME}</b>"
                    )

                    tg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                    requests.post(tg_url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})
                    last_sent_time = sms_time
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        time.sleep(5)

if __name__ == "__main__":
    fetch_otp()
