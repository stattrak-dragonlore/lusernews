import time
import config
import util
import globals as g
from user import increment_user_karma_by


# Add a news with the specified url or text.
#
# If an url is passed but was already posted in the latest 48 hours the
# news is not inserted, and the ID of the old news with the same URL is
# returned.
#
# Return value: the ID of the inserted news, or the ID of the news with
# the same URL recently added.
def insert_news(title, url, text, user_id):
    r = g.redis
    # If we don't have an url but a comment, we turn the url into
    # text://....first comment..., so it is just a special case of
    # title+url anyway.
    textpost = not url
    if textpost:
        url = "text://" + text[0:config.CommentMaxLength]

    # Check for already posted news with the same URL.
    nid = r.get("url:" + url)
    if not textpost and nid:
        return int(nid)
    # We can finally insert the news.
    ctime = int(time.time())
    news_id = r.incr("news.count")
    r.hmset("news:%s" % news_id, {
            "id": news_id,
            "title": title,
            "url": url,
            "user_id": user_id,
            "ctime": ctime,
            "score": 0,
            "rank": 0,
            "up": 0,
            "down": 0,
            "comments": 0
            })

    # The posting user virtually upvoted the news posting it
    rank, error = do_vote_news(news_id, 'up')
    # Add the news to the user submitted news
    r.zadd("user.posted:%s" % user_id, ctime, news_id)
    # Add the news into the chronological view
    r.zadd("news.cron", ctime, news_id)
    # Add the news into the top view
    r.zadd("news.top", rank, news_id)
    # Add the news url for some time to avoid reposts in short time
    if not textpost:
        r.setex("url:" + url, config.PreventRepostTime, news_id)
    # Set a timeout indicating when the user may post again
    if config.NewsSubmissionBreak > 0:
        r.setex("user:%s:submitted_recently" % user_id, config.NewsSubmissionBreak, '1')
    return news_id


# Edit an already existing news.
#
# On success the news_id is returned.
# On success but when a news deletion is performed (empty title) -1 is returned.
# On failure (for instance news_id does not exist or does not match
#             the specified user_id) false is returned.
def edit_news(news_id, title, url, text, user_id):
    news = get_news_by_id(news_id)
    if not news or news.get('del') or int(news['user_id']) != int(user_id):
        return False

    if not int(news['ctime']) > (time.time() - config.NewsEditTime):
        return False

    # If we don't have an url but a comment, we turn the url into
    # text://....first comment..., so it is just a special case of
    # title+url anyway.
    textpost = not url
    if textpost:
        url = "text://" + text[0:config.CommentMaxLength]

    r = g.redis
    # Even for edits don't allow to change the URL to the one of a
    # recently posted news.
    if not textpost and url != news['url']:
        if r.get("url:" + url):
            return False
        # No problems with this new url, but the url changed
        # so we unblock the old one and set the block in the new one.
        # Otherwise it is easy to mount a DOS attack.
        r.delete("url:" + news['url'])
        r.setex("url:" + url, config.PreventRepostTime, news_id)

    # Edit the news fields.
    r.hmset("news:%s" % (news_id),
            {"title": title,
            "url": url})
    return news_id


# Mark an existing news as removed.
def del_news(news_id, user_id):
    news = get_news_by_id(news_id)
    if not news or news.get('del') or int(news['user_id']) != int(user_id):
        return False

    if not int(news['ctime']) > (time.time() - config.NewsEditTime):
        return False

    r = g.redis.pipeline()
    r.hset("news:%s" % (news_id), "del", 1)
    r.zrem("news.top", news_id)
    r.zrem("news.cron", news_id)
    r.execute()
    return True


