# WEB知识图谱构建

* 利用scrapy框架爬取去哪儿网热门景点信息
* 抽取三元组信息（存入mongdb数据库）
* 构建中文知识图谱（存入neo4j数据库）

## 环境构建
* Windows 10（也可在ubuntu）
* python 3.7
* mongdb 安装可参考[此处](https://www.cnblogs.com/billyzh/p/5913687.html)
* neo4j 安装可参考[此处](https://www.cnblogs.com/ljhdo/archive/2017/05/19/5521577.html)
> 注意：在python环境中需要安装 neo4j-driver

## 快速开始
1. 启动mongo服务
`$ net start MongDB`
2. 启动neo4j服务
`$ neo4j start`
3. 连接Neo4j Browser
	* 浏览器上访问 http://localhost:7474/
	* 用户名和密码与代码中一致 `auth=("neo4j", "123")`
4. 运行run.py
`$ cd WEB_qunaer/qunaer/spiders`
`$ python run.py`

## 运行效果
* 爬虫运行界面
![alt 属性文本](图片地址 "爬虫运行界面")
* mongdb存储去哪儿信息
![alt 属性文本](图片地址 "爬虫运行界面")
* mongdb存储三元组信息
![alt 属性文本](图片地址 "爬虫运行界面")
* 知识图谱结果
![alt 属性文本](图片地址 "爬虫运行界面")



最后感谢[WEB_KG](https://github.com/lixiang0/WEB_KG)!




