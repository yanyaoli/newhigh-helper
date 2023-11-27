# 流海云印任务助手
- 每日签到 + 每日抽奖 + 广告视频奖励 + PUSHPLUS推送
- 运行时间：北京时间上午00:01
- 支持多账号任务 【多个Access_token之间用 `,` 隔开】

## 如何使用
1. [Fork本仓库](https://github.com/yanyaoli/newhigh-helper)

2. 选择Fork后的仓库 -> **Settings** -> **Secrets and Variables** -> **Action** -> **New repository secret**, 添加Secrets变量如下:

|Name|Value|Required|
|:---:|:---:|:---:|
|ACCESS_TOKEN|流海云印登录授权|√|
|PUSHPLUS_TOKEN|[Pushplus](htps://pushplus.plus)官网申请，免费微信消息推送|×|

3. 仓库 -> Actions, 检查Workflows并启用。

### 获取Token

1. 打开浏览器，登录 [流海云印官方网站](http://www.newhigh.net/login/log)
2. 打开网页控制台(快捷键F12或鼠标右键-检查) -> **`Application`**
3. 在右侧 **`Storage`** 中选择 **`Cookies`**，再选择`http://www.newhigh.net`
4. 下滑找到 **`access_token`** ，复制`Value`中的值即可

> 如果已搭建Python环境，可使用get_token.py获取access_token
<br>

示例:
![image](https://github.com/yanyaoli/newhigh-helper/assets/120553430/03835537-160d-4cd0-92a5-895b67d43e0c)


其他方式：
> - IOS免费抓包软件:[Stream](https://apps.apple.com/cn/app/stream/id1312141691)
> - 安卓免费抓包软件:HttpCanary
