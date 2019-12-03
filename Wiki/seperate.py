import os
def seperate_content(lines):
	index = []
	for i in range(len(lines)):
		line = lines[i]
		if(line[:3] == '== '):  ######
			start = i
			i += 1
			if(i>=len(lines)):
				i-=1
				end=i
			else:
				line = lines[i]
				while not (line[:3] == '== ' or i == len(lines)-1):
					i += 1
					if(i == len(lines)):
						end = i-1
						pass
					else:
						line = lines[i]
						end = i-1
			index.append((start, end))
	
	return index
def mainfun(inputfile, destination):      
	fname = inputfile   # is a file
	destination = destination       # is a folder
	file = open(fname, 'r', encoding='utf-8')
	lines = file.readlines()
	
	content_lines = seperate_content(lines)
	length=len(content_lines)

	for i in range(len(content_lines)):
		tup = content_lines[i]
		#print(str(i)+" : ", end = '')
		#print (lines[tup[0]])

	
	for j in range(length):
		#print(j)
		req = content_lines[j]
		req_data = ''
		file_name = lines[req[0]]
		file_name = file_name[3: len(file_name)-4] 
		#print("File Name:" +file_name+":" )
		for i in range(req[0]+1, req[1]+1):
			req_data += lines[i]
	
		if req_data:
			dest = open(destination + "/" + file_name + ".txt", 'w', encoding='utf-8')
			dest.write(req_data)
			dest.close()
	
	file.close()
        
