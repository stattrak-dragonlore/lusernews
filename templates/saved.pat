<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
	<title>Saved news - Luser News</title>
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
			<li><a href="/latest">new</a></li>
			<li><a href="/comments">comments</a></li>
			<li><a href="/submit">submit</a></li>
		  </ul>

		  <ul class="nav pull-right">
			<li><a href="/user/{{user['username']}}">{{user['username']}} ({{user['karma']}})</a></li>
			<li class="divider-vertical"></li>
			<li><a href="/logout?apisecret={{user['apisecret']}}">logout</a></li>
		  </ul>
		</div>
	  </div>
	</div>

	<div class="container">
	  <div class="page-header">
		<h3>Your saved news</h3>
	  </div>

	  <div class="news">
		{% for n in news %}

		<div class="story">
		  <span class="newsid">{{start+loop.index}}.</span>
		  <span class="uparrow up">&#9650;</span>
		  <a class="newstitle" title="{{n['title']|e}}" href="{{n['url']|e}}">
			{{n['title']|e|truncate(75,True,'..')}}</a>

		  {% if n['domain'] %}
		  <span class="fromsite">({{n['domain']}})</span>
		  {% endif %}

		  <div class="subtext">{{n['score']}} points, posted by <a class="submitby" href="/user/{{n['username']}}">{{n['username']}}</a> {{n['when']}} <a class="newscomments" href="/news/{{n['id']}}#disqus_thread" data-disqus-identifier="/news/{{n['id']}}">0 comments</a></div>
		</div>

		{% endfor %}

		{% if next %}

		<span class="more"><a href="/saved/{{next}}">[more]</a></span>

		{% endif %}
	  </div>


	</div>

	<script type="text/javascript">
    /* * * CONFIGURATION VARIABLES: EDIT BEFORE PASTING INTO YOUR WEBPAGE * * */
    var disqus_shortname = 'lusernews'; // required: replace example with your forum shortname

    /* * * DON'T EDIT BELOW THIS LINE * * */
    (function () {
        var s = document.createElement('script'); s.async = true;
        s.type = 'text/javascript';
        s.src = 'http://' + disqus_shortname + '.disqus.com/count.js';
        (document.getElementsByTagName('HEAD')[0] || document.getElementsByTagName('BODY')[0]).appendChild(s);
    }());
	</script>

	<div id="footer" class="footer">
	  <a href="/about">about</a> | <a href="/rss">rss</a> | <a href="http://twitter.com/lusernews">twitter</a> | <a href="http://weibo.com/lusernews">weibo</a>
	  <script>var apisecret = '{{user['apisecret']}}';</script>
	</div>
  </body>
</html>
