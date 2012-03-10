<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
	<title>Error - Luser News</title>
	<link rel="stylesheet" type="text/css" href="/css/bootstrap.css"/>
	<link rel="stylesheet" type="text/css" href="/css/lusernews.css"/>
	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js"></script>
	<script src="/js/app.js"></script>
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
			<li><a href="#">new</a></li>
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
			<li><a href="/login">login</a></li>
			{% endif %}

		  </ul>
		</div>
	  </div>
	</div>

	<div class="container">

	  <div class="page-header">
		<h2>Error</h2>
	  </div>

	  <div id="errormsg">
		{{error}}
	  </div>

	</div>

	<div id="footer" class="footer">
	  <a href="/about">about</a> | <a href="/rss">rss</a> | <a href="http://twitter.com/lusernews">twitter</a> | <a href="http://weibo.com/lusernews">weibo</a>
	  <script>var apisecret = '{{user['apisecret']}}';</script>
	</div>
  </body>
</html>
