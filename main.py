import requests
import json
import os

USER_INFO_URL = "http://api.newhigh.net/user/info"
SIGNIN_URL = 'https://api.newhigh.net/user/signin'
VIDEO_URL = 'https://api.newhigh.net/monetizing/fishcoin/obtain/v2'
LUCKYDRAW_URL = 'https://api.newhigh.net/monetizing/luckydraw/v2'
PUSHPLUS_URL = 'https://www.pushplus.plus/send'

def main():
    access_token = os.environ["ACCESS_TOKEN"]
    pushplus_token = os.environ["PUSHPLUS_TOKEN"]

    user_info_headers = {
        'Content-Type': 'text/html',
        'Cookie': f"access_token={access_token}"
    }
    user_info_response = requests.get(USER_INFO_URL, headers=user_info_headers)
    user_info_data = user_info_response.json()
    
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

    signin_headers = {
        'Content-Type': 'application/json',
        'Cookie': f"access_token={access_token}"
    }

    signin_payload = {"front_channel_name": "IOS"}

    signin_response = requests.post(SIGNIN_URL, headers=signin_headers, data=json.dumps(signin_payload))
    signin_data = signin_response.json()
    signin_points = signin_data.get("body", {}).get("points")
    signin_continuoussign = signin_data.get("body", {}).get("continuoussign")

    video_headers = {
        'Content-Type': 'application/json',
        'Cookie': f"access_token={access_token}"
    }

    video_payload ={
        "task_id" : "2",
        "school_id" : school_id,
        "front_channel_name" : "IOS",
    }

    count = 0 
    while count < 2: 
        video_response = requests.post(VIDEO_URL, headers=video_headers, data=json.dumps(video_payload))
        video_data = video_response.json()
        videon_points = video_data.get("body", {}).get("total_obtained_points")
        count += 1 

    luckydraw_access_token = access_token.strip('"')
    
    luckydraw_headers = {
        'Content-Type': 'text/html',
        'access_token': luckydraw_access_token
    }
        
    luckydraw_get_url = f"https://api.newhigh.net/monetizing/luckydraw/v2?front_channel_name=IOS&school_id={school_id}"

    luckydraw_get_response = requests.get(luckydraw_get_url, headers=luckydraw_headers)
    luckydraw_get_data = luckydraw_get_response.json()
    
    luckydraw_payload = {
     "front_channel_name": "IOS",
     "school_id": school_id, 
     "lucky_draw_id": 37
    }

    luckydraw_response = requests.post(LUCKYDRAW_URL, headers=luckydraw_headers, data=json.dumps(luckydraw_payload))
    luckydraw_data = luckydraw_response.json()
    luckydraw_message = luckydraw_data.get("body", {}).get("prize", {}).get("name")

    user_info_response = requests.get(USER_INFO_URL, headers=user_info_headers)
    user_info_data = user_info_response.json()
    total_points = user_info_response.json().get("body", {}).get("points")

    
    pushplus_payload = {
        'token': pushplus_token,
        'title': '流海云印每日签到',
        'content': (f'流海用户：{nickname}\n 签到成功 +{signin_points} 鱼籽\n 已连续签到 {signin_continuoussign} 天\n '
                    f'抽奖获得 {luckydraw_message}\n 视频奖励 {videon_points} 鱼籽\n 现有鱼籽： {total_points}')
    }

    requests.post(PUSHPLUS_URL, data=pushplus_payload)

if __name__ == '__main__':
    main()
