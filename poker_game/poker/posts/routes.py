from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, current_app)
from flask_login import current_user, login_required
from poker import db
from poker.models import Post, Game
from poker.posts.forms import PostForm, GameForm
# from poker.main import show_hand, show_winner, show_rank
from PIL import Image

posts = Blueprint('posts', __name__)


# @posts.route("/post/game", methods=['GET', 'POST'])
# @login_required
# def show_cards():
#     hands = show_hand()
#     ranks = show_rank()
#     winner = show_winner()
#     # card_image = cards_picture(url_for('static', filename='images/cards/2_of_clubs.png'))
#     # # card_image = Image.open('static/images/2_of_clubs.png')
#     # # card_image.thumbnail((150, 218))
#     form = GameForm()
#     if form.validate_on_submit():
#         game = Game(winner=form.winner.data, author=current_user)
#         db.session.add(game)
#         db.session.commit()
#         flash(f'{winner} won', 'success')
#     return render_template("create_game.html", hands=hands, ranks=ranks
#                             form=form, title="New Poker Game", legend='New Poker Game')

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))