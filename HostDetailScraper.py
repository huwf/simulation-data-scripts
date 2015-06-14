from BeautifulSoup import BeautifulSoup
import sys
sys.path.insert(0, '..')
from URLGetter import URLGetter
import time

ug = URLGetter()
urls = []
with open('countries.txt', 'r') as f:
	urls = eval(f.read())
with open('sql.txt', 'w') as f:	
	for u in urls:
		i = 1
		while True: #We don't know how many pages there are going to be		
			url = "%s?pi=%d" % (u[0], i)
			print url
			html = ug.request(url)['html']
			#print html
			soup = BeautifulSoup(html)
			rows = soup.find(id="AutoNumber7").find('table').findAll('tr')
			carry_on = False
			for tr in rows:						
				if(tr.find('td') != None):			
					cells = tr.findAll('td')#.find('a').text
					
					if len(cells[0].attrs) > 1:
						if 'Next' in cells[0].text:
							carry_on = True
						break
					market_share = float(cells[2]	.text.replace('%',''))/100
					domains = cells[3].text
					query = "INSERT INTO HostingProviders\
							(HostName,Country,MarketShare,Domains) \
							VALUES('%s',%d,%f,'%s');\n" 
					% (cells[1].text, u[1], market_share,domains)
					f.write(query)
			if carry_on:
				print "About to sleep for 5 seconds"
				time.sleep(5)			
				i+=1
			else:
				break		