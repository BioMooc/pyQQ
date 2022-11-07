from flask import Flask, make_response, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY']='12s4356'
app.config['PERMANENT_SESSION_LIFETIME']=10  #second, default is 31 days: 3600*24*31
# the total time, whether you are active or not.


# usage of session: similar to python dict

style="""
<style>
.show li{margin-bottom: 10px;}
.show li b{color:red; margin-right:20px; }
.large{font-size: xx-large;}
</style>
"""

# home
@app.route("/")
def home():
    links="""
        <a class="large" href="/login" target="_blank">login (set session)</a>: should set SECRET_KEY <br>
        <a class="large" href="/index" target="_blank">index (get one session)</a>:  <br>
        <a class="large" href="/list" target="_blank">list (all session)</a>:  <br>
        <a class="large" href="/get/author" target="_blank">get one session: author</a><br>
    """
    return make_response(style + links);


# set 
@app.route("/login")
def login():
    session["author"] = "s_Tom"
    session["pkg"] = "s_Flask"
    return make_response("success: set 2 session key-value pairs")


# get one
@app.route("/index")
def index():
    name = session.get("author")
    return f" hello {name}"

# get one2
@app.route("/get/<cname>")
def getC(cname):
    val=session.get(cname,'')
    if val != "":
        return jsonify({
            'status': "success", 
            'cookie':[cname, val]
        })
    else:
        return jsonify({
            'status': 'failed',
            'cookie': [cname]
        })


# list all
@app.route("/list")
def listS():
    html="Session on this server: <pre>"
    for k in session:
        html+= f"{k}: {session[k]}\n"
    return html;



# del
@app.route("/delete/<sname>")
def delSession(sname):
    session.pop(sname)
    #del session[sname]
    #session.clear()
    return f" del session: {sname}"




if __name__ == '__main__':
    #app.run()
    app.run(host="0.0.0.0", port=5000, debug=True)

# $ python3 a2_flask_session.py 
# http://y.biomooc.com:5000/