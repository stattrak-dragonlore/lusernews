import config
import globals as g

# Has the user submitted a news story in the last `NewsSubmissionBreak` seconds?
def submitted_recently():
    return allowed_to_post_in_seconds() > 0

# Indicates when the user is allowed to submit another story after the last.
def allowed_to_post_in_seconds():
    return g.redis.ttl('user:%s:submitted_recently' % g.user['id'])


# Generic API limiting function
def rate_limit_by_ip(delay, *tags):
    r = g.redis
    key = "limit:" + ".".join(tags)
    if r.exists(key):
        return True
    r.setex(key, delay, 1)
    return False
