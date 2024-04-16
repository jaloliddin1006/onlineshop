import threading
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import random


class EmailThreading(threading.Thread):
    def __init__(self, subject, body, to_email, content_type):
        self.subject = subject
        self.body = body
        self.to_email = to_email
        self.content_type = content_type
        threading.Thread.__init__(self)

    def run(self):
        email = EmailMessage(
            subject=self.subject,
            body=self.body,
            to=[self.to_email]
        )
        if self.content_type == "html":
            email.content_subtype = "html"
        email.send()


def send_mail_code(email, code):
    html_content = render_to_string(
        template_name='accounts/password_reset_email.html',
        context={'code': code}
    )

    subject = "Instagram tashdiqlash uchun ro'yxatdan o'tish"
    body = html_content
    to_email = email
    content_type = 'html'

    EmailThreading(subject, body, to_email, content_type).start()


class VerifyEmailCode:
    def __init__(self):
        self.SIGN = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.K = 6

    def new_code(self):

        self.code_list = random.sample(self.SIGN, k=self.K)
        self.code = ''.join(self.code_list)  # list to string
        return self.code


