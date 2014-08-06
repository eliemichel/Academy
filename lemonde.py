from urllib.request import urlopen
from lxml.etree import parse, HTMLParser
html = HTMLParser()

"""
Dump paragraphs from last LeMonde.fr articles (those in RSS feeds).
It can constitute an interesting sentence basis.
"""


page = urlopen('http://www.lemonde.fr/rss/')
dom = parse(page, html)

feeds = dom.xpath("//div[@id='contentMain']//table//tr//td[2]//a/@href")

count = 0
with open("lemonde.dump", 'w') as output:
	for f in feeds:
		try:
			page = urlopen(f)
			xml = parse(page)
		except e:
			print("[Error!]%s" % (e,))
			continue

		articles = xml.xpath("/rss/channel/item")

		for a in articles:
			count += 1
			link = a.xpath("link")[0].text.split('#')[0]
			print('[%d] Scanning %s...' % (count, link))

			try:
				page = urlopen(link)
				dom = parse(page, html)
			except Exception as e:
				print("[Error!]%s" % (e,))
				continue

			for body in dom.xpath("//div[@id='articleBody']"):
				paragraphs = body.xpath("p[not(@*)] | h2[@class='taille_courante']")

				for p in paragraphs:
					output.write(''.join(p.itertext()) + "\n")
			output.flush()


