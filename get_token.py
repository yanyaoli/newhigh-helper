import requests
import json
import random
import string
import re
from datetime import datetime

CONFIG_FILE_PATH = 'config.json'

def gen_random(n):
    chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    return ''.join(random.choice(chars) for _ in range(n))

def save_access_token_to_config(access_token):
    try:
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            config_data = json.load(config_file)
            access_tokens = config_data.get("access_tokens", [])
    except (FileNotFoundError, json.JSONDecodeError):
        config_data = {"access_tokens": []}
        access_tokens = config_data.get("access_tokens", [])

    if access_token:
        access_tokens.append(access_token)
    else:
        
        access_tokens = []

    config_data["access_tokens"] = access_tokens 
    config_data["update_time"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")  
    with open(CONFIG_FILE_PATH, 'w') as config_file:
        json.dump(config_data, config_file)


def get_access_tokens_from_config():
    try:
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            config_data = json.load(config_file)
            return config_data.get("access_tokens", [])
    except FileNotFoundError:
        return []

def extract_access_token_from_cookie(cookie_value):
    match = re.search(r'access_token="(.+?)"', cookie_value)
    if match:
        return match.group(1)
    return None

def main():
    # 清空原有的 access_tokens
    save_access_token_to_config("")

    while True:
        random_string = gen_random(9) + '3' + gen_random(6)
        random_code_string = gen_random(4) + '6' + gen_random(11)

        verification_url = f"https://api.newhigh.net/public/{random_string}?front_channel_name=web"

        response = requests.get(verification_url, headers={
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept-Language": "zh-Hans-US;q=1, en-US;q=0.9, zh-Hant-US;q=0.8"
        })
        verification_data = response.json()
        verification_code = verification_data["body"]["data"]

        user_phone = input("请输入手机号: ")

        sms_url = f"https://api.newhigh.net/{verification_code}?cellphone={user_phone}&code={random_code_string}&front_channel_name=web&sms_type=1&type=login"
        response = requests.get(sms_url, headers={
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept-Language": "zh-Hans-US;q=1, en-US;q=0.9, zh-Hant-US;q=0.8"
        })

        sms_code = input("请输入收到的验证码: ")

        post_url = "https://api.newhigh.net/common/sms"
        post_data = {
            "cellphone": user_phone,
            "verificationcode": sms_code
        }
        response = requests.post(post_url, json=post_data, headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept-Language": "zh-Hans-US;q=1, en-US;q=0.9, zh-Hant-US;q=0.8"
        })
        post_data = json.loads(response.text)

        login_url = "https://userapi.newhigh.net/user/login/v2"
        login_data = {
            "front_channel": "WEB",
            "cellphone": user_phone,
            "type": "local",
            "verification_code": sms_code
        }
        response = requests.post(login_url, json=login_data, headers={
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept-Language": "zh-Hans-US;q=1, en-US;q=0.9, zh-Hant-US;q=0.8"
        })

        set_cookie_value = response.headers.get("Set-Cookie")
        access_token = extract_access_token_from_cookie(set_cookie_value)

        save_access_token_to_config(access_token)

        continue_execution = input("是否继续执行获取 access_token 的操作？(y/n): ")
        if continue_execution.lower() != 'y':
            break

if __name__ == '__main__':
    main()
