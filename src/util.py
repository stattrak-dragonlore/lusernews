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

    elif seconds < 60:
        return "%s seconds ago" % seconds

    elif seconds < 3600:
        minutes = seconds / 60
        return "%d minute%s ago" % (minutes, 's' if minutes > 1 else '')

    elif seconds < 86400:
        hours = seconds / 3600
        return "%d hour%s ago" % (hours, 's' if hours > 1 else '')

    days = seconds / 86400
    return "%d day%s ago" % (days, 's' if days > 1 else '')


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
    kwargs.update({'disqus_name': config.DisqusName})
    if config.GoogleAnalytics:
        kwargs.update({'ga': config.GoogleAnalytics})
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
