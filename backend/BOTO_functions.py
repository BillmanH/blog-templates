from boto.s3.connection import S3Connection
import boto
import yaml


# This function returns a default blog article, it is set to return my first article in the event of an error.
def getBlogArticle(article):
        mybucket = conn.get_bucket('flaskgame')
        if article==None:
            defaultKey = mybucket.get_key("blog/" + "d3_backend.json")
            myKey = mybucket.get_key(defaultKey)
            content = yaml.load(myKey.get_contents_as_string())
            return content
        potentialKey = "blog/" + article + ".json"
        if potentialKey in [item.name for item in mybucket.list() if "blog/" in item.name]:
                defaultKey = mybucket.get_key("blog/" + article + ".json")
                content = yaml.load(defaultKey.get_contents_as_string())
        else:
                defaultKey = mybucket.get_key("blog/" + "d3_backend.json")
                myKey = mybucket.get_key(defaultKey)
                content = yaml.load(myKey.get_contents_as_string())
        return content

def getContentList():
	mybucket = conn.get_bucket('flaskgame')
	myKey = mybucket.get_key('blog/contentlist')
	content = yaml.load(myKey.get_contents_as_string())
	return content


