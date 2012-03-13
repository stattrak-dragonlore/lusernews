import time
import config
import util
import limit
import globals as g


# Create a new user with the specified username/password
#
# Return value: the function returns two values, the first is the
#               auth token if the registration succeeded, otherwise
#               is nil. The second is the error message if the function
#               failed (detected testing the first return value).
def create_user(username, password, userip):
    r = g.redis
    username = username.lower()
    if r.exists("username.to.id:" + username):
        return None, "Username exists, please try a different one."

    if not util.lock('create_user.' + username):
        return None, "Please wait some time before creating a new user."

    user_id = r.incr("users.count")
    auth_token = util.get_rand()
    salt = util.get_rand()
    now = int(time.time())

    pl = r.pipeline()
    pl.hmset("user:%s" % user_id, {
            "id": user_id,
            "username": username,
            "salt": salt,
            "password": util.hash_password(password, salt),
            "ctime": now,
            "karma": config.UserInitialKarma,
            "about": "",
            "email": "",
            "auth": auth_token,
            "apisecret": util.get_rand(),
            "flags": "",
            "karma_incr_time": now,
            "replies": 0,
            })

    pl.set("username.to.id:" + username, user_id)
    pl.set("auth:" + auth_token, user_id)
    pl.execute()

    util.unlock('create_user.' + username)

    return auth_token, None


# Try to authenticate the user, if the credentials are ok we populate the
# g.user global with the user information.
# Otherwise g.user is set to nil, so you can test for authenticated user
# just with: if g.user ...
def auth_user(auth):
    if not auth:
        return
    r = g.redis
    user_id = r.get("auth:%s" % auth)
    if user_id:
        g.user = r.hgetall("user:%s" % user_id)
        increment_karma_if_needed()


def get_user_by_id(user_id):
    r = g.redis
    return r.hgetall('user:%s' % user_id)


def get_user_by_name(username):
    r = g.redis
    user_id = r.get('username.to.id:%s' % username)
    if user_id:
        return get_user_by_id(user_id)


# Update the specified user authentication token with a random generated
# one. This in other words means to logout all the sessions open for that
# user.
#
# Return value: on success the new token is returned. Otherwise nil.
# Side effect: the auth token is modified.
def update_auth_token(user):
    r = g.redis
    r.delete("auth:%s" % user['auth'])
    new_auth_token = util.get_rand()
    r.hset("user:%s" % user['id'], "auth", new_auth_token)
    r.set("auth:%s" % new_auth_token, user['id'])
    return new_auth_token


# Check if the username/password pair identifies an user.
# If so the auth token and form secret are returned, otherwise nil is returned.
def check_user_credentials(username, password):
    user = get_user_by_name(username)
    if not (user and user.has_key('password') and \
                user['password'] ==  util.hash_password(password, user['salt'])):
        return None, None
    return user['auth'], user['apisecret']


def increment_karma_if_needed():
    now = time.time()
    if int(g.user['karma_incr_time']) < now - config.KarmaIncrementInterval:
        userkey = "user:%s" % g.user['id']
        g.redis.hset(userkey, "karma_incr_time", int(now))
        increment_user_karma_by(g.user['id'], config.KarmaIncrementAmount)


# Increment the user karma by the specified amount and make sure to
# update g.user to reflect the change if it is the same user.
def increment_user_karma_by(user_id, increment):
    userkey = "user:" + user_id
    g.redis.hincrby(userkey, "karma", increment)
    if g.user and int(user_id) == int(g.user['id']):
        g.user['karma'] = int(g.user['karma']) + increment


def get_new_users(count):
    r = g.redis
    n = int(r.get('users.count'))
    pl = r.pipeline()
    for i in range(n, n-count, -1):
        if i == 0:
            break
        key = "user:%s" % i
        pl.hgetall(key)

    users = pl.execute()

    return users
