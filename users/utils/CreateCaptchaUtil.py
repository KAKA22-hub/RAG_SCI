import random

class CreateCaptcha:
    def __init__(self):
        pass
    @staticmethod
    def create_captcha():
        captcha = random.randint(1000, 9999)
        return captcha