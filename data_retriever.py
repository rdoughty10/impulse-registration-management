import imaplib
import email
import os
import base64

email_user = input('Email: ')
email_pass = input('Password: ')

mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
mail.login(email_user, email_pass)

mail.select("Inbox")