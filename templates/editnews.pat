<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
	<title>Edit news - Luser News</title>
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
			<li>
			  <a href="/top">top</a>
			</li>
			<li><a href="/latest">new</a></li>
			<li><a href="/comments/latest/0">comments</a></li>
			<li><a href="/submit">submit</a></li>
		  </ul>
		  <ul class="nav pull-right">
			<li><a href="/user/{{user['username']}}">{{user['username'] }} ({{user['karma']}}) </a></li>
			<li class="divider-vertical"></li>
			<li><a href="/logout?apisecret={{user['apisecret']}}">logout</a></li>
		  </ul>
		</div>
	  </div>
	</div>
	<div class="container">

	  <a class="uparrow" href="#up">&#9650;</a>
	  <a class="newstitle" title="{{news['title']|e}}" href="{{news['url']|e}}">
		{{news['title']|e}}</a>
	  <span class="fromsite">({{news['domain']}})</span>

	  <div class="subtext1 newspage">{{news['score']}} points, posted by <a class="submitby" href="/user/{{news['username']}}">{{news['username']}}</a> {{news['when']}} <a class="newscomments" href="/news/{{news['id']}}">0 comments</a></div>

	  <br/>

	  <form name="f" class="newspage">
		<input value="{{news['id']}}" type="hidden" name="news_id">
		<label>title:</label>
		<input type="text" class="input-title" name="title" value="{{news['title']|e}}"/> <br/>

		<label>url:</label>
		<input type="text" class="input-url" name="url"
			   {%if not news['text'] %}
			   value="{{news['url']|e}}"
			   {% endif %}/> <br/>

		<b>or</b>

		<label>text:</label>
		<textarea class="textarea-comment" name="text" rows="6">{{news['text']}}</textarea>	<br/>
		<input value="1" type="checkbox" name="del">delete this news<br><br>

		<button type="submit" class="btn">Submit</button>

	  </form>

	  <div id="errormsg">
	  </div>

	  <script>
        $(function() {
            $("form[name=f]").submit(submit);
        });
      </script>


	</div>

	{% include "footer.pat" %}

  </body>
</html>
