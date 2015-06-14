from BeautifulSoup import BeautifulSoup
import os
from datetime import datetime
import math



def parse_data(folder):	
	#Manually substitute the software to search for
	listy = ['firefox', 'internet_explorer', 'chrome']

	for fi in os.listdir('CVEs'):
		running_total = 0			
		if ('2013' in fi or '2012' in fi or '2014' in fi) and 'xml' in fi:#not os.path.isdir(os.path.join('CVEs', fi)):
			for li in listy:
				with open(os.path.join('CVEs', fi)) as f:
					cve_dict = {}
					print "Parsing %s" % fi
					soup = BeautifulSoup(f.read())
					cves = soup.findAll('entry')
					for entry in cves:
						#id = entry.find('vuln:cve-id').text
						#print "Parsing %s" % id
						cve_date = entry.find('vuln:published-datetime').text.split('T')[0]

						products = entry.find('vuln:vulnerable-software-list')
						if products == None:
							continue
						products = products.findAll('vuln:product')						
						relevant_product = False

						for prod in products:
							product = prod.text
							split = product.split(':')
							name = split[3]
							if name == li:#in listy:
								relevant_product = True
								break
						severity = entry.find('vuln:cvss')
						if severity != None:
							severity = severity.find('cvss:base_metrics').find('cvss:score').text
							if float(severity) >= 8 and relevant_product:
								if cve_date not in cve_dict:
									cve_dict[cve_date] = 1
								else:
									cve_dict[cve_date] += 1
									running_total += 1
				soup.decompose()#Think this gets around the MemoryError
				with open(os.path.join('CVEs', '%sCVEs.csv' % li), 'a') as f:
					for c in cve_dict.keys():
						f.write("%s,%s\n" % (c, cve_dict[c]))


parse_data('')
