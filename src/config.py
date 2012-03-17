import string

# Redis config
RedisHost = "127.0.0.1"
RedisPort = 6379

# Security
PBKDF2Iterations = 5000 # Set this to 5000 to improve security. But it is slow.
PasswordMinLength = 6
CreateUserRate = 3600

# limit
#[a-zA-Z_]
UsernameChars =  string.letters + string.digits + '-'
MaxTitleLen = 100
MaxUrlLen = 256


# Karma
UserInitialKarma = 1
KarmaIncrementInterval = 3*3600
KarmaIncrementAmount = 1
NewsDownvoteMinKarma = 30
NewsDownvoteKarmaCost = 6
NewsUpvoteMinKarma = 0
NewsUpvoteKarmaCost = 1
NewsUpvoteKarmaTransfered = 1
KarmaIncrementComment = 1


# Comments
CommentMaxLength = 4096
DisqusName = 'example'   #replace it with your forum shortname

# News and ranking
NewsAgePadding = 100
TopNewsPerPage = 30
LatestNewsPerPage = 30
NewsEditTime = 60*30
NewsScoreLogStart = 10
NewsScoreLogBooster = 2
RankAgingFactor = 1.6
PreventRepostTime = 3600*48
NewsSubmissionBreak = 10
SavedNewsPerPage = 30
TopNewsAgeLimit = 60*72

# path
HomePath = "~/lusernews2/"

TemplatesPath = "templates"
StaticPath = "static"

#Logging
LogFile = "logs/error.log"
LogLevel = "DEBUG"

PidFile = "logs/luser.pid"

#
InviteOnlySignUp = False

# e.g. UA-29222488-1
GoogleAnalytics = ""

github_client_id = "ZZZ"
github_secret = 'top-secret'
github_callback_url = 'http://example.com/oauth/github/callback'

