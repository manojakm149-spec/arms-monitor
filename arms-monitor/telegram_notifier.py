import requests
from datetime import datetime
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


class TelegramNotifier:
    def __init__(self):
        self.token = TELEGRAM_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.api = f"https://api.telegram.org/bot{self.token}" if self.token else None
        self.enabled = bool(self.token and self.chat_id)

        # Validate required environment variables
        if not self.token:
            print("[WARNING] TELEGRAM_TOKEN environment variable is not set - Telegram notifications disabled")
        if not self.chat_id:
            print("[WARNING] TELEGRAM_CHAT_ID environment variable is not set - Telegram notifications disabled")

        if self.enabled:
            # Ensure chat_id is a string (required by Telegram API)
            self.chat_id = str(self.chat_id)
            print(f"[DEBUG] TelegramNotifier initialized with token: {self.token[:10]}... and chat_id: {self.chat_id}")
        else:
            print("[INFO] Telegram notifications are disabled (missing environment variables)")

    def _send(self, text):
        if not self.enabled:
            print(f"[SKIP] Telegram disabled - would send: {text[:50]}...")
            return True  # Return True to not break the flow

        try:
            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": "HTML"
            }
            print(f"[DEBUG] Sending to Telegram: chat_id={self.chat_id}, text_length={len(text)}")

            r = requests.post(
                f"{self.api}/sendMessage",
                json=payload,
                timeout=10
            )

            print(f"[DEBUG] Telegram API Response: Status={r.status_code}")
            print(f"[DEBUG] Response content: {r.text}")

            if r.status_code == 200:
                response_data = r.json()
                if response_data.get("ok"):
                    print("[✓] Telegram message sent successfully")
                    return True
                else:
                    print(f"[✗] Telegram API returned error: {response_data.get('description', 'Unknown error')}")
                    return False
            else:
                print(f"[✗] Telegram API request failed with status {r.status_code}")
                return False

        except requests.exceptions.Timeout:
            print("[✗] Telegram request timed out (10s)")
            return False
        except requests.exceptions.ConnectionError:
            print("[✗] Telegram connection error - check internet/network")
            return False
        except Exception as e:
            print(f"[✗] Telegram error: {e}")
            return False

    def test_connection(self):
        if not self.enabled:
            print("[SKIP] Telegram disabled - skipping connection test")
            return False

        try:
            print(f"[DEBUG] Testing Telegram connection with token: {self.token[:10]}...")
            print(f"[DEBUG] Chat ID: {self.chat_id}")

            r = requests.get(f"{self.api}/getMe", timeout=10)

            print(f"[DEBUG] getMe Response: Status={r.status_code}")
            print(f"[DEBUG] Response content: {r.text}")

            if r.status_code == 200:
                response_data = r.json()
                if response_data.get("ok"):
                    name = response_data["result"]["first_name"]
                    print(f"[✓] Telegram connected — Bot: {name}")
                    return True
                else:
                    print(f"[✗] Telegram API returned error: {response_data.get('description', 'Unknown error')}")
                    return False
            else:
                print(f"[✗] Telegram getMe failed with status {r.status_code}")
                return False

        except requests.exceptions.Timeout:
            print("[✗] Telegram test timed out (10s)")
            return False
        except requests.exceptions.ConnectionError:
            print("[✗] Telegram connection error - check internet/network")
            return False
        except Exception as e:
            print(f"[✗] Telegram test failed: {e}")
            return False

    def notify_start(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_message = (
            f"🚀 <b>ARMS Monitor Started</b>\n"
            f"🕐 {now}\n\n"
            f"I'll ping you the moment your results are published! 📡"
        )

        print("[INFO] Sending startup notification")
        sent = self._send(start_message)

        if sent:
            print("[✓] Startup notification sent")
        else:
            print("[✗] Failed to send startup notification")

        return sent

    def send_notification(self, course_code, course_name, grade, status, month_year):
        message = (
            f"🎓 <b>NEW RESULT PUBLISHED!</b>\n\n"
            f"📘 <b>Course:</b> {course_name}\n"
            f"🔖 <b>Code:</b> {course_code}\n"
            f"✅ <b>Status:</b> {status}\n"
            f"📅 <b>Month/Year:</b> {month_year}\n\n"
            f"Check your ARMS portal now! 🎉"
        )

        print(f"[INFO] Attempting to send notification for course: {course_code}")
        sent = self._send(message)

        if sent:
            print(f"[✓] Notification sent successfully for {course_code}")
        else:
            print(f"[✗] Failed to send notification for {course_code}")

        return sent

    def notify_error(self, msg):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_message = f"⚠️ <b>ARMS Monitor Error</b>\n🕐 {now}\n\n❌ {msg}"

        print(f"[INFO] Sending error notification: {msg}")
        sent = self._send(error_message)

        if sent:
            print("[✓] Error notification sent successfully")
        else:
            print("[✗] Failed to send error notification")

        return sent