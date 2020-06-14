"""List of Reddit API endpoints known to aPRAW."""


BASE_URL = "https://oauth.reddit.com{}?{}"

API_PATH = {
    "compose"              : "/api/compose",
    "info"                 : "/api/info",
    "moderated"            : "/user/{user}/moderated_subreddits",
    "modmail_conversation" : "/api/mod/conversations/{id}",
    "modmail_conversations": "/api/mod/conversations",
    "morechildren"         : "/api/morechildren",
    "submission"           : "/r/{sub}/comments/{id}",
    "subreddit"            : "/r/{sub}",
    "subreddit_about"      : "/r/{sub}/about",
    "subreddit_comments"   : "/r/{sub}/comments",
    "subreddit_edited"     : "/r/{sub}/about/edited",
    "subreddit_hot"        : "/r/{sub}/hot",
    "subreddit_log"        : "/r/{sub}/about/log",
    "subreddit_moderators" : "/r/{sub}/about/moderators",
    "subreddit_modqueue"   : "/r/{sub}/about/modqueue",
    "subreddit_new"        : "/r/{sub}/new",
    "subreddit_reports"    : "/r/{sub}/about/reports",
    "subreddit_rising"     : "/r/{sub}/rising",
    "subreddit_spam"       : "/r/{sub}/about/spam",
    "subreddit_top"        : "/r/{sub}/top",
    "subreddit_unmoderated": "/r/{sub}/about/unmoderated",
    "subreddits_new"       : "/subreddits/new",
    "user_about"           : "/user/{user}/about",
    "user_comments"        : "/user/{user}/comments",
    "user_submissions"     : "/user/{user}/submitted"
}
