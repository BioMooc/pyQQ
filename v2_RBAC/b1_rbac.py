#import sqlite3
from b1_rbac_lib import *

if __name__ == '__main__':
    db_file="backup/rbac.db"
    #init_tables(db_file)
    nodes=get_permission_list(db_file, 3)
    print(nodes)
    #
    rs=executeSql(db_file, "select * from user where id==3;")
    print(rs)