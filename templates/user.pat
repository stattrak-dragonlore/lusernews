<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
	<title>User {{username}} - Luser News</title>
	<link rel="stylesheet" type="text/css" href="/css/bootstrap.css"/>
	<link rel="stylesheet" type="text/css" href="/css/lusernews.css"/>
	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js"></script>
	<script src="/js/app.js"></script>
	{% include "ga.pat" %}
  </head>
  <body>
	<div class="navbar">
	  <div class="navbar-inner">
		<div class="container">
		  <a class="brand" href="/">
			Luser News
		  </a>
		  <ul class="nav">
			<li><a href="/top">top</a></li>
			<li><a href="/latest">new</a></li>
			<li><a href="/comments">comments</a></li>
			<li><a href="/submit">submit</a></li>
		  </ul>

		  <ul class="nav pull-right">
			{% if user %}
			<li><a href="/user/{{user['username']}}">{{user['username']}} ({{user['karma']}})</a></li>
			<li class="divider-vertical"></li>
			<li><a href="/logout?apisecret={{user['apisecret']}}">logout</a></li>
			{% else  %}
			<li class="divider-vertical"></li>
			<li class="active"><a href="/login">login</a></li>
			{% endif %}

		  </ul>
		</div>
	  </div>
	</div>
	<div class="container">
	  <div class="userinfo">

		<span class="avatar">
		  <img src="{{userinfo['gravatar']}}" />
		</span>

		<span class="username">{{ userinfo['username'] }}</span>

		<pre>{{userinfo["about"]|e}}</pre>

		<div class="info">
		  <span class="ulabel">created</span> {{userinfo["created"]}} </br>
		  <span class="ulabel">karma</span> {{userinfo['karma']}} </br>
		  {% if userinfo['id'] == user['id'] %}
		  <span class="ulabel">saved news</span> <a href="/saved">{{userinfo['saved']}}</a> </br>
		  {% endif %}
		  <span class="ulabel">posted news</span> {{userinfo['posted']}} </br>
		</div>

		{% if userinfo['id'] == user['id'] %}

		<br/>
		<form name="f">
		  <label>email(not shown, used for gravatar)</label>
		  <input type="text" name="email" value="{{userinfo['email']|e}}"/> <br/>

		  <label>change password(optional)</label>
		  <input type="password" name="password"/> <br/>

		  <label>about</label>
		  <textarea class="input-xlarge" name="about" rows="4">{{userinfo['about']|e}}</textarea>	<br/>

		  <button type="submit" class="btn">Update</button>

		</form>

		<div id="errormsg">
		</div>

		<script>
          $(function() {
          $("form[name=f]").submit(update_profile);
          });
		</script>

		{% endif %}


	  </div>
	</div>

	{% include "footer.pat" %}

  </body>
</html>
