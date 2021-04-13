import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import RrepublicbankdominicaItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class RrepublicbankdominicaSpider(scrapy.Spider):
	name = 'republicbankdominica'
	start_urls = ['https://www.republicbankdominica.com/news']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@title="Go to next page"]/@href').get()
		if next_page:
			yield response.follow(next_page, self.parse)

	def parse_post(self, response):
		date = response.xpath('//div[@class="field field--name-body field--type-text-with-summary field--label-hidden field--item"]/p[1]//em//text()').get()
		date = re.findall(r'\w+\s\d+\,\s\d+',date)
		title = response.xpath('//h1/span/text()').get()
		content = response.xpath('//div[@class="content"]/div[@class="field field--name-body field--type-text-with-summary field--label-hidden field--item"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=RrepublicbankdominicaItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
