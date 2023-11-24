import requests
import json
import os
import re

USER_INFO_URL = "http://api.newhigh.net/user/info"
SIGNIN_URL = 'https://api.newhigh.net/user/signin'
VIDEO_URL = 'https://api.newhigh.net/monetizing/fishcoin/obtain/v2'
LUCKYDRAW_URL = 'https://api.newhigh.net/monetizing/luckydraw/v2'
PUSHPLUS_URL = 'https://www.pushplus.plus/send'

CONFIG_FILE_PATH = 'config.json'

def get_user_info(access_token):
    headers = {
        'Content-Type': 'text/html',
        'Cookie': f"access_token={access_token}"
    }
    response = requests.get(USER_INFO_URL, headers=headers)
    data = response.json()
    return data

def extract_access_token_from_cookie(cookie_value):
    match = re.search(r'access_token="(.+?)"', cookie_value)
    if match:
        return match.group(1)
    return None

def save_access_tokens_to_config(access_tokens):
    config_data = {"access_tokens": access_tokens}
    with open(CONFIG_FILE_PATH, 'w') as config_file:
        json.dump(config_data, config_file)

def load_access_tokens_from_config():
    try:
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            config_data = json.load(config_file)
            return config_data.get("access_tokens", [])
    except FileNotFoundError:
        return []

def save_config(config_data):
    with open(CONFIG_FILE_PATH, 'w') as config_file:
        json.dump(config_data, config_file)

def load_config():
    try:
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            config_data = json.load(config_file)
            return config_data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def main():
    config_data = load_config()
    access_tokens = load_access_tokens_from_config()
    pushplus_token = config_data.get("pushplus_token","")
    
    if not access_tokens:
        print("未找到有效的 access_tokens，请确保 config.json 中包含有效的 access_tokens。")
        return
    
    for access_token in access_tokens:
        user_info_data = get_user_info(access_token)
        if user_info_data.get("code") == "10002":
            print(f"access_token无效或已过期，请重新填写")
            # PushPlus 微信通知推送
            pushplus_payload = {
                'token': pushplus_token,
                'title': '流海云印每日签到',
                'content': f'access_token无效或已过期，请重新填写'
            }
            try:
                requests.post(PUSHPLUS_URL, data=pushplus_payload)
            except Exception as e:
                print(f"推送请求出错：{e}")
            continue

        nickname = user_info_data.get("body", {}).get("nickname")
        school_id = user_info_data.get("body", {}).get("school", {}).get("school_id")

        # 签到逻辑
        signin_headers = {
            'Content-Type': 'application/json',
            'Cookie': f"access_token={access_token}"
        }
        signin_payload = {"front_channel_name": "WECHAT_APPLET"}

        signin_response = requests.post(SIGNIN_URL, headers=signin_headers, data=json.dumps(signin_payload))
        signin_data = signin_response.json()
        signin_points = signin_data.get("body", {}).get("points")
        signin_continuoussign = signin_data.get("body", {}).get("continuoussign")

        # 视频奖励逻辑
        video_headers = {
            'Content-Type': 'application/json',
            'Cookie': f"access_token={access_token}"
        }
        video_payload ={
            "task_id" : "2",
            "school_id" : school_id,
            "front_channel_name" : "WECHAT_APPLET",
        }

        count = 0
        while count < 2:
            video_response = requests.post(VIDEO_URL, headers=video_headers, data=json.dumps(video_payload))
            video_data = video_response.json()
            videon_points = video_data.get("body", {}).get("total_obtained_points")
            count += 1

        # 抽奖逻辑
        luckydraw_access_token = access_token.strip('"')
        luckydraw_headers = {
            'Content-Type': 'text/html',
            'access_token': luckydraw_access_token
        }
        luckydraw_get_url = f"https://api.newhigh.net/monetizing/luckydraw/v2?front_channel_name=WECHAT_APPLET&school_id={school_id}"

        luckydraw_get_response = requests.get(luckydraw_get_url, headers=luckydraw_headers)
        luckydraw_get_data = luckydraw_get_response.json()

        luckydraw_payload = {
            "front_channel_name": "WECHAT_APPLET",
            "school_id": school_id,
            "lucky_draw_id": 37
        }

        luckydraw_response = requests.post(LUCKYDRAW_URL, headers=luckydraw_headers, data=json.dumps(luckydraw_payload))
        luckydraw_data = luckydraw_response.json()
        luckydraw_message = luckydraw_data.get("body", {}).get("prize", {}).get("name")

        # 再次获取用户信息，以更新总鱼籽数量
        user_info_data = get_user_info(access_token)
        total_points = user_info_data.get("body", {}).get("points")
        

        # 推送通知
        pushplus_payload = {
            'token': pushplus_token,
            'title': '流海云印每日签到',
            'content': (f'流海用户：{nickname}\n签到成功 +{signin_points} 鱼籽\n已连续签到 {signin_continuoussign} 天\n'
                        f'抽奖获得 {luckydraw_message}\n视频奖励 {videon_points} 鱼籽\n现有鱼籽： {total_points}')
        }

        requests.post(PUSHPLUS_URL, data=pushplus_payload)
        print(pushplus_payload)

if __name__ == '__main__':
    main()
