<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
	<title>Signup - Luser News</title>
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
			  <a href="/">top</a>
			</li>
			<li><a href="/latest">new</a></li>
			<li><a href="/comments">comments</a></li>
			<li><a href="/submit">submit</a></li>
		  </ul>
		  <ul class="nav pull-right">
			<li class="divider-vertical"></li>
			<li><a href="/login">login</a></li>
		  </ul>
		</div>
	  </div>
	</div>
	<div class="container">

	  <div class="page-header">
		<h2>Create Account</h2>
	  </div>

	  <form name="f">
		<input type="text" id="username" class="input-small" placeholder="username"/> <br/>
		<input type="password" id="password" class="input-small" placeholder="password"/> <br/>
		{% if invite %}
		<input type="text" id="invitecode" class="input-small" placeholder="invitation code"/> <br/>
		{% endif %}

		<button type="submit" class="btn btn-small">signup</button> <br/>
	  </form>

	  <div id="errormsg">
	  </div>

	  <script>
        $(function() {
            $("form[name=f]").submit(signup);
        });
      </script>

	</div>

	{% include "footer.pat" %}

  </body>
</html>
