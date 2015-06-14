from BeautifulSoup import BeautifulSoup
import sys
sys.path.insert(0, '..')
from URLGetter import URLGetter
import time
import os

ug = URLGetter()
def get_table_information(table, cms_param, filename = None):
	print "get_table_information"
	urls = []
	for tr in table:
		cms = ''
		th = tr.find('th')
		if th != None:
			if th.find('a') != None:
				a = tr.find('th').find('a')
				cms = a.text				
				urls.append({cms:a['href']})
				cms = a.text
			
			#Graph table embedded inside the other table
			tables = tr.find('td').findAll('table')
			#print "Stay classy"
			if len(tables) > 0:
				#print "I'm Ron Burgundy?"
				table = tables[0]
				share_text = table.find('tr').findAll('td')[1].text.replace('%','')
				share = 0
				if not 'less than' in share_text:
					share = float(share_text)
				if filename != None:
					#print "Man, that escalated quickly!"
					with open('CMS/%s/%s.txt' % (cms_param.replace(':',''), filename.replace(':','')), 'a') as f:						
						query = "INSERT INTO CMSVersion(CMSId,Version,Share)\nSELECT CMSId, '%s', %f FROM CMSSoftware WHERE Name = '%s';\n" % (cms,share,cms_param)						
						f.write(query)
						#print query
	#print urls
	return urls




def algorithm(urls, counter, already_done, cms, only_one_table = False):		
	print "Calling algorithm(%s,%d,%s)" % (str(urls[0]), counter,only_one_table)
	already_done.append(urls)
	for url in urls:		
		filename = url.keys()[0]
		print "Algorithm loop(%s,%d,%s)" % (url[filename], counter,only_one_table)			
				
		html = ug.request(url[filename])['html']
		soup = BeautifulSoup(html)
		table = None
		if soup.find(attrs={'class' : 'bars'}) == None:
			return
		if(only_one_table):
			table = soup.find(attrs={'class' : 'bars'}).findAll('tr')
		else:
			tables = soup.findAll(attrs={'class' : 'bars'})
			#print tables
			if len(tables) > 1:				
				table = tables[1].findAll('tr')
				#print table
			else:
				return
		print "CMS: %s filename: %s" % (cms,filename)
		urls = get_table_information(table, cms, filename)
		if urls in already_done:
			return
		counter += 1		
		print "About to sleep for 10s"
		time.sleep(10)
		algorithm(urls, counter, already_done, cms, False)





#Need to generate the CMSList.txt
def get_original_list():
	cms_list = []
	with open('w3techs.html', 'r') as f:
		html = f.read()
		soup = BeautifulSoup(html)
		table = soup.find(attrs={'class' : 'bars'}).findAll('tr')
		for tr in table:
			#print tr
			cell = tr.find('th')
			if cell != None and cell.find('a') != None:
				a = cell.find('a')
				print a['href'], a.text
				cms_list.append({a.text : a['href']})

	return cms_list


with open('CMSList.txt', 'r') as f:
	urls = get_original_list()
	for url in urls:
		#HACK
		u = [url]
		print "In the main list again..."
		already_done = []
		cms = url.keys()[0]
		os.makedirs(os.path.join('CMS',cms.replace(':','')))
		algorithm(u, 0, already_done, cms, True)
		print "come out the end of the algorithm"