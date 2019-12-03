import wikipedia as w
import os

def grabInfo(name, path):
	name = w.search(name)[0]
	page = w.page(name)
	print("name:",page)
	if not os.path.exists(path + "/" + name):
		os.makedirs(path + "/" + name)
	FileName = path + "/" + name + "/" + "RawData" +".txt"
	fo = open(FileName, "w", encoding='utf-8')
	content = page.content
	fo.write(content)
	fo.close()
	return name