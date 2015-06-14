import os
import re
import time
def parse_file_versions(list_of_files, parent, already_done):
	'''
	Returns a list of versions the file has information on
	Modifies the files so that the market share is an accurate representation
	e.g.45% of 30% rather than 30%
	'''
	#print "Parameters: list_of_files: %s parent: %s already_done: %s" % (list_of_files,parent,already_done)

	new_list = []
	cms = ''
	filename = ''
	for lof in list_of_files:
		li = lof.keys()[0]
		adjusted_value = lof[li]
		cms = li.split('|')[0]
		filename = li.split('|')[1]		
		if filename in already_done:
			continue
		already_done.append(filename)
		if(os.path.exists('CMS/%s/%s.txt' % (cms,filename))):			
			if not filename == parent:			
				#If this is running, then the parent is obsolete
				#Unless it's the top version
				print "filename: %s parent: %s" % (filename,parent)
				with open('CMS/%s/%s.txt' % (cms,parent), 'r+') as f:
					text = f.read()
					f.seek(0)
					if not text[0] == '/':
						f.write("%s\n%s\n%s" % ('/*', text, '*/'))
						f.truncate()
			with open('CMS/%s/%s.txt' % (cms,filename), 'r+') as txt:		
				txt_list = txt.read().strip().split(';\n')
				txt.seek(0)
				sql = ''
				for t in txt_list:
					m = re.search('(Version ([0-9]*\.*)*)\', ([0-9]+\.[^ ]*)',t)					
					percent = float(m.group(3))/100					
					version_name = m.group(1)
					print "%s\tPercent: %f\tAdjusted_Value: %f\tAdjusted_Value * Percent: %f" % (version_name,percent,adjusted_value, adjusted_value * percent)
					sql += "INSERT INTO CMSVersion(CMSId,Version,Share)\nSELECT CMSId, '%s', %f FROM CMSSoftware WHERE Name = '%s'\n" % (version_name, adjusted_value * percent, cms)
					#if not version_name in already_done:						
					new_list.append({"%s|%s" % (cms,version_name) : adjusted_value * percent})
			
			
						#print str(new_list)
						#print str(already_done)
				txt.write(sql)
				txt.truncate()	
				parse_file_versions(new_list,filename, already_done)
		
				#print str(new_list)
	
	


already_done = []

#parse_file_versions([{'Joomla|Joomla' : 1}], 'Joomla', already_done)



files_to_process = []
for d in os.listdir('CMS'):
	if(os.path.exists('CMS/%s/%s.txt' % (d,d))):
		#print 'CMS/%s/%s.txt' % (d,d)
		files_to_process.append([{'%s|%s' % (d,d):1}])

for f in files_to_process:
	cms = f[0].keys()[0].split('|')[0]
	print cms
	parse_file_versions(f,cms,already_done)

with open('new_sql.txt', 'a') as new_file:
	for cms in os.listdir('CMS'):
		for f in os.listdir('CMS/%s' % cms):
			with open('CMS/%s/%s' % (cms,f)) as sql_file:
				sql = sql_file.read()
				if not sql[0:2] == '/*':
					new_file.write(sql)
