import os
import sys
import random

import django

# 设置环境
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social.settings")
django.setup()

from user.models import User

from faker import Faker
fake = Faker(locale='zh_CN')

def gen_user(n):
    for i in range(n):
        try:
            gender = random.choice(['male', 'female'])
            if gender == 'male':
                name = fake.name_male()
            else:
                name = fake.name_female()
            phone = fake.phone_number()
            city = fake.province()

            User.objects.create(nickname=name,gender=gender,phone=phone,location=city)
            print(f'gen_user: {name}')
        except:
            return 'genuser出现问题'


def show_user():
    # user = User.objects.all()
    users =User.objects.all()

    return users




if __name__ == "__main__":
    gen_user(100)