import hashlib

md5 = hashlib.md5()
md5.update( '123456'.encode('utf-8'))
print(md5.hexdigest())


# as function
def calc_md5(passwd):
	import hashlib
	md5 = hashlib.md5()
	md5.update(passwd.encode('utf-8'))
	return md5.hexdigest()

print( calc_md5("123456") ) #e10adc3949ba59abbe56e057f20f883e
print( calc_md5("123456" + "xjo,jw!e56.f") ) #add salt

# using shell
# $ echo -n "123456" | md5sum | cut -f 1 -d " "
# e10adc3949ba59abbe56e057f20f883e