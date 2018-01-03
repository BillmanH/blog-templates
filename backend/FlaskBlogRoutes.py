import yaml
from flask import Blueprint, render_template,request
from wtforms import Form, TextField, validators

blog = Blueprint('blog', __name__, template_folder='templates')

blogroutes = [blog]

@blog.route('/blog')
def blogTemplate():
	article = request.args.get('c')
	blogTemplate = bto.getBlogArticle(article)
	#blogTemplate = yaml.load(open('/home/ubuntu/flaskapp/templates/blogs/example_article_json.json', 'r'))
	return render_template('blogs/blog_template.html',blogContent=blogTemplate,article=article)

