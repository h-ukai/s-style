import smtplib
from email.mime.text import MIMEText

SMTP_HOST = "sv1231.xserver.jp"
SMTP_PORT = 465  # 465=SSL, 587=STARTTLS
SMTP_USER = "info@s-style.ne.jp"
SMTP_PASS = "o]iZVVis+E8v"

FROM_ADDR = "info@s-style.ne.jp"
TO_ADDR = "info@s-style.ne.jp"

msg = MIMEText("これはPythonからのSMTPテスト送信です。", _charset="utf-8")
msg["Subject"] = "SMTPテスト"
msg["From"] = FROM_ADDR
msg["To"] = TO_ADDR

# 465 (SSL) で接続
with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
    smtp.set_debuglevel(1)  # やりとりを表示
    smtp.login(SMTP_USER, SMTP_PASS)
    smtp.send_message(msg)

print("送信完了")
