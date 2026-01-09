from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    desc=db.Column(db.String(300),nullable=False)
    created_At=db.Column(db.DateTime,default=datetime.today())

    def __repr__(self):
        return f"{self.sno} - {self.title}"


@app.route("/", methods=['GET','POST'])
def logIn():
    if request.method=="POST" :
      title=  request.form.get("title")
      desc= request.form.get("desc")
      todo=Todo(title=title,desc=desc)
      db.session.add(todo)
      db.session.commit()
    
    data=Todo.query.all()
 
    return render_template('index.html',data=data)

@app.route("/delete/<sno>")
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<sno>" , methods=['GET','POST'])
def update(sno):
    c_task=Todo.query.filter_by(sno=sno).first()
    if request.method =="POST":
        title=request.form.get("title")
        desc= request.form.get("desc")
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    return render_template('update.html', c_task=c_task)

if __name__=='__main__':
    app.run(debug=True)
    db.create_all()