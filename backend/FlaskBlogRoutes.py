import yaml
from flask import Blueprint, render_template,request
from wtforms import Form, TextField, validators
import BOTO_BL as bbto

blog = Blueprint('blog', __name__, template_folder='templates')

blogroutes = [blog]

@blog.route('/blog')
def blogTemplate():
	c = request.args.get('c')
	t = request.args.get('t')
	if t == "json":
		blogTemplate = bbto.getBlogArticle(c)
		return render_template('blogs/blog_template.html',blogContent=blogTemplate,article=c)
	if t == "html":
		try:
			blogTemplate = bbto.getJupyterBlog(c)
		except:
			return c
	#blogTemplate = bbto.getBlogArticle(article)
	#blogTemplate = yaml.load(open('/home/ubuntu/flaskapp/templates/blogs/example_article_json.json', 'r'))
		return render_template('blogs/blog_template2.html',blogContent=blogTemplate,article=c)
	return "invalid blog type (t)"
