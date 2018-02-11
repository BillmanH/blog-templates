from boto.s3.connection import S3Connection
from boto.s3.key import Key
import yaml
import time
import pandas as pd

conn = S3Connection()
mybucket = conn.get_bucket('flaskgame') #my s3 bucket was created for the game that I'm working on. I'm recycling that code for aws and the name is not changable.


articles = [x for x in mybucket.list() if ("blog" in x.name)&(x.name!="blog/")&(('.html' in x.name)|('.json' in x.name))] #only blogs, not the directory

blogList = []
for art in articles:
	if '.json' in art.name:
		j = yaml.load(art.get_contents_as_string())
		name = j['title']
		articleID = j['articleID']
		articleID = articleID.lower()
		try:  #TODO I had a datevalue that changed from one to the other. I'll fix it at some other time.
			date = time.strptime(j['date'], "%d/%m/%Y")
		except:
 			date = time.strptime(j['date'], "%m/%d/%Y")
		dateStr = j['date']
		blogList.append({'name':name,'date':date,'dateStr':dateStr,'articleID':articleID,"type":"json"})
	#HTML is from JupyterNotebooks, and are loaded differently:
	if '.html' in art.name:
		date = time.strptime(art.last_modified,"%Y-%m-%dT%H:%M:%S.%fZ")#2012-03-13T03:54:07.000Z
		name = str(art.name)
		name = name.replace("+"," ")
		name = name.replace("blog/","")
		name = name.replace(".html","").encode('utf8')
		dateStr = art.last_modified.encode('utf8')
		articleID = str(art.name).encode('utf8')
		blogList.append({'name':name,'date':date,'dateStr':dateStr,'articleID':articleID,"type":"html"})

df = pd.DataFrame(blogList)
#TODO: sort_values was not supported in my version of Pandas. I need to upgrade. 
#df = df.sort_values(by="date",ascending=False).reset_index(drop=True)
df = df.sort(["date"],ascending=False)
df = df[["dateStr","name",'articleID','type']]

blogMenuKeys = df.T.to_dict()

k = Key(mybucket)
k.key = 'blog/' + "contentlist" #only dns compliant names!
k.set_contents_from_string(str(blogMenuKeys))

