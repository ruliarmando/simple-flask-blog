from flask import Blueprint, render_template, request, make_response, current_app, url_for
from flask.ext.login import login_required
from app.shared.models import Category, Post


frontend = Blueprint('frontend', __name__)


@frontend.context_processor
def ctx_processor():
	categories = Category.query.all()
	categories_right = categories[:len(categories)/2]
	categories_left = categories[len(categories)/2:]
	
	return {
		'categories_left': categories_left,
		'categories_right': categories_right
	}


@frontend.route('/')
def index():
	page = int(request.args.get('page', 1))
	posts = Post.query.order_by(Post.date.desc()).paginate(page, 10)
	return render_template('index.html', posts=posts)


@frontend.route('/post/<int:id>')
def post(id):
	post = Post.query.get_or_404(id)
	return render_template('post.html', post=post)


@frontend.route('/about')
def about():
	return render_template('about.html')


@frontend.route('/category/<int:id>')
def category(id):
	category = Category.query.get_or_404(id)
	posts = Post.query.filter_by(category_id=id).all()
	return render_template('category.html', category=category, posts=posts)

@frontend.route('/search')
def search():
	q = request.args.get('q')
	posts = Post.query.filter_by(title=q).order_by(Post.date.desc()).all()
	return render_template('search.html', posts=posts)


@frontend.route('/upload', methods=['POST'])
@login_required
def upload():
	import os
	error = url = ""
	callback = request.args.get('CKEditorFuncNum')
	
	if request.method == 'POST' and 'upload' in request.files:
		image = request.files['upload']
		filepath = os.path.join(current_app.static_folder, 'uploads', image.filename)
		dirname = os.path.dirname(filepath)
		
		if not os.path.exists(dirname):
			try:
				os.makedirs(dirname)
			except:
				error = 'ERROR_CREATING_DIR'
		elif not os.access(dirname, os.W_OK):
			error = 'ERROR_DIR_NOT_WRITEABLE'

		if not error:
			image.save(filepath)
			url = url_for('static', filename="%s/%s" % ('uploads', image.filename))
		else:
			error = 'ERROR_POST'

		res = """<script type="text/javascript">
					window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
				 </script>""" % (callback, url, error)

	 	response = make_response(res)
	 	response.headers['Content-Type'] = 'text/html'
	 	return response