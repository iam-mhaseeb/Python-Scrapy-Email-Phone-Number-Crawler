# -*- coding: utf-8 -*-
import scrapy
import sys


class EmailspiderSpider(scrapy.Spider):
    name = 'emailspider'
    allowed_domains = ['']
    start_urls = ['http://google.com/search?q=']

    def start_requests(self):
        query = input("Enter your query: ")
        for url in self.start_urls:
            yield scrapy.Request("{}{}".format(url, query))

    def parse(self, response):
        links_to_follow = response.css("h3.r a::attr(href)").extract()
        print("---------------------")
        print(links_to_follow)