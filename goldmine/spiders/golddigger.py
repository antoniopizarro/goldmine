# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from goldmine.items import GoldmineItem



class GolddiggerSpider(CrawlSpider):
    # name = 'golddigger'
    # allowed_domains = ['goudengids.be']
    # start_urls = ['https://www.goudengids.be/zoeken/aannemers/']
    # # start_urls = ['http://www.dropsolid.com']

    # rules = [
    #     Rule(LinkExtractor(allow=['/aannemers/\d+/']),
    #         callback='parse_item',
    #         follow=True)
    # ]
    # rules = [
    #     Rule(LinkExtractor(allow=['.*']), callback='parse_item', follow=True),
    # ]

    name = 'golddigger'
    allowed_domains = ['goudengids.be']
    start_urls = ['https://www.goudengids.be/zoeken/+/']
    # start_urls = ['http://www.dropsolid.com']

    rules = [
        Rule(LinkExtractor(allow=['/zoeken/\+/\d+/']),
            callback='parse_item',
            follow=True)
    ]


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
            request = scrapy.Request(next_url, callback = self.parse_third)
            request.meta['item'] = item
            yield request

    def parse_third(self, response):
        print response.url
        item = response.meta['item']
        item['other_url'] = response.url
        item['name'] = str(response.css('h1::text').extract_first())
        item['address'] = str(response.css('li.icon.icon--poi::text').extract_first())

        number = response.css('li.icon.icon--phone a::text').extract()
        if number:
            if len(number)>1:
                telnumber = number[0]
                telnumber2 = number[1]
            else:
                telnumber = number[0]
                telnumber2 = ''
        else:
            telnumber = ''
            telnumber2 = ''
        item['telnumber'] = str(telnumber)
        item['secondTelnumber'] = str(telnumber2)

        emails = response.css('li.icon.icon--mail a::text').extract()
        if emails:
            if len(emails)>1:
                email = emails[0]
                email2 = emails[1]
            else:
                email = emails[0]
                email2 = ''
        else:
            email = ''
            email2 = ''
        item['email'] = str(email)
        item['secondEmail'] = str(email2)

        websites = response.css('li.icon.icon--website a::text').extract()
        if websites:
            if len(websites)>1:
                website = websites[0]
                website2 = websites[1]
            else:
                website = websites[0]
                website2 = ''
        else:
            website = ''
            website2 = ''
        
        item['website'] = str(website)
        item['secondWebsite'] = str(website2)

        cat = response.css('div[id=detail-kw] dl dd::text').extract_first()

        if cat:
            category = cat
        else:
            category = response.css('dl.list--horizontal a::text').extract_first()

        item['category'] = str(category)


        yield item
        print item




