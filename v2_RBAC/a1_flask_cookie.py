from flask import Flask, make_response, request, jsonify

app = Flask(__name__)

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
        <a class="large" href="/index" target="_blank">View cookies</a> <br>
        <a class="large" href="/set_cookie" target="_blank">set cookies</a><br>
        <a class="large" href="/delete/pkg" target="_blank">delete cookies:pkg</a><br>
    """
    return make_response(style + links);


# del
@app.route('/delete/<cname>')
def delete(cname):
    resp = make_response("delete cookie:"+cname)
    resp.delete_cookie(cname)
    return resp


# list all
@app.route("/index")
def index():
    cookie = request.cookies.to_dict()
    i=0;
    html="<ol class=show>"
    li=""
    for k in cookie:
        i+=1
        li = f"<li><b>{k}:</b> {cookie[k]}</li>\n" + li
    html +=style + li+"</ol>"
    return make_response(html);




# set
@app.route('/set_cookie')
def hello_world():
    resp = make_response("success: set 3 cookies")
    resp.set_cookie("name", "python3")
    resp.set_cookie("pkg", "Flask")
    resp.set_cookie("auther", "Tom", max_age=60) # second
    return resp



if __name__ == '__main__':
    #app.run()
    app.run(host="0.0.0.0", port=5000, debug=True)

# $ python3 a1_flask_cookie.py 
# http://y.biomooc.com:5000/