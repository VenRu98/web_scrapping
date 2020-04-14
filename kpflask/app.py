# app.py
from flask import Flask, render_template, request
app=Flask(__name__,template_folder='page')

@app.route('/send',methods=['GET','POST'])
def send():
    if request.method == 'POST':
        age=request.form['age']
        return render_template('age.html',age=age)
    return render_template('index.html')
   # return "<h1>HELLO</h1>"
app.run()
# if __name__=="__main__":
#     app.run()