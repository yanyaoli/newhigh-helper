# 流海云印每日任务助手
- 自动化执行签到+抽奖+广告奖励+PUSHPLUS通知
- 自动化运行时间：北京时间上午00:01

## 如何使用
1. [Fork本仓库](https://github.com/ooyq/newhigh-helper)

2. 选择Fork后的仓库 -> **Settings** -> **Secrets and Variables** -> **Action** -> **New repository secret**, 添加Secrets变量如下:

|Name|Value|Required|
|:---:|:---:|:---:|
|ACCESS_TOKEN|流海云印登录授权|√|
|SCHOOL_ID|流海云印自己所在学校ID号|√|
|PUSHPLUS_TOKEN|[Pushplus](htps://pushplus.plus)官网申请，免费微信消息推送|×|

3. 仓库 -> Actions, 检查Workflows并启用。

## 如何获取ACCESS_TOKEN
1. 打开浏览器，登录 [流海云印官方网站](http://www.newhigh.net/login/log)
2. 打开网页控制台(快捷键F12或鼠标右键-检查) -> `Network`
3. 在`RequestUrl`中选择`info`，在`Preview`或者`Response`中找到 `school_id`，复制即可；
4.  在`RequestUrl`中选择`info`，在`Request headers`中找到`Cookie`,复制`access_token`后""中的内容，例如`Cookie: access_token=`

示例截图：
![image](https://github.com/ooyq/newhigh-helper/assets/120553430/b149cab9-37a8-4e7e-8577-f6e2630fe7d1)
![image](https://github.com/ooyq/newhigh-helper/assets/120553430/7572ab3c-8efa-4db0-afd8-1423f85eb62b)

其他方式：
> - IOS免费抓包软件-[Stream](https://apps.apple.com/cn/app/stream/id1312141691)
> - 安卓免费抓包软件-HtttpCanary

## 许可
[MIT](https://github.com/ooyq/newhigh-helper/blob/main/LICENSE)
