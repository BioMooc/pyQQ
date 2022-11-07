import urllib.parse

rs = urllib.parse.urlparse('https://i.cnblogs.com:8001/post/edit/102?opt=1&active=1#footer')

print(rs)
print(rs.path) #/post/edit/102
print( rs.path.startswith("/post/edit") )
print(rs.port)