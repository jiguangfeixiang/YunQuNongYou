Django共享局域网访问项目

在`settings.py`写

```
ALLOWED_HOSTS = ['*']`并运行`python manage.py runserver` `0.0.0.0:8000
```

注意:您可以使用任何`port`而不是`8000`。

收藏分享票数 8

EN

#### Stack Overflow用户

发布于 2021-04-19 20:32:54

解决这一问题的步骤有：

**1.**使用`http://<your ip address>`而不是https

**2.**然后在settings.py中写

代码语言：javascript

复制

```javascript
ALLOWED_HOSTS = ['*'] 
```

**3.**最终运行服务器时：

代码语言：javascript

复制

```javascript
python manage.py runserver 0.0.0.0:8000
```