# Vote the specified news in the context of a given user.
# type is either :up or :down
#
# The function takes care of the following:
# 1) The vote is not duplicated.
# 2) That the karma is decreased from voting user, accordingly to vote type.
# 3) That the karma is transfered to the author of the post, if different.
# 4) That the news score is updaed.
#
# Return value: two return values are returned: rank,error
#
# If the fucntion is successful rank is not nil, and represents the news karma
# after the vote was registered. The error is set to nil.
#
# On error the returned karma is false, and error is a string describing the
# error that prevented the vote.
def do_vote_news(news_id, vote_type):
    # Fetch news and user
    r = g.redis
    user = g.user
    news = get_news_by_id(news_id)
    if not news:
        return False, "No such news."

    # Now it's time to check if the user already voted that news, either
    # up or down. If so return now.
    if r.zscore("news.up:%s" % news_id, user['id']) or\
            r.zscore("news.down:%s" % news_id, user['id']):
        return False, "Duplicated vote."

    if user['id'] != news['user_id']:
        # Check if the user has enough karma to perform this operation
        if (vote_type == "up" and user['karma']  < config.NewsUpvoteMinKarma) or \
                (vote_type == "down" and (user['karma'] < config.NewsDownvoteMinKarma)):
            return False, "You don't have enough karma to vote " + vote_type

    # News was not already voted by that user. Add the vote.
    # Note that even if there is a race condition here and the user may be
    # voting from another device/API in the time between the ZSCORE check
    # and the zadd, this will not result in inconsistencies as we will just
    # update the vote time with ZADD.
    now = int(time.time())
    if r.zadd("news.%s:%s" % (vote_type, news_id), now, user['id']):
        r.hincrby("news:%s" % news_id, vote_type, 1)

    if vote_type == 'up':
        r.zadd("user.saved:%s" % user['id'], now, news_id)

    # Compute the new values of score and karma, updating the news accordingly.
    score = compute_news_score(news)
    news["score"] = score
    rank = compute_news_rank(news)
    r.hmset("news:%s" % (news_id),
           {"score": score,
            "rank": rank})
    r.zadd("news.top",rank, news_id)

    # Remove some karma to the user if needed, and transfer karma to the
    # news owner in the case of an upvote.
    if user['id'] != news['user_id']:
        if vote_type == "up":
            increment_user_karma_by(user['id'], -config.NewsUpvoteKarmaCost)
            increment_user_karma_by(news['user_id'], config.NewsUpvoteKarmaTransfered)
        else:
            increment_user_karma_by(user['id'], -config.NewsDownvoteKarmaCost)

    return rank, None


# Given the news compute its score.
# No side effects.
def compute_news_score(news):
    r = g.redis
    upvotes = r.zrange("news.up:%s" % news["id"], 0, -1, withscores=True)
    downvotes = r.zrange("news.down:%s" % news["id"], 0, -1, withscores=True)
    # FIXME: For now we are doing a naive sum of votes, without time-based
    # filtering, nor IP filtering.
    # We could use just ZCARD here of course, but I'm using ZRANGE already
    # since this is what is needed in the long term for vote analysis.
    score = len(upvotes) - len(downvotes)
    # Now let's add the logarithm of the sum of all the votes, since
    # something with 5 up and 5 down is less interesting than something
    # with 50 up and 50 down.
    votes = len(upvotes) + len(downvotes)
    if votes > config.NewsScoreLogStart:
        score += math.log(votes - config.NewsScoreLogStart) * config.NewsScoreLogBooster
    return score


# Given the news compute its rank, that is function of time and score.
#
# The general forumla is RANK = SCORE / (AGE ^ AGING_FACTOR)
def compute_news_rank(news):
    now = int(time.time())
    age = (now - int(news["ctime"])) / 60.0  #in minutes

    score = float(news["score"])

    if score <= 0:
        rank = score - (age ** config.RankAgingFactor)/20000

    else:
        rank = ((score-0.9)*20000) / \
            ((age+config.NewsAgePadding)**config.RankAgingFactor)

    if age > config.TopNewsAgeLimit:
        rank -= 6

    return rank



# Updating the rank would require some cron job and worker in theory as
# it is time dependent and we don't want to do any sorting operation at
# page view time. But instead what we do is to compute the rank from the
# score and update it in the sorted set only if there is some sensible error.
# This way ranks are updated incrementally and "live" at every page view
# only for the news where this makes sense, that is, top news.
#
# Note: this function can be called in the context of redis.pipelined {...}
def update_news_rank_if_needed(r, n):
    real_rank = compute_news_rank(n)
    delta_rank = abs(real_rank - float(n["rank"]))
    if delta_rank > 0.001:
        r.hset("news:%s" % n["id"], "rank", real_rank)
        r.zadd("news.top", real_rank, n["id"])
        n["rank"] = str(real_rank)


