import	scrapy

class ChancellorsSpider(scrapy.Spider):
	name="asd"
	start_urls = [
		'https://en.wikipedia.org/wiki/List_of_engineering_schools'
	]

	def parse(self, response):
		i = 0
		us = '//*/table[8]/*//a[contains(@href, "University")]'
		india_univ = '//*/table[2]/*//a[contains(@href, "University")]'
		india_college = '//*/table[2]/*//a[contains(@href, "College")]'
		for bircket in response.xpath(us):
			yield scrapy.Request(response.urljoin(bircket.xpath('@href').extract()[0]), callback=self.parse_univ_page)
		for bircket in response.xpath(india_univ):
			yield scrapy.Request(response.urljoin(bircket.xpath('@href').extract()[0]), callback=self.parse_univ_page)
		for bircket in response.xpath(india_college):
			yield scrapy.Request(response.urljoin(bircket.xpath('@href').extract()[0]), callback=self.parse_univ_page)
	
	def parse_univ_page(self, response):
		xpchan = '//a[contains(@href, "Chancellor")]/../parent::node()/td/text()'
		xpdean = '//a[contains(@href, "Dean")]/../parent::node()/td/text()'
		xpdean2 = '//a[contains(@href, "Dean")]/../../parent::node()/td/text()'
		xppresident = '//a[contains(@href, "University_president")]/../parent::node()/td/*/text()'
		xppresident2 = '//a[contains(@href, "University_president")]/../parent::node()/td/text()'
		xpprincipal = '//a[contains(@href, "Principal")]/../parent::node()/td/*/text()'
		univ = '//h1[@id="firstHeading"]/text()'
		dean = response.xpath(xpdean).extract()
		if dean is []:
			dean = response.xpath(xpdean2).extract()
		president = response.xpath(xppresident).extract()
		if president is []:
			president = response.xpath(xppresident2).extract()
		yield {
			'university': response.xpath(univ).extract()[0],
			'dean': dean,
			'president': response.xpath(xppresident).extract(),
			'chancellor': response.xpath(xpchan).extract(),
			'principal': response.xpath(xpprincipal).extract()
		}