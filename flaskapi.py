from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/posts/*": {"origins": "*"}})
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Temp_23@localhost/MyFirstPostgresDB'
db = SQLAlchemy(app)


class posts(db.Model):
    __tablename__ = 'posts'
    user = db.Column(db.String(), primary_key=True)
    post = db.Column(db.String(), nullable=False)

    def __init__(self, user, post):
        self.user = user
        self.post = post


@app.route('/posts', methods=['GET'])
def getPosts():
    allPosts = posts.query.all()
    res = []
    for post in allPosts:
        currPost = {}
        currPost['user'] = post.user
        currPost['post'] = post.post
        res.append(currPost)
    return jsonify(res)


@app.route('/posts', methods=['POST'])
def createPost():
    postData = json.loads(request.data)
    newPost = posts(user=postData['user'], post=postData['post'])
    db.session.add(newPost)
    db.session.commit()
    return jsonify(postData)
