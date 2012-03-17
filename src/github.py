import json
import webob
import oauth2  #requires httplib2 0.6
import util
import config
import globals as g
from user import *


# github:login -> id
#

oauth_settings = {
    'client_id': config.github_client_id,
    'client_secret': config.github_secret,
    'base_url': 'https://github.com/login/oauth/',
    'redirect_url': config.github_callback_url,
}

def auth(request):
    auth_user(request.cookies.get('auth'))
    if g.user:
        return util.redirect('/')

    oauth_client = oauth2.Client2(
        oauth_settings['client_id'],
        oauth_settings['client_secret'],
        oauth_settings['base_url']
        )
    authorization_url = oauth_client.authorization_url(
        redirect_uri = oauth_settings['redirect_url'],
        # params={'scope': 'user'}
        )
    return util.redirect(authorization_url)


# this function is slow
def callback(request):
    auth_user(request.cookies.get('auth'))
    if g.user:
        return util.redirect('/')

    oauth_client = oauth2.Client2(
        oauth_settings['client_id'],
        oauth_settings['client_secret'],
        oauth_settings['base_url']
        )

    code = request.GET.get('code')
    if not code:
        return util.render('error.pat', user=None,
                           error="no code")

    try:
        data = oauth_client.access_token(code, oauth_settings['redirect_url'])
    except Exception as e:
        return util.render('error.pat', user=None,
                           error="failed to get access token, try again")
    access_token = data.get('access_token')

    (headers, body) = oauth_client.request(
        'https://api.github.com/user',
        access_token=access_token,
        token_param='access_token'
        )

    error = 0
    try:
        if headers['status'] == '200':
            user = json.loads(body)
            username = user['login']
            email = user.get('email', '')
        else:
            error = 1
    except Exception as e:
        error = 1

    if error:
        return util.render('error.pat', user=None, error='bad login, try again')

    user = get_user_by_name(username)
    if not user:
        #create new user
        auth, msg = create_user_github(username, email)
        if not auth:
            return util.render('error.pat', user=None, error=msg)
    else:
        if 'g' in user['flags']:
            auth = user['auth']
        else:
            return util.render('error.pat', user=None, error='account exists :(')

    res = webob.exc.HTTPTemporaryRedirect(location='/')
    res.headers['Set-Cookie'] = 'auth=' + auth + \
        '; expires=Thu, 1 Aug 2030 20:00:00 UTC; path=/';
    return res


# Create a new user with github login name
#
# Return value: the function returns two values, the first is the
#               auth token if the registration succeeded, otherwise
#               is nil. The second is the error message if the function
#               failed (detected testing the first return value).
def create_user_github(username, email):
    r = g.redis
    username = username.lower()

    if r.exists("username.to.id:" + username):
        return None, "Username exists, please try a different one."

    if not util.lock('create_user.' + username):
        return None, "Please wait some time before creating a new user."

    user_id = r.incr("users.count")
    auth_token = util.get_rand()
    now = int(time.time())

    pl = r.pipeline()
    pl.hmset("user:%s" % user_id, {
            "id": user_id,
            "username": username,
            "ctime": now,
            "karma": config.UserInitialKarma,
            "about": "",
            "email": email,
            "auth": auth_token,
            "apisecret": util.get_rand(),
            "flags": "g", #github user
            "karma_incr_time": now,
            "replies": 0,
            })

    pl.set("username.to.id:" + username, user_id)
    pl.set("auth:" + auth_token, user_id)

    pl.execute()
    util.unlock('create_user.' + username)

    return auth_token, None

