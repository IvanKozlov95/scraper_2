# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy import Selector


class GoogleSearchSpider(scrapy.Spider):
	name = 'googlesearch'
	handle_httpstatus_list = [400, 200]

	rules = {
		'links': '//div[@class="s"]/../h3/a/@href',
		'names': '//div[@class="s"]/../h3/a/text()'
	}
	start_urls = [
		'https://www.google.com/search?q={}&num={}&hl={}',
	]

	def __init__(self, query, depth=10, lang='en', *args, **kwargs):
		self.query = query.replace(' ', '+')
		GoogleSearchSpider.start_urls[0] = GoogleSearchSpider.start_urls[0].format(query, depth, lang)
		super(GoogleSearchSpider, self).__init__(*args, **kwargs)

	def parse(self, response):
		data = self.parse_with_rules(response, GoogleSearchSpider.rules)[0]
		links = data['links']
		names = data['names']
		for idx, link in enumerate(links):
			if link is not '':
				url = link
				yield scrapy.Request(url,
					callback=self.company_page_parse, meta={ 'company': names[idx] },
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
		company = response.meta['company']
		if response.status == 400:
			yield {'company': company, 'error': 'bad request error'}
		contact_rule = "//a[text()[contains(.,'Contact')]]/@href"
		links = response.xpath(contact_rule).extract()
		for link in links:
			yield scrapy.Request(response.urljoin(link), callback=self.contact_page_parse, meta={ 'company': company }) 

	def contact_page_parse(self, response):
		phone_reg = re.compile('([0-9]{3})-([0-9]{3})-([0-9]{4})')
		email_reg = re.compile('\w+@\w*\.[a-z]{3}')
		yield {'company': response.meta['company'], 'phones': phone_reg.findall(str(response.body)), 'emails': email_reg.findall(str(response.body))}