import scrapy
from deposbs.items import DeposbsItem
from scrapy.loader import ItemLoader

class FirstSpider(scrapy.Spider):
	name = 'depos_spider'
	start_urls = ['some url']

	def parse(self, response):
		self.log('Page #: ' + response.url)
		for depo in response.css('div.posting-card'):
			url = depo.css('a.go-to-posting ::attr(href)').get()
			yield response.follow(url, self.parse_items)

		next_page_url = response.css('li.pag-go-next > a::attr(href)').get()
		if next_page_url:
			yield response.follow(next_page_url, self.parse)

	def parse_items(self, response):
		self.log('I just have visited: ' + response.url)
		item = DeposbsItem()
		item['name'] = response.css("h2.title-type-sup ::text").get()
		item['district'] = response.css("h2.title-location ::text").getall()
		item['total_square'] = response.xpath('//*[@id="article-container"]/section[1]/ul/li[1]/b/text()').get()
		item['covered_square'] = response.xpath('//*[@id="article-container"]/section[1]/ul/li[2]/b/text()').get()
		item['rooms'] = response.xpath('//*[@id="article-container"]/section[1]/ul/li[3]/b/text()').get()
		item['bathrooms'] = response.xpath('//*[@id="article-container"]/section[1]/ul/li[4]/b/text()').get()
		item['parking_lots'] = response.xpath('//*[@id="article-container"]/section[1]/ul/li[5]/b/text()').get()
		item['bedrooms'] = response.xpath('//*[@id="article-container"]/section[1]/ul/li[6]/b/text()').get()
		item['toilets'] = response.xpath('//*[@id="article-container"]/section[1]/ul/li[7]/b/text()').get()
		item['age'] = response.xpath('//*[@id="article-container"]/section[1]/ul/li[8]/b/text()').get()
		item['information'] = response.css('section.general-section.article-section > ul.section-bullets ::text').getall()
		item['price'] = response.css('div.price-items ::text').get()
		item['expenses'] = response.css('div.block-expensas.block-row >span::text').get()
		yield item

	

