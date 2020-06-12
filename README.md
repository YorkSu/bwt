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
* pywin32
* cryptography

## 准备

请先在根目录创建一个`config.json`文件，填写以下内容

```json
{
  "host":"wiki.biligame.com", // BWIKI站点，不用改动
  "path":"/xxxx", // xxxx改为你的BWIKI链接
  "browser":"Edge", // 填写你的浏览器名字，目前支持新版Edge、Chrome
  "SESSDATA":"xxxxxx;" // 改为对应浏览器登录用户的SESSDATA
}
```

> 如何获取 SESSDATA ？
>
> 登录BWIKI后，打开浏览器开发者工具（F12）的网络（network）标签页，再刷新当前页面（F5），点击列表中的第一个请求，在右侧弹出的信息窗口中找到cookie一项，找到`SESSDATA`，将值复制出来即可。
