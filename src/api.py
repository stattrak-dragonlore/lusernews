#coding: utf-8
import time
import sys
import webob
import webob.exc
import util
import config
import globals as g
from user import *
from news import *


def signup(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if config.InviteOnlySignUp:
        invitecode = request.POST.get('invitecode')

    username, msg = util.check_string(username, 2, 20, config.UsernameChars)
    if not username:
        result = {
            'status': 'error',
            'error': 'username ' + msg
            }
        return util.json_response(result)

    password, msg = util.check_string(password, config.PasswordMinLength)
    if not password:
        result = {
            'status': 'error',
            'error': 'password ' + msg
            }
        return util.json_response(result)

    r = g.redis

    if config.InviteOnlySignUp:
        #race condition here.
        if not r.sismember('invite.code', invitecode):
            result = {
            'status': 'error',
            'error': 'invalid invitation code',
            }
            return util.json_response(result)

        #mark as used
        r.smove('invite.code', 'invite.code.used', invitecode)

    #XXX proxied requests have the same REMOTE_ADDR
    auth, msg = create_user(username, password, request.environ['REMOTE_ADDR'])
    if not auth:
        result = {
            'status': 'error',
            'error': msg,
            }
    else:
        result = {
            'status': 'ok',
            'auth': auth,
            }
    return util.json_response(result)


def login(request):
    username = request.GET.get('username')
    password = request.GET.get('password')

    username, msg = util.check_string(username, 2, 20)
    if not username:
        result = {
            'status': 'error',
            'error': 'username ' + msg
            }
        return util.json_response(result)

    password, msg = util.check_string(password)
    if not password:
        result = {
            'status': 'error',
            'error': 'password ' + msg
            }
        return util.json_response(result)

    auth, apisecret = check_user_credentials(username, password)

    if auth:
        result = {
            'status': 'ok',
            'auth': auth,
            'apisecret': apisecret
            }

    else:
        result = {
            'status': 'error',
            'error': 'bad username/password',
            }

    return util.json_response(result)


def logout(request):
    auth_user(request.cookies.get('auth'))
    if g.user:
        apisecret = request.POST.get('apisecret')
        if apisecret == g.user["apisecret"]:
            update_auth_token(g.user)
            return util.json_response({'status': 'ok'})

    result = {'status': 'error',
              'error': 'Wrong auth credentials or API secret.'
              }
    return util.json_response(result)


#submit news or edit news
def submit(request):
    auth_user(request.cookies.get('auth'))
    if not g.user:
        result = {'status': 'error',
                  'error': 'Not authenticated.'
                  }
        return util.json_response(result)

    if request.POST.get('apisecret') != g.user["apisecret"]:
        result = {'status': 'error',
                  'error': 'Wrong form secret'
                  }
        return util.json_response(result)

    title = request.POST.get('title')
    url = request.POST.get('url')
    text = request.POST.get('text')
    news_id = util.force_int(request.POST.get('news_id'))

    if text:
        text = text.lstrip('\r\n').rstrip()

    if not title or (not url and not text):
        result = {'status': 'error',
                  'error': 'title and (url or text) required'
                  }
        return util.json_response(result)

    # Make sure the URL is about an acceptable protocol, that is
    # http:// or https:// for now.
    if url and not url.startswith('http://') and not url.startswith('https://'):
        result = {'status': 'error',
                  'error': 'we only accept http:// and https:// news'
                  }
        return util.json_response(result)

    if len(title) > config.MaxTitleLen or len(url) > config.MaxUrlLen:
        result = {'status': 'error',
                  'error': 'title or url too long'
                  }
        return util.json_response(result)

    if not url and len(text) > config.CommentMaxLength:
        result = {'status': 'error',
                  'error': 'text too long'
                  }
        return util.json_response(result)

    if news_id is None:
        result = {'status': 'error',
                  'error': 'bad news_id'
                  }
        return util.json_response(result)

    if news_id == -1:
        if limit.submitted_recently():
            result = {'status': 'error',
                      'error': "You have submitted a story too recently, " +
                      "please wait %s seconds." % limit.allowed_to_post_in_seconds()
                      }
            return util.json_response(result)

        news_id = insert_news(title, url, text, g.user['id'])

    else:
        news_id = edit_news(news_id, title, url, text, g.user['id'])
        if not news_id:
            result = {'status': 'error',
                      'error': 'Invalid parameters, news too old to be modified' +
                      'or url recently posted.'
                      }
            return util.json_response(result)

    result = {'status': 'ok',
              'news_id': int(news_id)
              }

    return util.json_response(result)


def delete_news(request):
    auth_user(request.cookies.get('auth'))
    if not g.user:
        result = {'status': 'error',
                  'error': 'Not authenticated.'
                  }
        return util.json_response(result)

    if request.POST.get('apisecret') != g.user["apisecret"]:
        result = {'status': 'error',
                  'error': 'Wrong form secret'
                  }
        return util.json_response(result)

    news_id = util.force_int(request.POST.get('news_id'))
    if not news_id:
        result = {'status': 'error',
                  'error': 'bad news_id'
                  }
        return util.json_response(result)

    if del_news(news_id, g.user['id']):
        result = {'status': 'ok',
                  'news_id': -1
                  }
        return util.json_response(result)

    result = {'status': 'err',
              'error': 'News too old or wrong ID/owner.'
              }

    return util.json_response(result)


def update_profile(request):
    auth_user(request.cookies.get('auth'))
    if not g.user:
        result = {'status': 'error',
                  'error': 'Not authenticated.'
                  }
        return util.json_response(result)

    if request.POST.get('apisecret') != g.user["apisecret"]:
        result = {'status': 'error',
                  'error': 'Wrong form secret'
                  }
        return util.json_response(result)


    password = request.POST.get('password')    #optinal
    email = request.POST.get('email')
    about = request.POST.get('about')

    email, msg = util.check_string(email, maxlen=128)
    if email is None:
        result = {
            'status': 'error',
            'error': 'email ' + msg
            }
        return util.json_response(result)

    about, msg = util.check_string(about, maxlen=256)
    if about is None:
        result = {
            'status': 'error',
            'error': 'about ' + msg
            }
        return util.json_response(result)

    r = g.redis

    if password:
        password, msg = util.check_string(password, config.PasswordMinLength)
        if not password:
            result = {
                'status': 'error',
                'error': 'password ' + msg
                }
            return util.json_response(result)

        salt = g.user.get('salt', util.get_rand())
        r.hmset("user:" + g.user['id'], {
                "password": util.hash_password(password, salt),
                "salt": salt
                })

    r.hmset("user:" + g.user['id'], {
            "about": about.rstrip(),
            "email": email
            })
    return util.json_response({'status': "ok"})


def vote_news(request):
    auth_user(request.cookies.get('auth'))
    if not g.user:
        result = {'status': 'error',
                  'error': 'Not authenticated.'
                  }
        return util.json_response(result)

    if request.POST.get('apisecret') != g.user["apisecret"]:
        result = {'status': 'error',
                  'error': 'Wrong form secret'
                  }
        return util.json_response(result)

    news_id = util.force_int(request.POST.get('news_id'))
    vote_type = request.POST.get('vote_type')
    if not news_id or (vote_type != 'up' and vote_type != 'down'):
        result = {'status': 'error',
                  'error': 'Missing news ID or invalid vote type.'
                  }
        return util.json_response(result)

    # Vote the news
    karma, error = do_vote_news(news_id, vote_type)
    if karma:
        return util.json_response({"status": "ok" })
    else:
        return util.json_response({"status": "error" })
