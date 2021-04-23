# -*- coding: utf-8 -*-
import scrapy
from ..items import QunaerItem
import parsel


class QunaerSpider(scrapy.Spider):
    name = 'qunaer'
    allowed_domains = ['piao.qunar.com']
    url = 'https://piao.qunar.com/ticket/list.htm?keyword=%E7%83%AD%E9%97%A8%E6%99%AF%E7%82%B9&region=&from=mps_search_suggest&subject=%E8%87%AA%E7%84%B6%E9%A3%8E%E5%85%89&page={}&sku='
    page = 1

    def start_requests(self):
        for i in range(0, 500, 30):
            url = self.url.format(i)
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response):
        items = QunaerItem()
        selector = parsel.Selector(response.text)
        lists = selector.css('#search-list .sight_item')
        for list in lists:
            items['title'] = list.css('.sight_item_caption a::attr(title)').get()  # 景区名字
            items['level'] = list.css('.sight_item_info .level::text').get()  # 景区等级
            items['area'] = list.css('.area a::attr(title)').get()  # 地区
            items['address'] = list.css('.address span::attr(title)').get()  # 地址
            items['province'] = items['area'].split("·")[0]
            string = list.css('.product_star_level em::attr(title)').get()  # 热度
            items['string']= float(string.strip('热度: '))
            items['intro']= list.css('.intro::attr(title)').get()  # 简介
            items['price'] = list.css('.sight_item_price em::text').get()  # 价格
            items['hot_num'] = list.css('.hot_num::text').get()  # 月销
            yield items