# An instant messenger using python3

## v1_Socket: basic py socket


## v2_RBAC: access control, using Sqlite + Flask

```
	a1 cookie: resp.set_cookie("name3", "jerry", max_age=7200)
		在 set-cookie 中可以用 max_age, expires 来设置 cookie 的有效期，
		其中 max_age 是以秒为单位的，expires 是时间戳或者以 datetime 格式对象数据
		* 获取：request.cookies.get(key, '默认值')
		* 设置：resp.set_cookie(key, value, max_age=整数)
		* 删除：resp.delete_cookie(key)

	a2 session:
		* 获取：session.get(key, '默认值')
		* 设置：
			session.permanent = True
    		session[key] = value  
		* 删除：
			指定删除：session.pop(key, None)
			清空所有：session.clear()
	a3 Sqlie3: db functions
	a4 get path from url using urlparse
	a5 use hashlib to encode passwd

	b1 for a user name, get permission
	b2 b1+flask



```





