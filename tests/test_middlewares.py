"""This module contains the base test cases for the ``scrapy_selenium`` package"""

import asyncio
from twisted.internet import asyncioreactor

# Need to install the asyncio reactor before importing Scrapy (?)
# Maybe there is a cleaner way to to it?
asyncioreactor.install(asyncio.get_event_loop())

import scrapy
from scrapy.crawler import CrawlerRunner
from twisted.internet import defer
from twisted.trial.unittest import TestCase

import scrapy_puppeteer


class ScrapyPuppeteerTestCase(TestCase):
    """Test case for the ``scrapy-puppeteer`` package"""

    class PuppeteerSpider(scrapy.Spider):
        name = 'puppeteer_crawl_spider'
        allowed_domains = ['codesandbox.io']
        custom_settings = {
            'DOWNLOADER_MIDDLEWARES': {
                'scrapy_puppeteer.PuppeteerMiddleware': 800
            }
        }

        items = []

        def start_requests(self):
            yield scrapy_puppeteer.PuppeteerRequest(
                'https://codesandbox.io/search?page=1',
                wait_until='networkidle0'
            )

        def parse(self, response):
            for selector_item in response.selector.xpath('//li[@class="ais-Hits-item"]'):
                self.items.append(selector_item.xpath('.//h2').extract_first())

    def setUp(self):
        """Store the Scrapy runner to use in the tests"""

        self.runner = CrawlerRunner()

    @defer.inlineCallbacks
    def test_items_number(self):
        crawler = self.runner.create_crawler(self.PuppeteerSpider)
        yield crawler.crawl()
        self.assertEqual(len(crawler.spider.items), 10)
