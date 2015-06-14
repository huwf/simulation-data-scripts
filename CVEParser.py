'''
Keeping in case I ever need it, but I suspect this is obsolete...
'''
from BeautifulSoup import BeautifulSoup
import os
from datetime import datetime
import math

def parse_data(folder):
	#listy = ['firefox', 'internet_explorer', 'chrome', 'safari']
	listy = ['wordpress', 'drupal', 'apache', 'magneto']
	product_dict = {}

	for fi in os.listdir('CVEs'):
		if not os.path.isdir(os.path.join('CVEs', fi)):
			with open(os.path.join('CVEs', fi)) as f:
				print "Parsing %s" % fi
				soup = BeautifulSoup(f.read())
				cves = soup.findAll('entry')
				for entry in cves:
					#id = entry.find('vuln:cve-id').text
					#print "Parsing %s" % id
					cve_date = entry.find('vuln:published-datetime').text.split('T')[0]
					#datetime_cve_date = parser.parse(cve_date)
					severity = entry.find('vuln:cvss')
					if severity != None:
						severity = severity.find('cvss:base_metrics').find('cvss:score').text
					#info_list = [id, cve_date, severity]
					products = entry.find('vuln:vulnerable-software-list')
					#print vars(products)
					if products != None and float(severity) >= 9:
						products = products.findAll('vuln:product')
						for prod in products:
							product = prod.text
							split = product.split(':')
							name = split[3]
							name_version = name
							if len(split) >= 5:
								name_version = '%s_%s' % (name, split[4])

							if name in listy:
								if name_version in product_dict:
									product_dict[name_version].append(cve_date)
								else:
									product_dict[name_version] = [cve_date]
				soup.decompose()
	print product_dict
	for pd in product_dict.keys():
		
		listy = sorted(product_dict[pd])
		with open(os.path.join('CVEs', folder, '%s.csv' % pd), 'a') as f:
			for li in listy:
				f.write('%s\n' % li)
	product_dict = {}
			#print "%s\n%s" % (pd, str(product_dict[pd]))

#combine the Chrome stuff into more manageable chunks
#assumes that there is only chrome entries in the folder
# current_version = 0
# version_dict = {current_version: []}
# for fi in os.listdir(os.path.join('CVEs', 'browsers')):
# 	if not os.path.isdir(fi) and '_' in fi and '.' in fi:
# 		version = fi.split('_')[1].split('.')[0]
# 		#print version
# 		if version == current_version:
# 			version_dict[current_version].append(fi)
# 		else:
# 			version_dict[version] = [fi]
# 			current_version = version

# for v in version_dict.keys():
# 	print "%s\n%s" % (v, str(version_dict[v]))
# 	with open(os.path.join('CVEs', 'browsers', 'chrome', 'chrome_%s' % v), 'a') as f:
# 		for li in version_dict[v]:
# 			with open(os.path.join('CVEs', 'browsers', li)) as fi:
# 				text = fi.read()
# 				f.write(text)

def regression(filename, folder):
	with open(os.path.join('CVEs', folder, filename)) as f:
		prev_date = None
		i = 1
		days = []
		y_values =  []
		for line in f.readlines():
			y_values.append(i)
			line = line.strip()
			datey = datetime.strptime(line, '%Y-%m-%d')
			if i == 1:				
				days.append(0)
			else:						
				delta = datey - prev_date
				days.append(delta.days + days[len(days) - 1])
			prev_date = datey
			i += 1


		#print days

	n = len(days)
	if n == 1:
		return [0,0]

	a = 0
	for i in range(0,len(days)):
		a += (days[i] * y_values[i])
	a = a * n


	b = sum(days) * sum(y_values)

	c = 0
	for x in days:
		x = math.pow(x,2)
		c += x
	c = c  * n

	d = math.pow(sum(days),2)
	try:
		m = (a-b)/(c-d)
	except:
		#die silently!
		return [0,0]

	e = sum(y_values)
	f = m * sum(days)
	c = (e - f)/n

	print "f(x) = %fx + %f" % (m,c)
	return [m,c]


def more_regression_stuff(folder):
	slopes = []
	intercepts = []
	for fi in os.listdir(os.path.join('CVEs', folder)):
		if not os.path.isdir(fi):
			slope_intercept = regression(fi,folder) 
			if not slope_intercept[0] == 0 and not slope_intercept[1] == 0:
				slopes.append(slope_intercept[0])
				intercepts.append(slope_intercept[1])

	print slopes,intercepts

	mean_slope = sum(slopes) / len(slopes)
	mean_intercept = sum(intercepts) / len(intercepts)

	print "Mean f(x) = %fx + %f" % (mean_slope, mean_intercept)

#parse_data('server')
#more_regression_stuff('server')


#	print days




more_regression_stuff('2013')

