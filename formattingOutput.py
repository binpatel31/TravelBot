
def more(text):
	# split-up
	
	if(type(text)=='str'):
		ts = text.split("\n")
	else:
		ts = text
	ls = len(ts)
	if(ls<15):
		return text
	else:
		l = int(ls*0.3)
		t = ts[:l]
		ext = ts[l:]
		#####
		return "<p>"+''.join(t)+"<span name=\"dots\" style=\"display:inline\">...</span><span name=\"more\" style=\"display:none\">"+''.join(ext)+"</span><br><button onclick=\"readMore()\" name=\"myBtn\" >Read more</button></p>"
		
#def comprehend(text):
	