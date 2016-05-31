# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item,Field  
  
class hangzhouItem(Item):  
    salary = Field()  
    location1 = Field()
    location2 = Field()
    jobDesc  = Field()
    jobType = Field()  
    degree = Field()
# we catch four elements to analysis the jobs