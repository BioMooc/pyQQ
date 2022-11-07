# db class
import sqlite3

'''写一个类打包成库，通用于储存信息的sqlite'''
'''函数返回值可优化'''
'''使用：使用'''
'''说明：1、单例模式连接数据库：避免数据库connect过多导致数据库down
        2、根据数据库增删查改性能对比，统一使用execute进行常规数据库操作
        3、且不做try操作：1、影响性能 2、若报错，外部调用无法确定问题所在，'''

class LiteDb(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance


    def openDb(self, dbname):
        self.dbname = dbname
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()

    def closeDb(self):
        '''
        关闭数据库
        :return:
        '''
        self.cursor.close()
        self.conn.close()

    def createTable(self, sql):
        '''
        example：'create table userinfo(name text, email text)'
        :return: result=[1,None]  
        '''
        self.cursor.execute(sql)
        self.conn.commit()
        result = [1, None]
        return result

    def dropTable(self, sql):
        '''
        example:'drop table userinfo'
        :param sql:
        :return:result=[1,None]
        '''
        self.cursor.execute(sql)
        self.conn.commit()
        result = [1, None]
        return result

    def executeSql(self, sql, value=None):
        '''
        执行单个sql语句，只需要传入sql语句和值便可
        :param sql:'insert into user(name,password,number,status) values(?,?,?,?)'
                    'delete from user where name=?'
                    'updata user set status=? where name=?'
                    'select * from user where id=%s'
        :param value:[(123456,123456,123456,123456),(123,123,123,123)]
                value:'123456'
                value:(123,123)
        :return:result=[1,None]
        '''

        '''增、删、查、改'''
        if isinstance(value,list) and isinstance(value[0],(list,tuple)):
            for valu in value:
                self.cursor.execute(sql, valu)
            else:
                self.conn.commit()
                result = [1, self.cursor.fetchall()]
        else:
            '''执行单条语句：字符串、整型、数组'''
            if value:
                self.cursor.execute(sql, value)
            else:
                self.cursor.execute(sql)
            self.conn.commit()
            result = [1, self.cursor.fetchall()]
        return result





# only need to exe once, after del  db file.
def init_tables(filename):
    db=LiteDb()
    db.openDb(filename)
    db.executeSql("""
create table if not exists `user` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `username` varchar(50) unique,
  `passwordHash` TEXT NOT NULL,
  active int DEFAULT 1,
  `desc` text
);
""")
    db.executeSql("""
create table if not exists `role` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `title`  varchar(75) unique NOT NULL,
  active int DEFAULT 1,
  `desc` text
);
""")
    db.executeSql("""
create table if not exists `node` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `title` varchar(75) unique NOT NULL,
  active int DEFAULT 1,
  `desc` text
);
""")
    db.executeSql("""
create table if not exists `auth_user_role` (
  `uid` INTEGER NOT NULL,
  `rid` INTEGER NOT NULL,
  PRIMARY KEY (`uid`,`rid`)
);
""")
    db.executeSql("""
create table if not exists `auth_role_node` (
  `rid` INTEGER NOT NULL,
  `nid` INTEGER NOT NULL,
  PRIMARY KEY (`rid`,`nid`)
);
""")
    db.executeSql("""
insert into node(title) values('/role/add'), ('/role/del'), ('/role/edit'), ('/role/disable'), ('/role/enable'), ('/node/add'), ('/node/del'), ('/node/edit'), ('/node/disable'), ('/node/enable'), ('/user/add'), ('/user/del'), ('/user/edit'), ('/user/disable'), ('/user/enable'), ('/post/add'), ('/post/del'), ('/post/edit'), ('/post/disable'), ('/post/enable');
""")

    db.executeSql("""
insert into role(title) values('root'), ('admin'), ('common');
""")

    db.executeSql("""
insert into user(username, passwordHash) values('Robin', 'e10adc3949ba59abbe56e057f20f883e'), ('Lucy', 'e10adc3949ba59abbe56e057f20f883e'), ('Tom1', 'e10adc3949ba59abbe56e057f20f883e');
""")

    db.executeSql("""
insert into auth_user_role values(1,1), (1,2), (2,2), (3,3);
""")

    db.executeSql("""
insert into auth_role_node values (1,1), (1,2), (1,3), (1,4), (1,5), 
(1,6), (1,7), (1,8), (1,9), (1,10), (1,11), (1,12), (1,13), (1,14), (1,15),
(2,11), (2,12), (2,13), (2,14), (2,15), (2,19), (2,20),
(3,16), (3,17), (3,18), (3,19), (3,20);
""")

    db.closeDb()
    print("Init table structure and data success!");


def executeSql(filename, sql):
    db=LiteDb()
    db.openDb(filename)
    rs=db.executeSql(sql)
    db.closeDb()
    if rs[0]==1:
        return rs[1]



def get_permission_list(filename, uid):
    db=LiteDb()
    db.openDb(filename)
    rs=db.executeSql(f"""
select username, a.id as uid, b.title, d.title as nodename 
	from user a,role b, auth_user_role c, node d, auth_role_node e 
	where a.id==c.uid and b.id==c.rid and 
	e.rid==b.id and e.nid==d.id and a.id=='{uid}' and
    a.active==1 and b.active==1 and d.active==1;
""")
    if rs[0]==1:
        #print(rs[1])
        for node in rs[1]:
            #print(node)
            pass
    db.closeDb()
    return rs[1]

# input the output list of get_permission_list(file, uid)
def get_role_list(nodes):
    roles=[]
    for node in nodes:
        uid=node[2]
        if uid not in roles:
            roles.append(uid)
    return roles


def get_user_info(filename, uname):
    sql=f"select * from user where username=='{uname}'"
    #print("sql=", sql)
    return executeSql(filename, sql)




def calc_md5(passwd):
	import hashlib
	md5 = hashlib.md5()
	md5.update(passwd.encode('utf-8'))
	return md5.hexdigest()