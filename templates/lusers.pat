<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
	<title>new lusers - Luser News</title>
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

	  <div class="page-header">
		<h3>New Lusers</h3>
	  </div>

	  <div class="lusers">

		{% for u in users %}

		<span class="luser">
		  <a href="/luser/{{u['username']}}">{{u['username']}}</a>
		</span>

		{% endfor %}

	  </div>

	</div>

	{% include "footer.pat" %}

  </body>
</html>
