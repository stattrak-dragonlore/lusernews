import jinja2
from redis import StrictRedis
import config

redis = None
user = None
jj = None


def init():
    global redis, user, jj
    redis = StrictRedis(config.RedisHost, config.RedisPort)
    user = None

    loader = jinja2.FileSystemLoader(config.TemplatesPath)
    jj = jinja2.Environment(loader=loader)


