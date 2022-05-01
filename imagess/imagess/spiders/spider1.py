import csv

import scrapy
from scrapy_splash import SplashRequest
import demjson


class Spider1(scrapy.Spider):
    name = 'mo'
    allowed_domains = ['toolspareparts.com.au']
    start_urls = ['https://www.toolspareparts.com.au/aeg-abg5520-spare-parts.html']

    def parse(self,response):

        with open('tools.csv', 'r') as f:
            reader = csv.reader(f)
            c = 0
            for i in reader:
                if c ==0:
                    c = 1
                    continue
                yield scrapy.Request(i[0],callback=self.parse_tool)


    def parse_tool(self,response):
        script = response.xpath('//div[@class="product media"]/script').get().split('>')[1].split('<')[0]
        dic = demjson.decode(script)
        img_links = dic['[data-gallery-role=gallery-placeholder]']["mage/gallery/gallery"]["data"]
        cleaning_urls = []
        for link in img_links:
            cleaning_urls.append(link["full"])

        yield {
            'image_urls': cleaning_urls
        }