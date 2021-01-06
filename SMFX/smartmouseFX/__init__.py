from flask import *
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ndxxxu/Desktop/smartmouseFX/smartmouseFX.db'
db = SQLAlchemy(app)
app.secret_key = "forex"
login_manager = LoginManager()
login_manager.login_view = 'adminconsole'
login_manager.init_app(app)
class ForexEdu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))

    @login_manager.user_loader
    def load_user(admin_id):
        return Admin.query.get(int(admin_id))


@app.route('/')
def index():
    posts = ForexEdu.query.all()
    return render_template('index.html', posts=posts)

@app.route('/edu')
def edu():
    posts = ForexEdu.query.all()
    return render_template('forexEdu.html', posts=posts )
@app.route('/post/<int:post_id>')
def post(post_id):
    post = ForexEdu.query.filter_by(id=post_id).one()
    date_posted = post.date_posted.strftime('%B %d, %Y ')
    return render_template('posts.html', post=post, date_posted=date_posted )

@app.route('/r&r')
def rate_review():
    return render_template('R&R.html')

@app.route('/s&sp')
def signal_signal_plans():
    return render_template('S&SP.html')

@app.route('/admin101')
def login():
    return render_template('adminlogin.html')

@app.route('/admin101', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')


    user = Admin.query.filter_by(username=username).first()

    if not user or not (user.password, password):
        flash('Please check your login details and try again')
        return redirect(url_for('admin101'))
    return render_template('adminconsole.html')

@app.route('/adminconsole')
@login_required
def adminconsole():
    return render_template('adminconsole.html')

@app.route('/adminconsole', methods=['POST'])
@login_required
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = ForexEdu(title=title, subtitle=subtitle,author=author,content=content, date_posted=datetime.now())
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('edu'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

def getApp():
    return app

if __name__ == '__main__':
    app.run()