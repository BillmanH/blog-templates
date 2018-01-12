from boto.s3.connection import S3Connection
from boto.s3.key import Key
import yaml
import time
import pandas as pd

conn = S3Connection()
mybucket = conn.get_bucket('flaskgame') #my s3 bucket was created for the game that I'm working on. I'm recycling that code for aws and the name is not changable.


articles = [x for x in mybucket.list() if ("blog" in x.name)&(x.name!="blog/")&('.json' in x.name)] #only blogs, not the directory

blogList = []
for art in articles:
    j = yaml.load(art.get_contents_as_string())
    name = j['title']
    articleID = j['articleID']
    articleID = articleID.lower()
    try:  #I had a datevalue that changed from one to the other. I'll fix it at some other time.
        date = time.strptime(j['date'], "%d/%m/%Y")
    except:
        date = time.strptime(j['date'], "%m/%d/%Y")
    dateStr = j['date']
    blogList.append({'name':name,'date':date,'dateStr':dateStr,'articleID':articleID})

df = pd.DataFrame(blogList)
df = df.sort_values(by="date",ascending=False).reset_index(drop=True)
df = df[["dateStr","name",'articleID']]

blogMenuKeys = df.T.to_dict()

k = Key(mybucket)
k.key = 'blog/' + "contentlist" #only dns compliant names!
k.set_contents_from_string(str(blogMenuKeys))

