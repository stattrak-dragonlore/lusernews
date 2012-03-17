import urllib
import hashlib
import sys
import re
import webob
import webob.exc
import url
import util

from user import *
from news import *
import globals as g

urlmapping = []

def compile_url_pattern(url_mapping):
    for m in url_mapping:
        urlmapping.append((re.compile(m[0]), m[1]))

def get_handler(request_url):
    for m in urlmapping:
        match = m[0].match(request_url)
        if match:
            module_name, method_name = m[1].rsplit('.', 1)
            try:
                module = __import__(module_name, globals(), locals(), [method_name])
            except ImportError as e:
                return
            try:
                return getattr(module, method_name), match.groups()
            except AttributeError as e:
                return


compile_url_pattern(url.url_mapping)

def application(environ, start_response):
    request_url = environ['PATH_INFO']

    request = webob.Request(environ)
    h = get_handler(request_url)

    if not h:
        #404
        response = webob.exc.HTTPNotFound()
    else:
        g.init()
        handler, param = h
        response = handler(request, *param)

    return response(environ, start_response)


def login(request):
    auth_user(request.cookies.get('auth'))
    if g.user:
        return util.redirect('/')
    else:
        return util.render('login.pat')


def signup(request):
    auth_user(request.cookies.get('auth'))
    if g.user:
        return util.redirect('/')

    return util.render('signup.pat', invite=config.InviteOnlySignUp)


def logout(request):
    auth_user(request.cookies.get('auth'))
    if g.user:
        apisecret = request.GET.get('apisecret')
        if apisecret == g.user["apisecret"]:
            update_auth_token(g.user)

    return util.redirect("/")


def submit(request):
    auth_user(request.cookies.get('auth'))
    if not g.user:
        return util.redirect('/login')
    else:
        return util.render('submit.pat', user=g.user,
                           title=request.GET.get('t', ''),
                           url=request.GET.get('u', ''))

#top news page
def top(request):
    auth_user(request.cookies.get('auth'))
    news, total = get_top_news()
    hack_news(news)
    return util.render('top.pat', news=news, user=g.user)


def index(request):
    return latest(request)


def latest(request, start=None):
    auth_user(request.cookies.get('auth'))

    if not start:
        start = 0
    else:
        try:
            #/200
            start = int(start[1:])
        except ValueError:
            start = 0
        if start < 0:
            start = 0

    news, total = get_latest_news(start)
    hack_news(news)

    next = None
    if total > start + config.LatestNewsPerPage:
        next = start + config.LatestNewsPerPage
    return util.render('latest.pat', news=news, user=g.user,
                       start=start, next=next)


def newspage(request, news_id):
    auth_user(request.cookies.get('auth'))
    news = get_news_by_id(news_id)
    if not news:
        return util.render('error.pat', user=g.user,
                           error="the news does not exist")

    hack_news(news)
    return util.render('news.pat', user=g.user, news=news)


def userpage(request, username):
    auth_user(request.cookies.get('auth'))

    user = get_user_by_name(username)
    if not user:
        return util.render('error.pat', user=g.user,
                           error='the user does not exist')

    user['created'] = "%s days ago" % int((time.time() - int(user['ctime'])) / (3600*24))

    #http://en.gravatar.com/site/implement/images/
    user['gravatar'] = "http://www.gravatar.com/avatar/" + \
        hashlib.md5(user['email'].lower()).hexdigest() + "?" + \
        "d=mm&"

    r = g.redis
    user['posted'] = r.zcard("user.posted:" + user['id'])
    user['saved'] = r.zcard("user.saved:" + user['id'])
    user['posted_comments'] = r.zcard("user.comments:" + user['id'])
    return util.render('user.pat', user=g.user, userinfo=user)


def about(request):
    auth_user(request.cookies.get('auth'))
    return util.render('about.pat', user=g.user)


def editnews(request, news_id):
    auth_user(request.cookies.get('auth'))
    if not g.user:
        return util.render('error.pat', user=g.user,
                           error='you have to login first')

    news = get_news_by_id(news_id)
    if not news:
        return util.render('error.pat', user=g.user,
                           error='the news does not exist')

    if news.get('del'):
        return util.render('error.pat', user=g.user,
                           error='news deleted')

    if news['user_id'] != g.user['id']:
        return util.render('error.pat', user=g.user,
                           error='permission denied')

    hack_news(news)
    return util.render('editnews.pat', user=g.user, news=news)


def comments(request):
    auth_user(request.cookies.get('auth'))
    return util.render('comments.pat', user=g.user)


def rss(request):
    news, total = get_latest_news()
    hack_news(news)

    return util.render('rss.pat', news=news)


def saved(request, start=None):
    auth_user(request.cookies.get('auth'))
    if not g.user:
        return util.render('error.pat', error='you need to login first')

    if not start:
        start = 0
    else:
        try:
            #/200
            start = int(start[1:])
        except ValueError:
            start = 0
        if start < 0:
            start = 0

    news, total = get_saved_news(g.user['id'], start, config.SavedNewsPerPage)
    hack_news(news)

    next = None
    if total > start + config.SavedNewsPerPage:
        next = start + config.SavedNewsPerPage
    return util.render('saved.pat', news=news, user=g.user,
                       start=start, next=next)


def lusers(request):
    auth_user(request.cookies.get('auth'))

    users = get_new_users(10)
    return util.render('lusers.pat', users=users, user=g.user)
