# 流海云印每日任务助手
- 每日自动签到+抽奖+广告奖励+PUSHPLUS通知
- 运行时间：北京时间上午00:01

## 如何使用
1. [Fork本仓库](https://github.com/ViiAyil/newhigh-helper)

2. 选择Fork后的仓库 -> **Settings** -> **Secrets and Variables** -> **Action** -> **New repository secret**, 添加Secrets变量如下:

|Name|Value|Required|
|:---:|:---:|:---:|
|ACCESS_TOKEN|流海云印登录授权|√|
|PUSHPLUS_TOKEN|[Pushplus](htps://pushplus.plus)官网申请，免费微信消息推送|×|

3. 仓库 -> Actions, 检查Workflows并启用。

## 如何获取ACCESS_TOKEN
1. 打开浏览器，登录 [流海云印官方网站](http://www.newhigh.net/login/log)
2. 打开网页控制台(快捷键F12或鼠标右键-检查) -> **`Application`**
3. 在右侧 **`Storage`** 中选择 **`Cookies`**，再选择`http://www.newhigh.net`
4. 下滑找到 **`access_token`** ，复制`Value`中的值即可

示例截图：
![image](https://github.com/ViiAyil/newhigh-helper/assets/120553430/0ac19bc1-89e0-467f-86f1-9bd8819ecabf)


其他方式：
> - IOS免费抓包软件-[Stream](https://apps.apple.com/cn/app/stream/id1312141691)
> - 安卓免费抓包软件-HttpCanary

## 许可
[MIT](https://github.com/ooyq/newhigh-helper/blob/main/LICENSE)
