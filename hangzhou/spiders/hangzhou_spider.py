# coding=gbk
from scrapy.spiders import Spider  
from scrapy.selector import Selector  
import scrapy
#from scrapy import log  
  
from hangzhou.items import hangzhouItem  
  
  
class hangzhouSpider(Spider):  
   
    name = "hangzhoujobs"  
    start_urls = [  
        "http://jobs.zhaopin.com/hangzhou/p1/"  
    ]  #start url at the first page
    
    #我们的爬虫有点点复制，首先涉及到下一页跳转的问题，然后，为了获取每个数目的信息，还要点进去连接，反正道理都一样。给每个函数定义好功能就很清楚了呢。
  	#讲述之前，我们先来说一下蜘蛛的逻辑吧。
  	#每个蜘蛛都有一个（当然可以不止一个start_url），我们一运行蜘蛛，蜘蛛就会把这个当做入口，然后获得一个网页
  	#我们把这个网页想成是一个html文件就可以了。这个文件呢，会被默认传入prase方法，也就是下面这个方法。
    def parse(self, response): #这个是spider类中默认的方法，我们做一个重写，response就是那个html文件哦。
  
        sel = Selector(response)#“html”文件被转化成了一个Selector（选择器）对象哦。这个对象的好处是，可以接受xpath或者css。
        #sel是一个选择器哦，我们就很方便使用xpath去获取一些数据。有时候呢，我们获取的会是一个数据list，因为你的路径下面也许会有很多并列，同一个level的项目啊。       
        sites = sel.xpath('//*[@class="post"]/a/@href').extract()  
        #所以呢，我们把这个List做一个遍历，这个遍历呢，就获取了某一页25本书的连接哦。可以用火狐的xpath插件检查哦。
        #不会xpath就去我之前的一篇文章看一下吧http://blog.csdn.net/qtlyx/article/details/51036437
        for siteUrl in sites:  
            #siteUrl = "http://ourex.lib.sjtu.edu.cn/primo_library/libweb/action/"+siteUrl
            yield scrapy.Request(siteUrl, callback=self.getDetailParse)
        
        #next page  
        #urls = sel.xpath('/html/body/div[6]/div[1]/form/div/div/span[9]/a/@href').extract()
        for i in range(2,101):
            #print url
            url = "http://jobs.zhaopin.com/hangzhou/p"+str(i)+"/"
            #print "lyx"+url
            yield scrapy.Request(url, callback=self.parse)
            
    #这是一个回调函数多余的不讲了，在这个回调函数里面，又回调了一个。有没有这样的一种感觉，没点进去一个页面，
    #就多一个回调函数。其实就是这样的。有几个层次们就会有多少个回调函数。        

    
    def getDetailParse(self, response):   
        sel = Selector(response)
        item = hangzhouItem() 
        salary = sel.xpath('/html/body/div[6]/div[1]/ul/li[1]/strong/text()').extract()
        location1 = sel.xpath('/html/body/div[6]/div[1]/ul/li[2]/strong/text()').extract()
        location2 = sel.xpath('/html/body/div[6]/div[1]/div[1]/div/div[1]/h2[2]/text()').extract()
        jobDesc = sel.xpath('/html/body/div[6]/div[1]/ul/li[8]/strong/a/text()').extract()
        jobType = sel.xpath('/html/body/div[6]/div[1]/ul/li[4]/strong/text()').extract()
        degree = sel.xpath('/html/body/div[6]/div[1]/ul/li[6]/strong/text()').extract()
        # print "lyx status is" + str(status)
        #name = sel.xpath('//*[@id="resultsListNoId"]/div[1]/div[1]/div/h1/text()').extract() 
            
        item['salary'] = [t.encode('utf-8') for t in salary]  
        item['location1'] = [t.encode('utf-8') for t in location1]  
        item['location2'] = [t.encode('utf-8') for t in location2]  
        item['jobDesc'] = [t.encode('utf-8') for t in jobDesc]             
        item['jobType'] = [t.encode('utf-8') for t in jobType]  
        item['degree'] = [t.encode('utf-8') for t in degree]  
       
        yield item
   
  
        #log.msg("Append done.",level='INFO')  
        #return items  
        