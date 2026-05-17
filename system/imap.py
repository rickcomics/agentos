# system/imap.py

import imaplib
import email
from email.header import decode_header
import os
from system.config import load_env

def decode_value(value):
    if not value:
        return ""
    decoded, charset = decode_header(value)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(charset or "utf-8", errors="ignore")
    return decoded

def fetch_messages(mailbox="INBOX", since_uid=0, limit=5):
    env = load_env()

    host = env["IMAP_HOST"]
    user = env["IMAP_USER"]
    password = env["IMAP_PASSWORD"]

    mail = imaplib.IMAP4_SSL(host)
    mail.login(user, password)
    mail.select(mailbox)

    criteria = f"(UID {since_uid + 1}:*)"
    result, data = mail.uid("search", None, criteria)

    if result != "OK":
        return []

    uids = data[0].split()
    uids = uids[:limit]

    messages = []

    for uid in uids:
        result, msg_data = mail.uid("fetch", uid, "(RFC822)")
        if result != "OK":
            continue

        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)

        sender = decode_value(msg.get("From"))
        subject = decode_value(msg.get("Subject"))

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

        messages.append((
            int(uid),
            {
                "from": sender,
                "subject": subject,
                "body": body
            }
        ))

    mail.logout()
    return messages
