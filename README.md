# BWT

BWIKI 小工具，基于MediaWiki API

## 作者

作者：若可_York，UID：339948505

## 环境

* Python 3

### 包

* request
* pandas
* xlrd

## 准备

请先在根目录创建一个`config.json`文件，填写以下内容

```json
{
	"url": "https://wiki.biligame.com/xxxx/api.php", // xxxx改为你的BWIKI链接
	"cookie":"xxxx"                                  // 改为当前登录用户的cookie
}
```

> 如何获取 cookie ？
>
> 登录BWIKI后，打开浏览器开发者工具（F12）的网络（network）标签页，再刷新当前页面（F5），点击列表中的第一个请求，在右侧弹出的信息窗口中找到cookie一项，全部复制并粘入对应位置。
> 如果登录状态为`valid`，即cookie正常
> 如果登陆状态为`invalid`，需要重新获取cookie
