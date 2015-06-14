from BeautifulSoup import BeautifulSoup

with open('share.html') as f:
	html = f.read()
	soup = BeautifulSoup(html)

	listy = soup.find(id='fwReportTable1').find('tbody').findAll('tr')

	browser_list = []
	TOTAL_PERCENTAGE_ACCOUNTED = 97.34
	total_share = 0.0
	for li in listy:
		td = li.findAll('td')
		i = 0		
		browser = ''
		share = ''
		for t in td:

			if i == 0:								
				browser = t.text.replace('&nbsp;', '')#.split(' ')
				if 'Microsoft Internet Explorer' in browser:
					browser = browser.replace('Microsoft Internet Explorer', 'MSIE')
				browser = browser.split(' ')
				browser_name = browser[0]
				browser_version = browser[1]
				i += 1
			else:
				if 'Proprietary' not in browser:
					#print t.text
					share = float(t.text.replace('%', ''))
					#share = share * 100				
					total_share += share/TOTAL_PERCENTAGE_ACCOUNTED
					print "INSERT INTO BrowserDistribution(BrowserName, BrowserVersion, StartingNumber) VALUES('%s','%s',%f);" % (browser_name, browser_version,total_share)
					#print "BrowserDict.Add(%f,new Browser(\"%s\",\"%s\"));" % (total_share, browser_name, browser_version)
				
				#for j in int(float(share) * 1000):

		#print 'Browser %s Share: %s' % (browser,share)
		


'''
	for li in listy:
		td = li.findAll('td')
		for t in td:
			browser = t.text
			print browser
		print '================'

'''



