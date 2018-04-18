import scrapy
import os
from scrapy.crawler import CrawlerProcess
from spiders.googlesearch import GoogleSearchSpider
from scrapy.utils.project import get_project_settings

# process = CrawlerProcess(get_project_settings())
# process.crawl(GoogleSearchSpider, depth=2, query='asd')
# process.start() 
command = "scrapy crawl googlesearch -a query={} -a depth={} -o {}.json --nolog"
items = [
	"anchor bolt",
	"batten",
	"bolt",
	"Screw",
	"brass",
	"buckle",
	"button",
	"cable tie",
	"captive fastener",
	"clamp",
	"hose clamp",
	"clasps",
	"lobster clasp",
	"cleco",
	"clips",
	"circlip",
	"hairpin clip",
	"paper clip",
	"terry clip",
	"clutch",
	"drawing pin",
	"flange",
	"frog",
	"grommet",
	"hook-and-eye closure",
	"hook and loop fastener",
	"Velcro",
	"latch",
	"nail",
	"pegs",
	"clothespin",
	"tent peg",
	"PEM nut",
	"pins",
	"bowtie cotter pin",
	"circle cotter",
	"clevis fastener",
	"cotter",
	"dowel",
	"linchpin",
	"R-clip",
	"split pin",
	"spring pin",
	"tapered pin",
	"retaining rings",
	"circlip",
	"e-ring",
	"rivet",
	"rock bolt",
	"rubber band",
	"screw anchor",
	"snap fastener",
	"staple",
	"stitches",
	"strap",
	"threaded fastener",
	"captive threaded fasteners",
	"nut",
	"screw",
	"washers",
	"threaded insert",
	"threaded rod",
	"tie",
	"toggle bolt",
	"treasury tag",
	"twist tie",
	"wedge anchor",
	"zipper"
]

test = [
	'asd', 'aaa'
]

if not os.path.exists(os.getcwd() + '/part2'):
	os.mkdir('part2')
for item in test:
	os.system(command.format(item, 2, 'part2/' + item))