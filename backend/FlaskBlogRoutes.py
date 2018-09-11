import yaml
from flask import Blueprint, render_template,request
from wtforms import Form, TextField, validators
import BOTO_BL as bbto

blog = Blueprint('blog', __name__, template_folder='templates')
adhoc = Blueprint('adhoc', __name__, template_folder='templates')
topicModels = Blueprint('topicModels', __name__, template_folder='templates')

blogroutes = [blog,
		adhoc,
		topicModels]

@blog.route('/blog')
def blogTemplate():
	c = request.args.get('c')
	t = request.args.get('t')
	if t == "json":
		blogTemplate = bbto.getBlogArticle(c)
		return render_template('blogs/blog_template_json.html',blogContent=blogTemplate,article=c)
	if t == "html":
		try:
			blogTemplate = bbto.getJupyterBlog(c)
		except:
			try:
				c = c.replace(" ","+")
				blogTemplate = bbto.getJupyterBlog(c)
			except:
				return c + " is an invalid blog article."
		article = c.replace("blog/","")
		article = article.replace(".html","")
		return render_template('blogs/blog_template_jpyter.html',blogContent=blogTemplate,article=article)
	return "invalid blog type (t)"


@adhoc.route('/ad-hoc-chart')
def adhocchart():
	return render_template('blogs/adhoc_data_viz.html')


@topicModels.route('/topicModels')
def adhoctopicModelschart():
	d = bbto.getD3Data('digTranTM.json')
	tw = bbto.getD3Data('topwords.json')
	td = bbto.getD3Data('topdocs.json')
	return render_template('blogs/topicModelViz.html',d=d,tw=tw,td=td)


	
