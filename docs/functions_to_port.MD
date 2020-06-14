#### Functions to port for use in [Banhammer.py](https://github.com/Dan6erbond/Banhammer.py)

**`banhammer.Subreddit.__init__()`**

 - `praw.Reddit.user.me()`
 - `praw.models.Subreddit.moderator()`
 - `praw.models.Subreddit.user_is_moderator`

**`banhammer.Subreddit.get_contact_url()`**

 - `praw.models.Subreddit.display_name`

**`banhammer.Subreddit.setup()`**

 - `praw.models.Subreddit.quarantine`
 - `praw.models.Subreddit.quaran.opt_in()`
 - `praw.models.Subreddit.mod.settings()`

**`banhammer.Subreddit.load_reactions()`**

 - `praw.models.Subreddit.wiki`
 - `praw.models.Subreddit.wiki.create()`

**`banhammer.Subreddit.get_new(), get_comments()`**

 - `praw.models.Subreddit.id`
 - `praw.models.Submisison.id`
 - `praw.models.Subreddit.new()`
 - `praw.models.Subreddit.comments()`
 - `praw.models.Comment.id`
 - `praw.models.Subreddit.mod.reports()`
 - `praw.models.Subreddit.modmail.conversations()`
 - `praw.models.ModmailConversation.messages`
 - `praw.models.ModmailMessage.id`
 - `praw.models.Subreddit.mod.modqueue()`
 - `praw.models.Subreddit.mod.log()`
 - `praw.models.ModAction.id`
 - `praw.models.ModAction.action`

**`banhammer.RedditItem.get_author()`**

 - `praw.models.Submission.author`
 - `praw.models.Comment.author`
 - `praw.models.ModmailConversation.authors`
 - `praw.models.ModAction.author`

**`banhammer.RedditItem.is_author_removed()`**

 - `praw.models.Redditor.name`

**`banhammer.RedditItem.get_item_url()`**

 - `praw.models.Submission.subreddit`
 - `praw.models.Submission.__str__()`
 - `praw.models.Comment.subreddit`
 - `praw.models.Comment.submission`
 - `praw.models.Comment.__str()`
 - `praw.models.ModmailConversation.id`
 - `praw.models.Message.was_comment`
 - `praw.models.Message.__str__()`
 - `praw.models.Subreddit.display_name`

**`banhammer.MessageBuilder.get_item_message()`**

 - `praw.models.Comment.__str__()`
 - `praw.models.Comment.subreddit`
 - `praw.models.Comment.author`
 - `praw.models.Comment.permalink`
 - `praw.models.Comment.title`
 - `praw.models.Comment.selftext`
 - `praw.models.Submission.__str__()`
 - `praw.models.Submission.subreddit`
 - `praw.models.Submission.author`
 - `praw.models.Submission.permalink`
 - `praw.models.Submission.title`
 - `praw.models.Submission.selftext`
