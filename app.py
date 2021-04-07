from typing import List
from flask import Flask, render_template, request, redirect, url_for
from models import db, User, Article
from flask_migrate import Migrate
from forms import ArticleForm
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db?check_same_thread=False'
app.config['SECRET_KEY'] = 'you-will-never-guess'
db.app = app
db.init_app(app)
migrate = Migrate(app, db)
Bootstrap(app)


@app.route('/')
def homepage():
    articles: List[Article] = Article.query.all()
    return render_template("index.html", title='Главная страница', articles=articles)


@app.route('/search')
def search_article():
    q = request.args.get("q", "")
    articles: List[Article] = Article.query.filter(Article.title.like(f"%{q}%") | Article.body.like(f"%{q}%")).all()
    return render_template("index.html", title='Главная страница', articles=articles)


@app.route('/articles/<int:article_id>')
def get_article(article_id):
    article: Article = Article.query.filter_by(id=article_id).first()
    return render_template('article.html', article=article)


@app.route('/articles/new', methods=["GET", "POST"])
def new_article():
    form = ArticleForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        is_verified = form.is_verified.data
        article = Article(title=title, body=body, is_verified=is_verified, user=User.query.first())
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("get_article", article_id=article.id))
    return render_template('new_article.html', form=form)


@app.route('/articles/<int:article_id>/edit', methods=["GET", "POST"])
def edit_article(article_id):
    form = ArticleForm()
    article = Article.query.filter_by(id=article_id).first()

    if form.validate_on_submit():
        article.title = form.title.data
        article.body = form.body.data
        article.is_verified = form.is_verified.data
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("get_article", article_id=article.id))

    form.title.data = article.title
    form.body.data = article.body
    form.is_verified.data = article.is_verified

    return render_template('edit_article.html', form=form)


if __name__ == '__main__':
    app.run()
