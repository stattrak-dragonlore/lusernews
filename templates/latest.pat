<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
	<title>Latest news - Luser News</title>
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
			<li class="active"><a href="#">new</a></li>
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
	  <div id="newslist" class="news">
		{% for n in news %}

		<div class="story" data-news-id="{{n['id']}}">
		  <span class="newsid">{{start+loop.index}}.</span>
		  {% if n['voted'] == 'up' %}
		  <span class="uparrow {{n['voted']}}">&#9650;</span>
		  {% else %}
		  <a class="uparrow" href="#up">&#9650;</a>
		  {% endif %}
		  <a class="newstitle" title="{{n['title']|e}}" href="{{n['url']|e}}">
			{{n['title']|e|truncate(75,True,'..')}}</a>

		  {% if n['domain'] %}
		  <span class="fromsite">({{n['domain']}})</span>
		  {% endif %}

		  <div class="subtext">{{n['score']}} points, posted by <a class="submitby" href="/user/{{n['username']}}">{{n['username']}}</a> {{n['when']}} <a class="newscomments" href="/news/{{n['id']}}#disqus_thread" data-disqus-identifier="/news/{{n['id']}}">0 comments</a></div>
		</div>

		{% endfor %}

		{% if next %}

		<span class="more"><a href="/latest/{{next}}">[more]</a></span>

		{% endif %}
	  </div>


	</div>

	{% include 'commentcount.pat' %}

	{% include 'footer.pat' %}

  </body>
</html>
