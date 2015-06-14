import sys
from BeautifulSoup import BeautifulSoup
import time
from datetime import datetime
sys.path.insert(0,'..')
import Log


from URLGetter import URLGetter
ug = URLGetter()

Log.makeLogger(True)

def getReleaseNotes(version):
	html = ug.request('http://www.mozilla.org/en-US/firefox/%s/releasenotes/' % version)['html']		
	soup = BeautifulSoup(html)
	text = soup.find('div', id="main-feature").find('p').text
	print "%s\t%s" % (version, text)
	time.sleep(3)

def getDates():
	with open('firefox.html','r') as f:
		html = f.read()
		soup = BeautifulSoup(html)


		soupy = soup.find('div', id="main-content").find('ol').findAll('li')
		for li in soupy:
			version = li.text		
			ol = li.ol
			#print "version: %s length: %d" % (version, len(li))
			version = ""
			if ol == None:
				version = li.text
			else:
				version = li.strong.text
			if int(version.split('.')[0]) < 9:
				print "%s Doing it" % version
				getReleaseNotes(version)
				return



def getStatements():
	with open('releasedates.txt', 'r') as f:
		for line in f:
			#print line
			version = line.split("\t")[0]
			date = line[line.index("\t"):].strip()
			date = datetime.strptime(date, '%B %d, %Y').strftime("%Y-%m-%d %H:%M:%S")
			print "INSERT INTO Browsers(BrowserName, BrowserVersion, ReleaseDate) VALUES('%s', '%s', '%s')" % ('Firefox', version, date)


getDates()




		

