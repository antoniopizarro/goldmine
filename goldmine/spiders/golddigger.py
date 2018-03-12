# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from goldmine.items import GoldmineItem



class GolddiggerSpider(CrawlSpider):
    name = 'golddigger'
    allowed_domains = ['goudengids.be']
    start_urls = ['https://www.goudengids.be/zoeken/aannemers/']
    # start_urls = ['http://www.dropsolid.com']

    rules = [
        Rule(LinkExtractor(allow=['/aannemers/\d+/']),
            callback='parse_item',
            follow=True)
    ]
    # rules = [
    #     Rule(LinkExtractor(allow=['.*']), callback='parse_item', follow=True),
    # ]

    def parse_item(self, response):
        print response.url

        item = GoldmineItem()
        item['mainurl'] = response.url

        selector_list= response.css('li[itemprop=itemListElement]')
        for selector in selector_list:

            logo = response.css('div.result-item__logo img::attr(alt)').extract_first()

            if logo:
                logo = 'yes'
            else:
                logo = 'no'
            item['logo'] = logo

        links= response.css('a.result-item__heading::attr(href)').extract()
        for l in links:
            next_url = 'http://www.goudengids.be' + l
            request = scrapy.Request(next_url, callback = self.parse_1)
            request.meta['item'] = item
            yield request

        # selector_list= response.css('li[itemprop=itemListElement]')
        # # selector_list= response.css('ol.result-items')

        # for selector in selector_list:
        #     links = response.css('a.result-item__heading::attr(href)').extract()
        #     #print links
        #     for l in links:
        #         next_url = 'http://goudengids.be' + l
        #         return scrapy.Request(next_url, callback = self.parse_1)

        #     name = selector.css('h2::text').extract_first()
        #     # name = response.css()
        #     # address = 
        #     # logo =
        #     # website =
        #     item = GoldmineItem({'name': name})# 'address': 'logo': 'website':})
        #     yield item
        #     print item

    def parse_1(self, response):
        print response.url
        item = response.meta['item']
        item['other_url'] = response.url

        item['name'] = str(response.css('h1::text').extract_first())
        item['address'] = str(response.css('li.icon.icon--poi::text').extract_first())
        item['telnumber'] = str(response.css('li.icon.icon--phone a::text').extract_first())
        item['email'] = str(response.css('li.icon.icon--mail a::text').extract_first())
        item['website'] = str(response.css('li.icon.icon--website a::text').extract_first())

        yield item
        print item



