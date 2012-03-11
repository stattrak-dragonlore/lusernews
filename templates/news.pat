<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
	<title> {{news['title']|e}} - Luser News</title>
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
	  <div id="newslist">
		<div class="story" data-news-id="{{news['id']}}">
		  {% if news["del"] %}
		  <span class="uparrow">&#9650;</span>
		  <span class="deleted">deleted</span>

		  {% else %}


		  {% if news['voted'] == 'up' %}
		  <span class="uparrow up">&#9650;</span>
		  {% else %}
		  <a class="uparrow" href="#up">&#9650;</a>
		  {% endif %}

		  <a class="newstitle" title="{{news['title']}}"  href="{{news['url']|e}}">
			{{news['title']|e}}</a>
		  {% if news['domain'] %}
		  <span class="fromsite">({{news['domain']}})</span>
		  {% endif %}
		  {% if news["showedit"] %}
		  <a href="/editnews/{{news['id']}}">[edit]</a>
		  {% endif %}

		  {% endif %}
		</div>
	  </div>

	  <div class="subtext1 newspage">{{news['score']}} points, posted by <a class="submitby" href="/user/{{news['username']}}">{{news['username']}}</a> {{news['when']}} <a class="newscomments" href="/news/{{news['id']}}#disqus_thread" data-disqus-identifier="/news/{{news['id']}}">0 comments</a></div>

	  {% if news["text"] %}
	  <div class="newstext"><pre> {{news["text"]|e}} </pre></div>
	  {% endif %}


	  {%if 1 %}
	  <div id="disqus_thread" class="disqus"></div>
	  <script type="text/javascript">
		/* * * CONFIGURATION VARIABLES: EDIT BEFORE PASTING INTO YOUR WEBPAGE * * */
		var disqus_shortname = '{{disqus_name}}'; // required: replace example with your forum shortname
		var disqus_identifier = '/news/{{news["id"]}}';

		/* * * DON'T EDIT BELOW THIS LINE * * */
		(function() {
        var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
        dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
        (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
		})();

	  </script>

	  <!-- comments count  -->
	  <script type="text/javascript">
		/* * * CONFIGURATION VARIABLES: EDIT BEFORE PASTING INTO YOUR WEBPAGE * * */
		var disqus_shortname = '{{disqus_name}}'; // required: replace example with your forum shortname

		/* * * DON'T EDIT BELOW THIS LINE * * */
		(function () {
        var s = document.createElement('script'); s.async = true;
        s.type = 'text/javascript';
        s.src = 'http://' + disqus_shortname + '.disqus.com/count.js';
        (document.getElementsByTagName('HEAD')[0] || document.getElementsByTagName('BODY')[0]).appendChild(s);
		}());
	  </script>

	  <noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>



	  {% else %}
	  <form name="f" class="newspage">
		<input value="{{news['id']}}" type="hidden" name="news_id">
		<input value="-1" type="hidden" name="comment_id">
		<input value="-1" type="hidden" name="parent_id"> <br/>
		<textarea class="textarea-comment" rows="6" name="comment"></textarea> <br>
		<button type="submit" class="btn btn-small">Add comment</button>
	  </form>
	  <div id="errormsg">
	  </div>

	  {% endif %}

	  <script>
        $(function() {
            $("form[name=f]").submit(post_comment);
        });
      </script>

	</div>

	<div id="footer" class="footer">
	<a href="/about">about</a> | <a href="/rss">rss</a> | <a href="http://twitter.com/lusernews">twitter</a> | <a href="http://weibo.com/lusernews">weibo</a>
	<script>var apisecret = '{{user['apisecret']}}';</script>
  </div>
  </body>
</html>
