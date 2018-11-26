# Scrapy with Puppeteer
[![PyPI](https://img.shields.io/pypi/v/scrapy-puppeteer.svg)](https://pypi.python.org/pypi/scrapy-puppeteer) [![Build Status](https://travis-ci.org/clemfromspace/scrapy-puppeteer.svg?branch=master)](https://travis-ci.org/clemfromspace/scrapy-puppeteer) [![Test Coverage](https://api.codeclimate.com/v1/badges/5c737098dc38a835ff96/test_coverage)](https://codeclimate.com/github/clemfromspace/scrapy-puppeteer/test_coverage) [![Maintainability](https://api.codeclimate.com/v1/badges/5c737098dc38a835ff96/maintainability)](https://codeclimate.com/github/clemfromspace/scrapy-puppeteer/maintainability)

Scrapy middleware to handle javascript pages using [puppeteer](https://github.com/GoogleChrome/puppeteer).

## ⚠ IN ACTIVE DEVELOPMENT ⚠

## Installation
```
$ pip install scrapy-puppeteer
```

## Configuration
Given that Scrapy rely on Twisted for his asynchronous part, and given that the Puppeteer python port is based on asyncio,
we need a "hack" to make the two compatible with each other.

As a consequence, you need to import the `scrapy_puppeteer` package as soon as possible in your code.
 

Add the `PuppeteerMiddleware` to the downloader middlewares:
```python
DOWNLOADER_MIDDLEWARES = {
    'scrapy_puppeteer.PuppeteerMiddleware': 800
}
```


## Usage
Use the `scrapy_puppeteer.PuppeteerRequest` instead of the Scrapy built-in `Request` like below:
```python
from scrapy_puppeteer import PuppeteerRequest

def your_parse_method(self, response):
    # Your code...
    yield PuppeteerRequest('http://httpbin.org', self.parse_result)
```
The request will be then handled by puppeteer.

The `selector` response attribute work as usual (but contains the html processed by puppeteer).

```python
def parse_result(self, response):
    print(response.selector.xpath('//title/@text'))
```

### Additional arguments
The `scrapy_puppeteer.PuppeteerRequest` accept 2 additional arguments:

#### `wait_until`

Will be passed to the [`waitUntil`](https://miyakogi.github.io/pyppeteer/_modules/pyppeteer/page.html#Page.goto) parameter of puppeteer.
Default to `networkidle0`.

#### `screenshot`
When used, puppeteer will take a [screenshot](https://miyakogi.github.io/pyppeteer/reference.html?highlight=headers#pyppeteer.page.Page.screenshot) of the page and the binary data of the .png captured will be added to the response `meta`:
```python
yield PuppeteerRequest(
    url,
    self.parse_result,
    screenshot=True
)

def parse_result(self, response):
    with open('image.png', 'wb') as image_file:
        image_file.write(response.meta['screenshot'])
```

