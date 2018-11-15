# -*- coding: utf-8 -*-
import scrapy
import sys
import re


class EmailspiderSpider(scrapy.Spider):
    name = 'emailspider'
    allowed_domains = ['']
    start_urls = ['http://google.com/search?q=']

    def start_requests(self):
        query = input("Enter your query: ")
        for url in self.start_urls:
            yield scrapy.Request("{}{}".format(url, query))

    def parse(self, response):
        url_to_follow = response.css(".r>a::attr(href)").extract()
        url_to_follow = [url.replace('/url?q=', '') for url in url_to_follow]
        for url in url_to_follow:
            yield scrapy.Request(
                url=url, callback=self.parse_email, dont_filter=True)

        next_pages_urls = response.css("#foot table a::attr(href)").extract()
        for page_num, url in enumerate(next_pages_urls):
            if(page_num < 11):
                next_page_url = response.urljoin(url)
                yield scrapy.Request(
                    url=next_page_url, callback=self.parse, dont_filter=True)
            else:
                break

    def parse_email(self, response):
        html_str = response.text
        emails = self.extract_email(html_str)
        phone_no = self.extract_phone_number(html_str)
        yield{
            "url": response.url,
            "emails": emails,
            "phone numbers": phone_no
        }

    def extract_email(self, html_as_str):
        return re.findall(r'[\w\.-]+@[\w\.-]+', html_as_str)

    def extract_phone_number(self, html_as_str):
        return re.findall(r'\+\d{2}\s?0?\d{10}', html_as_str)
