import csv
from ml_curation_app import db
from flask import Blueprint, render_template ,request, redirect, url_for
from ml_curation_app.services.ml_feed import get_sorted_posts, get_posts, get_single_blog, get_subscriptions
from ml_curation_app.models import Post , Blog
from sqlalchemy.orm import load_only
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# cosine유사도 계산용
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

main_route_bp = Blueprint('main', __name__)


class NameForm(FlaskForm):
    name = StringField('Search Keyword!', validators=[DataRequired()])
    submit = SubmitField('Submit')

# methods = ['GET']

@main_route_bp.route('/',methods =['GET','POST'])
def index():
    """
	기본 Endpoint 만들기
    names = get_names(ACTORS)
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        name = form.name.data
        if name.lower() in names:
            # empty the form field
            form.name.data = ""
            id = get_id(ACTORS, name)
            # redirect the browser to another route and template
            return redirect( url_for('actor', id=id) )
        else:
            message = "That actor is not in our database."
    return render_template('index.html', names=names, form=form, message=message)


    result = []
    posts = db.session.query(Post.title, Post.pub_date,Post.blog_name,Post.body,Post.post_link).limit(8)
    for row in posts:
        result.append(row)
    
    return render_template('search.html',data=result)
    """
    posts = db.session.query(Post.title, Post.pub_date,Post.blog_name,Post.body,Post.post_link).all()
    res = []
    for row in posts:
        res.append(row)
   
    final = [] # 최종 검색결과 넣을 리스트
   
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        title = form.name.data # 입력받은 값
        for row in res:
            if title in row[0]:
                final.append(row)
                # redirect(url_for('.get_result', data=final))
        return render_template('search_trend.html',data=final)
    else:
        message = "the keyword in not in database"

    return render_template('about.html',form=form,message=message )

""" 
@main_route_bp.route('/feeds')
def get_feeds():
    #db.session.query(Record).filter_by(Record.value>10).all()
    #res = Record.query.filter_by(Record.value>10)
    page_title = 'Today\'s Posts from all feeds'
    posts = get_posts()
    my_posts = get_sorted_posts(posts)
    res = db.session.query(Post).all()
    
    #render_template('filter_search.html', my_posts=my_posts, page_title=page_title)

    return res """



# 현재 결과 return 해주는 함수

@main_route_bp.route('/result')
def get_result(): 
    #f_title = db.session.query(Post).limit(5)
    """
    https://docs.sqlalchemy.org/en/14/orm/loading_columns.html
    https://stackoverflow.com/questions/11530196/flask-sqlalchemy-query-specify-column-names
    """
    #result = db.session.query(Post).options(load_only('title', 'pub_date','blog_name',"body",'post_link'))
    result = []
    posts = db.session.query(Post.title, Post.pub_date,Post.blog_name,Post.body,Post.post_link).limit(10)
    for row in posts:
        result.append(row)
    
    return render_template('search_trend.html',data=result)


"""

data = [('Facebook', 750, True),
        ('Alphabet', 1100, True),
        ('Amazon', 1700, True),
        ('Apple', 2100, False),
        ('Microsoft', 1750, False)]

df = pd.DataFrame(data, columns=['Name', 'M-cap', 'Internet Companies'])
"""


# 추전 함수
@main_route_bp.route('/recommendation/', defaults = {'word' : '3 Reasons Why You Should Use Linear Regression Models Instead of Neural Networks'})
@main_route_bp.route('/recommendation/<word>')
def get_recommend(word): 
    #f_title = db.session.query(Post).limit(5)
    """
    """
    #result = db.session.query(Post).options(load_only('title', 'pub_date','blog_name',"body",'post_link'))
    result = []
    posts = db.session.query(Post.title, Post.pub_date,Post.blog_name,Post.post_link).limit(10)
    for row in posts:
        result.append(row)

    df = pd.DataFrame(result, columns=['title','date','blog_name','url'])
    tfidf = TfidfVectorizer(stop_words='english')
    # title에 대해서 tf-idf 수행
    tfidf_matrix = tfidf.fit_transform(df['title'])
    # 코사인유사도 구하기
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # 인덱스 구하기
    indices = pd.Series(df.index, index=df['title']).drop_duplicates()

    # 입력한 단어 넣기
    idx = indices[word]

    #
    sim_scores = list(enumerate(cosine_sim[idx]))

    #유사도에 따른 정렬
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 가장 유사한 6개 받아오기
    sim_scores = sim_scores[1:6]
    # 6개 인덱스 가져오기
    post_indices = [i[0] for i in sim_scores]


    res=df[['title','url']].iloc[post_indices] #최종

    

    return render_template('reccomend.html', tables=[res.to_html(classes='data', header="true")])



# 지정일수만큼 피드 가져오기
@main_route_bp.route('/trend/',defaults = {'search_days' : 30})
@main_route_bp.route('/trend/<search_days>')
def dbcreate(search_days):
    # TODO 
    data = get_posts(search_days=int(search_days))
    db.drop_all(bind=None) # 테이블 삭제
    db.create_all() 
    for i in data:
        rc = Post(pub_date=i[0],
                blog_name=i[1], 
                title = i[2], 
                post_link=i[3],
                body = i[4])
        db.session.add(rc)

    db.session.commit()

    result = []
    posts = db.session.query(Post.title, Post.pub_date,Post.blog_name,Post.body,Post.post_link).limit(10)
    for row in posts:
        result.append(row)
    
    

    return render_template('search_trend.html',data=result)


@main_route_bp.route('/update')
def dbupdate():
    # TODO 
    data = get_posts(search_days=180) 
    for i in data:
        rc = Post(pub_date=i[0],
                blog_name=i[1], 
                title = i[2], 
                post_link=i[3],
                body = i[4])
        db.session.add(rc)


    db.session.commit()

    return 'Data updated!'



# 테이블 


# 데이터