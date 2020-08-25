from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from soft_deleted import SoftDeletedMixin


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/demo.sqlite'.format(
    app.root_path
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(SoftDeletedMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sex = db.Column(db.Integer)
    
    @property
    def sex_str(self):
        return '男' if self.sex else '女'

@app.before_first_request
def init_wsgi():
    db.create_all()

@app.route('/all')
def all():
    record = User.query.with_trashed
    return render_template_string('''
                                  {% for i in record %}
                                  <p>{{ i.id }} - {{ i.name }} - {{ i.delete_datetime }}</p>
                                  {% endfor %}
                                  ''', record=record)

@app.route('/trashed')
def trashed_on():
    trashed_user = User.query.only_trashed.all()
    for item in trashed_user:
        print(item.__dict__)
    return render_template_string('''
                                  <div>
                                  已软删除的用户
                                  {% for i in record %}
                                    <p>
                                    {{ i.id }} - {{ i.name }} - {{ i.sex_str }} - <a href="/{{ i.id}}/restore">恢复</a>
                                    </p>
                                  {% endfor %}
                                  </div>
                                  ''',
                                  record = trashed_user
                                  )

@app.route('/<int:id>/restore')
def restore(id):
    user = User.query.only_trashed.get(id)
    user.restore()
    db.session.commit()
    return 'restore success  <a href="/">返回首页</a>'
    

@app.route('/<int:id>/delete')
def delete(id):
    user = User.query.get(id)
    user.delete()
    db.session.commit()
    return 'delete success <a href="/">返回首页</a>'
        

@app.route('/', methods=['GET', 'POST'])
def index():
    record = User.query.all()
    for i in record:
        print(i.__dict__)
    if request.method == 'POST':
        user = User()
        user.name = request.form.get('name')
        user.sex = request.form.get('sex')
        db.session.add(user)
        db.session.commit()
    html ='''
<html>
<head></head>
<body style="margin-top: 200px;margin-left: 35%;">
<h1>正常的用户</h1> 
[<a href="/trashed">拉入回收站的用户</a>]
[<a href="/all">所有的用户</a>]
<ul>
{% for i in record %}
    <li>
        {{ i.id }} - {{ i.name }} - {{ i.sex_str }} - <a href="{{ i.id}}/delete">删除</a>
    </li>
{% endfor %}
</ul>
<form action="/" method="post">
    <div style="margin:20px">姓名:
    <input name="name" value="">
    </div>
	<div style="margin:20px">性别:
		<label><input type="radio" name="sex" value="1" checked="checked">男生</label>
		<label><input type="radio" name="sex" value="0">女生</label>
	</div>
    <div style="margin:20px">
        <input name="save" type="submit" value="保存">
    </div>
</form>
</body>
</html>
'''
    return render_template_string(html, record=record)