# Fetch one or more (if an Array is passed) news from Redis by id.
# Note that we also load other informations about the news like
# the username of the poster and other informations needed to render
# the news into HTML.
#
# Doing this in a centralized way offers us the ability to exploit
# Redis pipelining.
def get_news_by_id(news_ids, update_rank=False):
    single = False
    result = []
    if not isinstance(news_ids, list):
        single = True
        news_ids = [news_ids]

    r = g.redis
    pl = r.pipeline()
    for nid in news_ids:
        pl.hgetall('news:%s' % nid)

    news = pl.execute()
    if not news:
        # Can happen only if news_ids is an empty array.
        return []

    # Remove empty elements
    news = [n for n in news if len(n) > 0]

    if len(news) == 0:
        if single:
            return None
        else:
            return []

    if update_rank:
        for n in news:
            update_news_rank_if_needed(pl, n)
        pl.execute()

    # Get the associated users information
    for n in news:
        pl.hget('user:%s' % n['user_id'], 'username')
    usernames = pl.execute()
    for i, n in enumerate(news):
        n['username'] = usernames[i]

    # Load $User vote information if we are in the context of a
    # registered user.
    if g.user:
        for n in news:
            pl.zscore("news.up:%s" % n['id'], g.user['id'])
            pl.zscore("news.down:%s" % n['id'], g.user['id'])

        votes = pl.execute()
        for i, n in enumerate(news):
            if votes[i*2]:
                n['voted'] = 'up'
            elif votes[(i*2)+1]:
                n['voted'] = 'down'

    # Return an array if we got an array as input, otherwise
    # the single element the caller requested.
    if single:
        return news[0]
    return news


# Generate the main page of the web site, the one where news are ordered by
# rank.
#
# As a side effect thsi function take care of checking if the rank stored
# in the DB is no longer correct (as time is passing) and updates it if
# needed.
#
# This way we can completely avoid having a cron job adjusting our news
# score since this is done incrementally when there are pageviews on the
# site.
def get_top_news(start=0, count=config.TopNewsPerPage):
    r = g.redis
    numitems = r.zcard("news.top")
    news_ids = r.zrevrange("news.top", start, start+(count-1))
    result = get_news_by_id(news_ids, update_rank=True)
    # Sort by rank before returning, since we adjusted ranks during iteration.
    result.sort(cmp=lambda a, b: cmp(float(b['rank']), float(a["rank"])))
    return result, numitems


# Get news in chronological order.
def get_latest_news(start=0, count=config.LatestNewsPerPage):
    r = g.redis
    numitems = r.zcard("news.cron")
    news_ids = r.zrevrange("news.cron", start, start + count - 1)
    return get_news_by_id(news_ids, update_rank=True), numitems


# Get saved news of current user
def get_saved_news(user_id, start, count):
    r = g.redis
    numitems = int(r.zcard("user.saved:%s" % user_id))
    news_ids = r.zrevrange("user.saved:%s" % user_id, start, start + (count - 1))
    return get_news_by_id(news_ids), numitems


# Return the host part of the news URL field.
# If the url is in the form text:// nil is returned.
def news_domain(news):
    su = news["url"].split("/")
    if su[0] == "text:":
        return None
    return su[2]


# Assuming the news has an url in the form text:// returns the text
# inside. Otherwise nil is returned.
def news_text(news):
    su = news["url"].split("/")
    if su[0] == "text:":
        return news["url"][7:]
    return None


def hack_news(news):
    if isinstance(news, list):
        for n in news:
            n['when'] = util.str_elapsed(int(n['ctime']))
            n['domain'] = news_domain(n)
            if not n['domain']:
                n['url'] = '/news/%s' % n['id']
            n['title'] = n['title'].decode('utf-8')
            #rss pubDate
            n['date'] = util.rfc822(int(n['ctime']))
    else:
        news['when'] = util.str_elapsed(int(news['ctime']))
        news['domain'] = news_domain(news)
        if not news['domain']:
            news['text'] = news_text(news).decode('utf-8')
            news['url'] = '/news/%s' % news['id']
        news['title'] = news['title'].decode('utf-8')
        if g.user and g.user['id'] == news['user_id'] and\
                not news.get('del'):
            if time.time() - int(news['ctime']) < config.NewsEditTime:
                news['showedit'] = True

