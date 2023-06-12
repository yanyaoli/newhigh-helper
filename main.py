import requests
import json
import os

# 定义常量
USER_INFO_URL = "http://api.newhigh.net/user/info"
SIGNIN_URL = 'https://api.newhigh.net/user/signin'
VIDEO_URL = 'https://api.newhigh.net/monetizing/fishcoin/obtain/v2'
LUCKYDRAW_URL = 'https://api.newhigh.net/monetizing/luckydraw/v2'
PUSHPLUS_URL = 'https://www.pushplus.plus/send'

def main():
    access_token = os.environ["ACCESS_TOKEN"]
    pushplus_token = os.environ["PUSHPLUS_TOKEN"]

    # 用户信息
    user_info_headers = {
        'Content-Type': 'text/html',
        'Cookie': f"access_token={access_token}"
    }
    user_info_response = requests.get(USER_INFO_URL, headers=user_info_headers)
    user_info_data = user_info_response.json()
    
    # 判断响应的 code 是否为 "10002"
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
        # 结束程序
        exit()
    else:
        nickname = user_info_response.json().get("body", {}).get("nickname")
        school_id = user_info_response.json().get("body", {}).get("school", {}).get("school_id")

    # 签到请求
    signin_headers = {
        'Content-Type': 'application/json',
        'Cookie': f"access_token={access_token}"
    }

    signin_payload = {"front_channel_name": "IOS"}

    signin_response = requests.post(SIGNIN_URL, headers=signin_headers, data=json.dumps(signin_payload))
    signin_data = signin_response.json()
    signin_points = signin_data.get("body", {}).get("points")
    signin_continuoussign = signin_data.get("body", {}).get("continuoussign")

    # 视频奖励
    video_headers = {
        'Content-Type': 'application/json',
        'Cookie': f"access_token={access_token}"
    }

    video_payload ={
        "task_id" : "2",
        "school_id" : school_id,
        "front_channel_name" : "IOS",
    }

    count = 0 # 计数器
    while count < 2: 
        video_response = requests.post(VIDEO_URL, headers=video_headers, data=json.dumps(video_payload))
        video_data = video_response.json()
        videon_points = video_data.get("body", {}).get("total_obtained_points")
        count += 1 # 计数器加一

    # 抽奖
    luckydraw_headers = {
        'Host': 'api.newhigh.net',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Origin': 'https://luckydraw-h5.newhigh.net',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                       '(KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'),
        'Referer': 'https://luckydraw-h5.newhigh.net/',
        'access_token': access_token,
        'Content-Length': '65'
    }
    
    luckydraw_payload = {
     "front_channel_name": "IOS",
     "school_id": school_id, 
     "lucky_draw_id": 37
    }

    luckydraw_response = requests.post(LUCKYDRAW_URL, headers=luckydraw_headers, data=json.dumps(luckydraw_payload))
    luckydraw_data = luckydraw_response.json()
    luckydraw_message = luckydraw_data.get("body", {}).get("prize", {}).get("name")

    # 现有鱼籽
    user_info_response = requests.get(USER_INFO_URL, headers=user_info_headers)
    user_info_data = user_info_response.json()
    total_points = user_info_response.json().get("body", {}).get("points")

    # PushPlus 微信通知推送
    pushplus_payload = {
        'token': pushplus_token,
        'title': '流海云印每日签到',
        'content': (f'流海用户：{nickname}\n 签到成功 +{signin_points} 鱼籽\n 已连续签到 {signin_continuoussign} 天\n '
                    f'抽奖获得 {luckydraw_message}\n 视频奖励 {videon_points} 鱼籽\n 现有鱼籽： {total_points}')
    }

    requests.post(PUSHPLUS_URL, data=pushplus_payload)

if __name__ == '__main__':
    main()
