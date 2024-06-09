import imaplib
import email
from config import read_ini_file


class CheckMail:

    def __init__(self):
        config = read_ini_file(section='mail')
        self.user_name = config['mail_name']
        self.password = config['mail_password']
        self.imap_server = config['imap_server']

    def check_mail_box(self):
        imap = imaplib.IMAP4_SSL(self.imap_server)
        imap.login(self.user_name, self.password)
        imap.select("inbox")

        status, response = imap.uid('search', "UNSEEN", "ALL")
        if status == 'OK':
            messages = []
            unread_msg_nums = response[0].split()
            for ms_num in unread_msg_nums:
                res, msg = imap.uid('fetch', ms_num, '(RFC822)')  #Для метода uid
                msg = email.message_from_bytes(msg[0][1])
                for part in msg.walk():
                    try:
                        message = part.get_payload(decode=True).decode()
                        message = message.replace('<div>', '')
                        message = message.replace('</div>', '')
                    except:
                        message = part.get_payload()

                text = f"<b>Уведомдение с почты {self.user_name}</b>\n{message}"
                messages.append(text)
            return messages


