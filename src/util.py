import json
import time
import os
import binascii
import webob
import webob.exc
import jinja2
import globals as g
import config

# Return the hex representation of an unguessable 160 bit random number.
def get_rand(length=20):
    return binascii.hexlify(os.urandom(length))


def hash_password(password, salt):
    from pbkdf2 import pbkdf2_hex
    return pbkdf2_hex(password, salt, config.PBKDF2Iterations)


def check_string(string, minlen=-1, maxlen=-1, charset=None):
    if isinstance(string, unicode):
        try:
            string = str(string)
        except UnicodeError:
            return None, "invalid"
    elif not isinstance(string, str):
        return None, "invalid"

    if maxlen != -1 and len(string) > maxlen:
        return None, "too long"
    elif minlen != -1 and len(string) < minlen:
        return None, "too short"

    if charset:
        for c in string:
            if c not in charset:
                return None, 'invalid char'

    return string, ''


# Given an unix time in the past returns a string stating how much time
# has elapsed from the specified time, in the form "2 hours ago".
def str_elapsed(t):
    seconds = int(time.time()) - t
    if seconds <= 1:
        return "now"
    if seconds < 60:
        return "%s seconds ago" % (seconds)
    if seconds < 60 * 60:
        return "%d minutes ago" % (seconds / 60)

    if seconds < 3600 * 24:
        return "%d hours ago" % (seconds / 3600)

    else:
        return "%d days ago" % (seconds / 3600 / 24)


def redirect(location='/'):
    return webob.exc.HTTPTemporaryRedirect(location=location)

def json_response(result):
    return webob.Response(json.dumps(result), content_type='application/json')

def static_response(file):
    f = open(os.path.join(config.StaticPath, file))
    html = f.read()
    f.close()
    return webob.Response(html)


#template
def render(template, **kwargs):
    return webob.Response(g.jj.get_template(template).render(kwargs))

def rfc822(when=None):
    return time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(when))


def lock(string):
    key = "lock:" + string
    return g.redis.setnx(key, int(time.time()))

def unlock(string):
    key = "lock:" + string
    return g.redis.delete(key)


def force_int(s):
    try:
        return int(s)
    except:
        return None
