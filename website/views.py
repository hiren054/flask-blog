from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user
from flask_login import login_required
from .models import Post
from website import db


views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home(): 
    posts = Post.query.order_by(Post.created.desc()).all()
    # page = request.args.get('page', 1,type=int)
    # posts = Post.query.order_by(Post.created.desc()).paginate(page=page, per_page=2)
    return render_template('home.html',posts = posts,user=current_user)


@views.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('blog/post.html', post=post,user=current_user)


@views.route('/new', methods=['GET','POST'])
@login_required 
def create():
    if request.method == 'POST' :
        title = request.form.get('title')
        content = request.form.get('content')
        error = None

        if not title :
            error = "Title required!"

        if not content :
            error = "Content required!"

        if error is not None :
            flash(error)
        else :
            post = Post(title=title, content=content, author=current_user)
            db.session.add(post)
            db.session.commit()
            error = "Your Post has been created!!"
            flash(error)
            return redirect(url_for('views.home'))
    return render_template('blog/create.html', user=current_user)



@views.route('/post/<int:id>/update', methods= ['GET','POST'])
@login_required
def update_post(id):
    error = None
    post = Post.query.get_or_404(id)
    if post.author != current_user :
        abort(403)
    if request.method == 'POST' :
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        if error is None :
            error = "Post Updated Successfully!"
            db.session.commit()
            flash(error)
            return redirect(url_for('views.home'))
    return render_template('blog/update.html', post=post, user=current_user)


@views.route('/delete/<int:id>', methods= ['GET','POST'])
@login_required
def delete_post(id):
    error = None
    post = Post.query.get_or_404(id)
    if post.author != current_user :
        abort(403)
    if error is None :
        db.session.delete(post)
        db.session.commit()
        error = "post deleted!"
        flash(error)
        return redirect(url_for('views.home'))