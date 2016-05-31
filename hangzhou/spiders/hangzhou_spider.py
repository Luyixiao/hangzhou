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
    
    #���ǵ������е�㸴�ƣ������漰����һҳ��ת�����⣬Ȼ��Ϊ�˻�ȡÿ����Ŀ����Ϣ����Ҫ���ȥ���ӣ�����������һ������ÿ����������ù��ܾͺ�������ء�
  	#����֮ǰ����������˵һ��֩����߼��ɡ�
  	#ÿ��֩�붼��һ������Ȼ���Բ�ֹһ��start_url��������һ����֩�룬֩��ͻ�����������ڣ�Ȼ����һ����ҳ
  	#���ǰ������ҳ�����һ��html�ļ��Ϳ����ˡ�����ļ��أ��ᱻĬ�ϴ���prase������Ҳ�����������������
    def parse(self, response): #�����spider����Ĭ�ϵķ�����������һ����д��response�����Ǹ�html�ļ�Ŷ��
  
        sel = Selector(response)#��html���ļ���ת������һ��Selector��ѡ����������Ŷ���������ĺô��ǣ����Խ���xpath����css��
        #sel��һ��ѡ����Ŷ�����Ǿͺܷ���ʹ��xpathȥ��ȡһЩ���ݡ���ʱ���أ����ǻ�ȡ�Ļ���һ������list����Ϊ���·������Ҳ�����кܶಢ�У�ͬһ��level����Ŀ����       
        sites = sel.xpath('//*[@class="post"]/a/@href').extract()  
        #�����أ����ǰ����List��һ����������������أ��ͻ�ȡ��ĳһҳ25���������Ŷ�������û����xpath������Ŷ��
        #����xpath��ȥ��֮ǰ��һƪ���¿�һ�°�http://blog.csdn.net/qtlyx/article/details/51036437
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
            
    #����һ���ص���������Ĳ����ˣ�������ص��������棬�ֻص���һ������û��������һ�ָо���û���ȥһ��ҳ�棬
    #�Ͷ�һ���ص���������ʵ���������ġ��м�������Ǿͻ��ж��ٸ��ص�������        

    
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
        