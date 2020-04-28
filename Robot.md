# Robot & User-Agent



## 1.robots协议

> ​	robots.txt文件是一个文本文件，使用任何一个常见的文本编辑器，比如Windows系统自带的Notepad，就可以创建和编辑它 [1]  。robots.txt是一个协议，而不是一个命令。robots.txt是搜索引擎中访问网站的时候要查看的第一个文件。robots.txt文件告诉蜘蛛程序在服务器上什么文件是可以被查看的。
>
> ​	当一个搜索蜘蛛访问一个站点时，它会首先检查该站点根目录下是否存在robots.txt，如果存在，搜索机器人就会按照该文件中的内容来确定访问的范围；如果该文件不存在，所有的搜索蜘蛛将能够访问网站上所有没有被口令保护的页面。百度官方建议，仅当您的网站包含不希望被搜索引擎收录的内容时，才需要使用robots.txt文件。如果您希望搜索引擎收录网站上所有内容，请勿建立robots.txt文件。
>
> ​	如果将网站视为酒店里的一个房间，robots.txt就是主人在房间门口悬挂的“请勿打扰”或“欢迎打扫”的提示牌。这个文件告诉来访的搜索引擎哪些房间可以进入和参观，哪些房间因为存放贵重物品，或可能涉及住户及访客的隐私而不对搜索引擎开放。但robots.txt不是命令，也不是防火墙，如同守门人无法阻止窃贼等恶意闯入者。
>
> *来源：[百度百科robots协议](https://baike.baidu.com/item/robots%E5%8D%8F%E8%AE%AE/2483797?fr=aladdin)*

>robots.txt的常规写法
>
>最简单的robots.txt只有两条规则：
>
>　　User-agent：指定对哪些爬虫生效
>
>　　Disallow：指定要屏蔽的网址
>
>　　整个文件分为x节，一节由y个User-agent行和z个Disallow行组成。一节就表示对User-agent行指定的y个爬虫屏蔽z个网址。这里x>=0，y>0，z>0。x=0时即表示空文件，空文件等同于没有robots.txt。
>
>1）、User-agent
>
>　　爬虫抓取时会声明自己的身份，这就是User-agent，没错，就是http协议里的User-agent，robots.txt利用User-agent来区分各个引擎的爬虫。
>
>　　举例说明：google网页搜索爬虫的User-agent为Googlebot，下面这行就指定google的爬虫。
>
>　　User-agent：Googlebot
>
>　　如果想指定所有的爬虫怎么办？不可能穷举啊，可以用下面这一行：
>
>　　User-agent: *
>
>（2）、Disallow
>
>　　Disallow行列出的是要拦截的网页，以正斜线 (/) 开头，可以列出特定的网址或模式。
>
>　　要屏蔽整个网站，使用正斜线即可，如下所示：
>
>　　Disallow: /
>
>　　要屏蔽某一目录以及其中的所有内容，在目录名后添加正斜线，如下所示：
>
>　　Disallow: /无用目录名/
>
>　　要屏蔽某个具体的网页，就指出这个网页，如下所示：
>
>　　Disallow: /网页.html
>
>　　举例：
>
>　　User-agent: baiduspider
>
>　　Disallow: /
>
>　　User-agent: Googlebot
>
>　　Disallow: /
>
>　　seo解释：意思也就是禁止百度蜘蛛和Google蜘蛛抓取所有文章
>
>京东的rotobs协议，网址：
>
>```
>User-agent: *               #任何爬虫的来源都应该遵守如下协议额
>Disallow: /?* 　　　　　　　　 #不允许爬取以？开头的路径
>Disallow: /pop/*.html  　　　　#不允许访问/pop/....html的页面
>Disallow: /pinpai/*.html?*    #不允许访问 /pinpai/....html？...　　　　　　　　　
>```
>*来源：[豆瓣](https://www.douban.com/note/288060709/)*

　　robots协议采用通配符编写，其中*可以代表任何字符串；?仅代表单个字符串，但此单字必须存在。

## 2.User-agent

​	根据以上内容，我们知道普通浏览器爬虫是无法爬取百度文库内容的。通过观察百度文库robots.txt文件，我们发现一些蜘蛛可以爬取百度文库内容，例如：

> User-agent: Baiduspider
>
> Disallow: /w?
>
> Disallow: /search?
>
> Disallow: /submit
>
> Disallow: /upload
>
> Disallow: /cashier/
>
> [百度文库robots协议](https://wenku.baidu.com/robots.txt)

​	而我们需要爬取的内容url格式为https://wenku.baidu.com/view/?.html，这代表Baiduspider应该可以爬取文库内容。大致猜测这是因为百度搜索时需要根据文本内容匹配搜索选项，所以放行。

​	因此我们尝试伪装User-agent为Baiduspider。

```python
header = {'User-agent': 'Baiduspider'}
```

​	然后print request得到的文件，发现已经和百度文库内直接查看的源代码不一样了（参考html.txt）！此时，百度文库内的文本已经显示在源代码中。

​	然而，我们发现这个代码与检查网页后得到的代码还是不同的。通过分析这份源代码而非另外两种代码，我们写出来这部分的爬取代码（爬取百度文库 txt v2.py），并成功爬取文本文件（baiduwenku2.txt）。

​	同时我们尝试了[百度文库robots协议](https://wenku.baidu.com/robots.txt)内的其他spider，如Googlebot，发现均可以实现爬虫。

​	**而我们的这些尝试，是在百度上搜索不到！**