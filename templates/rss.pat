<?xml version="1.0" encoding="utf-8" ?>
<rss version="2.0">
  <channel>
	<title>LuserNews Latest</title>
	<link>http://lusernews.com/latest</link>
	<description>luser news latest</description>
	<lastBuildDate>{{rss_build_date}}</lastBuildDate>
	<ttl>30</ttl>
	{% for n in news %}
	<item>
	  <title>
		<![CDATA[ {{n['title']|e}} ]]>
	  </title>
	  <comments>
		http://lusernews.com/news/{{n['id']}}
	  </comments>
	  <description>
		<![CDATA[ <a href="http://lusernews.com/news/{{n['id']}}">comments</a> ]]>
	  </description>
	  <link>
		{{n["url"]}}
	  </link>
	  <pubDate>
		<![CDATA[ {{n['date']}} ]]>
	  </pubDate>
	</item>
	{% endfor %}
  </channel>
</rss>
