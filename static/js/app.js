function signup() {
    var data = {
        username: $("input[id=username]").val(),
        password: $("input[id=password]").val(),
		invitecode: $("input[id=invitecode]").val(),
    };
	if (data.username.length == 0) {
		$("#errormsg").html('username missing')
		return false
	}
	if (data.password.length == 0) {
		$("#errormsg").html('password missing')
		return false
	}

    $.ajax({
        type: "POST",
        url:  "/api/signup",
        data: data,
        success: function(r) {
            if (r.status == "ok") {
                document.cookie =
                    'auth='+r.auth+
                    '; expires=Thu, 1 Aug 2030 20:00:00 UTC; path=/';
                window.location.href = "/";
            } else {
                $("#errormsg").html(r.error)
            }
        }
    });
    return false;
}

function login() {
    var data = {
        username: $("input[id=username]").val(),
        password: $("input[id=password]").val(),
    };

	if (data.username.length == 0) {
		$("#errormsg").html('username missing')
		return false
	}
	if (data.password.length == 0) {
		$("#errormsg").html('password missing')
		return false
	}

    $.ajax({
        type: "GET",
        url:  "/api/login",
        data: data,
        success: function(r) {
            if (r.status == "ok") {
                document.cookie =
                    'auth='+r.auth+
                    '; expires=Thu, 1 Aug 2030 20:00:00 UTC; path=/';
                window.location.href = "/";
            } else {
                $("#errormsg").html(r.error)
            }
        }
    });
    return false;
}

function submit() {
    var data = {
        news_id: $("input[name=news_id]").val(),
        title: $("input[name=title]").val(),
        url: $("input[name=url]").val(),
        text: $("textarea[name=text]").val(),
        apisecret: apisecret
    };
    var del = $("input[name=del]").length && $("input[name=del]").attr("checked");
    $.ajax({
        type: "POST",
		url: del ? "/api/delnews" : "/api/submit",
        data: data,
        success: function(r) {
            if (r.status == "ok") {
                if (r.news_id == -1) {
                    window.location.href = "/";
                } else {
					window.location.href = "/news/" + r.news_id;
                }
            } else {
                $("#errormsg").html(r.error)
            }
        }
    });
    return false;
}

function update_profile() {
    var data = {
        email: $("input[name=email]").val(),
        password: $("input[name=password]").val(),
        about: $("textarea[name=about]").val(),
        apisecret: apisecret
    };
    $.ajax({
        type: "POST",
        url: "/api/updateprofile",
        data: data,
        success: function(r) {
            if (r.status == "ok") {
                window.location.reload();
            } else {
                $("#errormsg").html(r.error)
            }
        }
    });
    return false;
}

function post_comment() {
    var data = {
        news_id: $("input[name=news_id]").val(),
        comment_id: $("input[name=comment_id]").val(),
        parent_id: $("input[name=parent_id]").val(),
        comment: $("textarea[name=comment]").val(),
        apisecret: apisecret
    };
    $.ajax({
        type: "POST",
        url: "/api/postcomment",
        data: data,
        success: function(r) {
            if (r.status == "ok") {
                if (r.op == "insert") {
                    window.location.href = "/news/"+r.news_id+"?r="+Math.random()+"#"+
                        r.news_id+"-"+r.comment_id;
                } else if (r.op == "update") {
                    window.location.href = "/editcomment/"+r.news_id+"/"+
                                           r.comment_id;
                } else if (r.op == "delete") {
                    window.location.href = "/news/"+r.news_id;
                }
            } else {
                $("#errormsg").html(r.error)
            }
        }
    });
    return false;
}


// Install the onclick event in all news arrows the user did not voted already.
$(function() {
    $('#newslist .story').each(function(i, news) {
        var news_id = $(news).attr("data-news-id");
        news = $(news);
        up = news.find(".uparrow");
        var voted = up.hasClass("up");
        if (!voted) {
            up.click(function(e) {
                if (typeof(apisecret) == 'undefined') return; // Not logged in
                e.preventDefault();
                var data = {
                    news_id: news_id,
                    vote_type: "up",
                    apisecret: apisecret
                };
                $.ajax({
                    type: "POST",
                    url: "/api/votenews",
                    data: data,
                    success: function(r) {
                        if (r.status == "ok") {
                            n = $(".story[data-news-id="+news_id+"]");
                            n.find(".uparrow").addClass("up");
                        } else {
                            alert(r.error);
                        }
                    }
                });
            });
        }
    });
});