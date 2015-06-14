from BeautifulSoup import BeautifulSoup
import sys
sys.path.insert(0, '..')
from URLGetter import URLGetter
import time

ug = URLGetter()
#Already got the results for Page 1 to test, so lets do it for the rest
for i in range(2,25):
	url = 'http://www.webhosting.info/webhosts/globalstats/?ob=HC\&oo=DESC\&pi=%d' % i
	html = ug.request(url)['html']
	soup = BeautifulSoup(html)
	rows = soup.find(id="AutoNumber7").find('table').findAll('tr')
	
	for tr in rows:
		if(tr.find('td') != None):
			cells = tr.findAll('td')
			country_url = cells[0].find('a')					
			country = country_url.text
			#Having a > means that it's linking to the next page
			#Don't want to try and add that into the database!
			if "&lt;" in country:
				break
			amount_of_companies = int(cells[2].text.replace(',',''))
			print "INSERT INTO Countries(Country, Url) \
				VALUES('%s', '%s');" % (country, country_url['href'])
			print "INSERT INTO HostPerCountry(CountryId, Amount)\nSELECT CountryId, %d \
			FROM Countries WHERE Country = '%s'" % (amount_of_companies, country)
	#Robots was a 404 but lets be nice...
	print "About to sleep for 10s..."
	time.sleep(10)			


#Don't think I need this...
# with open('hosts-share.html', 'r') as f:
# 	html = f.read()
# 	soup = BeautifulSoup(html)
# 	rows = soup.find(id="AutoNumber7").find('table').findAll('tr')
	
# 	for tr in rows:
# 		if(tr.find('td') != None):
# 			cells = tr.findAll('td')#.find('a').text
# 			country_cell = cells[0]
# 			print country_cell.attrs
# 			print len(country_cell.attrs)

# 			if "&lt;" in cells[0]:
# 				break
