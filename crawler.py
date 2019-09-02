import scrapy


class BookSpider(scrapy.Spider):
    name = 'books'

    # 定义爬虫爬取起始点
    start_urls = ['http://books.toscrape.com']

    def parse(self, response):
        for book in response.css('artical.produce_pod'):
            name = book.xpath('./h3/a/@title')
            price = book.css('p.price_color::text').extract_first()
            yield {
                'name': name,
                'price': price,
            }

        # 提取链接
        next_url = response.css(
            'ul.pager li.next a;::attr(href)').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse)


if __name__ == "__main__":
    sp = BookSpider()
    sp.parse()
