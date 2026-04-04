#!/usr/bin/env python3
from config import ARMS_USERID, ARMS_PASSWORD, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

print("=== Credential Check ===")
print(f"ARMS_USERID: '{ARMS_USERID}'")
print(f"ARMS_PASSWORD length: {len(ARMS_PASSWORD) if ARMS_PASSWORD else 0}")
print(f"TELEGRAM_TOKEN length: {len(TELEGRAM_TOKEN) if TELEGRAM_TOKEN else 0}")
print(f"TELEGRAM_CHAT_ID length: {len(TELEGRAM_CHAT_ID) if TELEGRAM_CHAT_ID else 0}")

# Test telegram connection
try:
    from telegram_notifier import TelegramNotifier
    notifier = TelegramNotifier()
    if notifier.test_connection():
        print("✓ Telegram connection successful")
    else:
        print("✗ Telegram connection failed")
except Exception as e:
    print(f"✗ Telegram test error: {e}")
