<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
	<title>Submit a new story - Luser News</title>
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
			<li><a href="/comments">comments</a></li>
			<li class="active"><a href="#">submit</a></li>
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

	  <div class="page-header">
		<h2>Submit a new story</h2>
	  </div>

	  <form name="f">
		<input value="-1" type="hidden" name="news_id">
		<label>title:</label>
		<input type="text" class="input-title" name="title" value="{{title|e}}"/> <br/>

		<br/>
		<label>url:</label>
		<input type="text" class="input-url" name="url" value="{{url|e}}"/> <br/>

		<b>or</b>

		<label>text:</label>
		<textarea class="textarea-comment" name="text" rows="6"></textarea>	<br/>

		<button type="submit" class="btn">Submit</button>

		<div id="errormsg">
		</div>
		<br/>

		<p class="help-block">Leave url blank to submit a question for discussion.</p> <br/>
		<p class="help-block">You can also submit via <a href="javascript:window.location=%22http://lusernews.com/submit?u=%22+encodeURIComponent(document.location)+%22&amp;t=%22+encodeURIComponent(document.title)">bookmarklet</a> .</p>



	  </form>


	  <script>
        $(function() {
            $("form[name=f]").submit(submit);
        });
      </script>


	</div>

	{% include "footer.pat" %}

  </body>
</html>
