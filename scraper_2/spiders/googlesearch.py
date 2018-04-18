# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy import Selector


class GoogleSearchSpider(scrapy.Spider):
	name = 'googlesearch'
	handle_httpstatus_list = [400, 200]

	rules = {
		'links': '//div[@class="s"]/../h3/a/@href'
	}
	start_urls = [
		'https://www.google.com/search?q={}&num={}&hl={}',
	]

	def __init__(self, query, *args, **kwargs):
		self.query = query.replace(' ', '+')
		GoogleSearchSpider.start_urls[0] = GoogleSearchSpider.start_urls[0].format(query, 3, 'en')
		super(GoogleSearchSpider, self).__init__(*args, **kwargs)

	def parse(self, response):
		data = self.parse_with_rules(response, GoogleSearchSpider.rules)[0]
		for link in data['links']:
			if link is not '':
				print(link)
				url = link
				print('link i am going to go: ', url)
				yield scrapy.Request(url,
					callback=self.company_page_parse, meta={ 'company': 'asd' },
					headers={'X-Requested-With': 'XMLHttpRequest','Content-Type':'application/json'})


	def parse_with_rules(self, response, rules):
		items = []
		self.traversal(Selector(response), rules, items)
		return items
	
	def traversal(self, sel, rules, items):
		item = {}
		for k, v in rules.items():
			if type(v) != dict:
				self.deal_text(sel, item, k, v)
			else:
				item[k] = []
				self.traversal(sel, v, item[k])
		items.append(item)

	def deal_text(self, sel, item, k, v):
		item[k] = self.extract_item(sel.xpath(v))

	def extract_item(self, sels):
		contents = []
		for i in sels:
			content = re.sub(r'\s+', ' ', i.extract())
			if content != ' ':
				contents.append(content)
		return contents

	def company_page_parse(self, response):
		if response.status == 400:
			print("ERROR\n")
			yield {}
		contact_rule = "//a[text()[contains(.,'Contact')]]/@href"
		company = response.meta['company']
		for link in response.xpath(contact_rule).extract():
			print('link: ', link)
			yield scrapy.Request(response.urljoin(link), callback=self.contact_page_parse, meta={ 'company': company }) 

	def contact_page_parse(self, response):
		# phone_reg = re.compile('/\(?([0-9]{3})\)?([ .-]?)([0-9]{3})\2([0-9]{4})/')
		phone_reg = re.compile('([0-9]{3})-([0-9]{3})-([0-9]{4})')
		yield {'phones': phone_reg.findall(str(response.body))}