import os
from b1_rbac_lib import *
from flask import Flask, make_response, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY']='12s4356'
#app.config['PERMANENT_SESSION_LIFETIME']=100  #second, default is 31 days: 3600*24*31
# the total time, whether you are active or not.

# $ python3 b1_rbac2.py
# http://y.biomooc.com:5000/user/info/2

style="""
<style>
.show li{margin-bottom: 10px;}
.show li b{color:red; margin-right:20px; }
.large{font-size: large;}
</style>
"""

db_file="backup/rbac.db"


# home page
@app.route("/")
def home():
    # check session is valid?
    if session.get("uid", '')=='':
        return redirect(url_for('login'))
    return redirect(url_for('user_info', session.get('uid')))


# login
@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method =='GET':
        html="""
        login:
        <form action="/login/" method="post">
            username <input type="input" name="username" /> <br>
            password <input type="input" name="password" /> <br>
            <input type="submit" value="submit" />
        </form>
        """
        return html
    elif request.method=='POST':
        username = request.form.get('username', '');
        password = request.form.get('password', '');
        print("From form: ", username, password)

        user_arr=get_user_info(db_file, username);
        print(user_arr)
        if len(user_arr) == 0 or calc_md5(password) != user_arr[0][2]:
            return "Error: username or password is error!";
        # write to session
        #[(2, 'Lucy', 'e10adc3949ba59abbe56e057f20f883e', 1, None)]
        uid=user_arr[0][0]
        session["username"] = username
        session["uid"] = uid
        #return f"{username} {password}"
        return redirect(url_for('user_info', uid=uid))


# logout
@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for('login'))






# user/info
@app.route("/user/info/<int:uid>")
def user_info(uid):
    # check session is valid?
    uid_session=int(session.get("uid", -1));
    if uid_session==-1:
        return redirect(url_for('login'))
    print(uid_session, uid)
    if uid_session != uid:
        return f"Invalid for <b>{session.get('username')}(uid={uid_session})</b> to view this page"

    nodes=get_permission_list(db_file, uid)
    roles = get_role_list(nodes)
    s_roles =", ".join(roles)
    links=f"""
        <title>RBAC model</title>
        <p>
            username: {nodes[0][0]}, uid:{uid}, role: {s_roles}
            | 
            <a href="/logout">logout</a>
        </p>
        <p><b>Accessible nodes: </b></p>
        <ol>
    """
    for node in nodes:
        links += f'<li><a class="large" href="{node[3]}" target="_blank">{node[3]}</a> </li>'
    links += "<ol>"
    return make_response(style + links)





# if the last is NOT an int
@app.route("/<path:subpath>")
def show_subpath2(subpath):
    # check session is valid?
    uid=session.get("uid", '')
    if uid=='':
        return redirect(url_for('login'))
    username=session.get('username', '')
    subpath = "/"+subpath
    msg = f"subpath: {subpath}"

    # check valid?
    nodes=get_permission_list(db_file, uid)
    flag=0
    for node in nodes:
        if subpath.startswith(node[3]):
            flag=1
            break
    if flag==1:
        return f"<b style='color:green;'>Valid</b> for {username}!<hr>" + msg
    else: 
        return f"<b style='color:red'>Invalid</b> for {username}! <hr>" + msg




if __name__ == '__main__':
    if not os.path.exists(db_file):
        init_tables(db_file)
    app.run(host="0.0.0.0", port=5000, debug=True)
# rs=executeSql(db_file, "select * from user where id==3;")
# print(rs)
