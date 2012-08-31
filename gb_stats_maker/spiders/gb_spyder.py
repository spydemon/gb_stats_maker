from scrapy.spider import BaseSpider
from scrapy.http import FormRequest, Request
from scrapy.selector import HtmlXPathSelector
import re
import saveValues
import drawGraph
import os 
import sys

class gbSpider(BaseSpider):
	name="gb"
	start_urls = ["http://www.goldenboys.fr"]

	def parse(self, response):
		#We use a ugly way to catch user's name and password.
		#(Feel free to contact me if you know a better one ;-) )
		stp = open("stp", "rt")
		stp = stp.readline() 
		stp = stp.split(':')
		self.userName = stp[0]
		self.userPswd = stp[1]
		self.output = stp[2]
		os.system("rm stp")

		#After: authentication on the website.
		identity = {}
		identity['username'] = self.userName
		identity['password'] = self.userPswd
		return [FormRequest.from_response(response, formdata=identity, callback=self.after_login)]

	#After: we redirect to the interesting web-page. :p
	def after_login(self, response):
		return Request(url="http://www.goldenboys.fr/portefeuille", callback=self.catching)

	#Finaly: start to work...
	def catching(self, response):
		hxs = HtmlXPathSelector(response)
		#We crawl only the name of companies and the evolution.
		name = hxs.select("//tr[contains(@class, 'pair')]/td[1]").extract()
		values = hxs.select("//tr[contains(@class, 'pair')]/td[6]").extract()
		#We check if the user is log in.
		if len(name) == 0:
			print "====================================================================="
			print "====================================================================="
			print "!!! WARNING : No compagny was found! You've probably made a mistake in your account setting."
			print "====================================================================="
			print "====================================================================="
			sys.exit(1)

		content = {}
		a = 0;
		for v in values:
			try:
				#For conserving only the real thigs that we need.
				pur_name = re.split("<", name[a])[2].split(">")[1]
				pur_value = re.split("<", v)[1].split("(")[1].split(")")[0].split("%")[0]
			except:
				#Sometime we also catch lines in the table that aren't our actions....
				print "Unvalid value, but we don't care: probably one action that are waiting to be buy or sell."
			else:
				#Values are written in this list.
				content[pur_name] = pur_value
			a+=1

		#Here we call the function for saving datas.
		fileName = self.userName + ".txt"
		v = saveValues.SaveValues(fileName)
		v.update(content)
		#And finaly, we make the graph!
		d = drawGraph.DrawGraph(fileName, self.userName, self.output)
