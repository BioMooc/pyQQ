
# 1. right
class Permission:
    COMMENT = 0x02
    ADMINISTER = 0x80

print(Permission.COMMENT, Permission.ADMINISTER);

# 2. role

import sqlite3

def demo1():
    #1. create db
    dbFile="backup/a1.db"
    con=sqlite3.connect(dbFile)

    #2.get cursor
    cur=con.cursor()

    #3.exec sql
    cur.execute("create table if not exists book(id primary key, name, price)")

    # insert data
    cur.execute("insert into book(id,price,name) values('003',28,'大学计算机多媒体')")
    cur.execute("insert into book(id,price,name) values (?,?,?)",("002",28,"数据库基础"))

    books=[("a1", 50, "C lang"), ("a2", 100, "rust lang")]
    cur.executemany("insert into book(id,price,name) values(?,?,?)",books)

    cur.execute("Update book set price=? where name = ?",(25,"C lang"))

    cur.execute("select * from book")
    for row in cur:
        print(row)


    #4. commit the modification
    con.commit()

    #5. close
    cur.close()
    con.close()



def demo2():
    #1. create db
    dbFile="backup/a1.db"
    con=sqlite3.connect(dbFile)

    #2.get cursor
    cur=con.cursor()

    #3.exec sql
    cur.execute("select * from book")
    for row in cur:
        print(row)

    #4. close
    cur.close()
    con.close()



def demo3():
    sql = "select * from book"
    #sql = "insert into book(id, price, name) values('a3',128,'csapp')" #rs= []
    #1. create db
    dbFile="backup/a1.db"
    con=sqlite3.connect(dbFile)

    #2.get cursor
    cur=con.cursor()

    #3.exec sql
    cur.execute(sql)
    con.commit()
    #rs=cur.fetchone()
    rs=cur.fetchall()
    #rs=cur.fetchmany(2)
    print("rs=", rs)

    print("")
    for row in rs:
        print(row)

    #4. close
    cur.close()
    con.close()




# for...else...: when break to exit for, not exe else.
def test1():
    a1=[1,2,30]
    for val in a1:
        print(val)
    else:
        print("the for ends normally.");

# isinstance
def test2():
    a1=[1,2,3]
    rs=isinstance(a1, list)
    print(a1, rs)

    #
    a2=(10,20,30)
    rs2=isinstance(a2, tuple)
    print(a2, rs2)



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

def demo4():
    db=LiteDb()
    db.openDb("backup/a1.db")

    #rs=db.executeSql("select * from book;")
    rs=db.cursor.executescript(".database")
    print(rs, "\n")

    if rs[0]==1:
        for val in rs[1]:
            print(val)
    db.closeDb()



if __name__ == '__main__':
    #demo1(); # add data
    #demo2(); #only search
    #test1(); #for...else
    #test2() #isinstance
    #demo3() #fetchall
    demo4() #test the class
