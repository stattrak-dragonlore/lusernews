<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
	<title>About - Luser News</title>
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
			<li><a href="/login">login</a></li>
			{% endif %}

		  </ul>
		</div>
	  </div>
	</div>

	<div class="container">

	  <div class="page-header">
		<h2>About</h2>
	  </div>

	  <div class="about">
		<a href="http://catb.org/jargon/html/L/luser.html">Luser</a> news is inspired by lamernews which is an implementation of a Reddit / Hacker News style news web site. <br/>

		<a href="http://github.com/dengzhp/lusernews">lusernews</a> is written in python, webob, jinja2, jQuery, bootstrap and redis. <br/>

	  </div>

	  <div id="disqus_thread"></div>
	  <script type="text/javascript">
		/* * * CONFIGURATION VARIABLES: EDIT BEFORE PASTING INTO YOUR WEBPAGE * * */
		var disqus_shortname = '{{disqus_name}}'; // required: replace example with your forum shortname
		var disqus_identifier = '/about';

		/* * * DON'T EDIT BELOW THIS LINE * * */
		(function() {
        var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
        dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
        (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
		})();
	  </script>
	  <noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>

	</div>


	{% include "footer.pat" %}


  </body>
</html>
