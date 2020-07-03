# TODO

## Endpoints

### Functions to port for use in [Banhammer.py](https://github.com/Dan6erbond/Banhammer.py)

**`banhammer.Subreddit.__init__()`**

 - [x] ~~`praw.Reddit.user.me()`~~
 - [x] ~~`praw.models.Subreddit.moderator()`~~
 - [x] ~~`praw.models.Subreddit.user_is_moderator`~~

**`banhammer.Subreddit.get_contact_url()`**

 - [x] ~~`praw.models.Subreddit.display_name`~~

**`banhammer.Subreddit.setup()`**

 - [ ] `praw.models.Subreddit.quarantine`
 - [ ] `praw.models.Subreddit.quaran.opt_in()`
 - [ ] `praw.models.Subreddit.mod.settings()`

**`banhammer.Subreddit.load_reactions()`**

 - [ ] `praw.models.Subreddit.wiki`
 - [ ] `praw.models.Subreddit.wiki.create()`

**`banhammer.Subreddit.get_new(), get_comments()`**

 - [x] ~~`praw.models.Subreddit.id`~~
 - [x] ~~`praw.models.Submisison.id`~~
 - [x] ~~`praw.models.Subreddit.new()`~~
 - [x] ~~`praw.models.Subreddit.comments()`~~
 - [x] ~~`praw.models.Comment.id`~~
 - [x] ~~`praw.models.Subreddit.mod.reports()`~~
 - [x] ~~`praw.models.Subreddit.modmail.conversations()`~~
 - [x] ~~`praw.models.ModmailConversation.messages`~~
 - [x] ~~`praw.models.ModmailMessage.id`~~
 - [x] ~~`praw.models.Subreddit.mod.modqueue()`~~
 - [x] ~~`praw.models.Subreddit.mod.log()`~~
 - [x] ~~`praw.models.ModAction.id`~~
 - [x] ~~`praw.models.ModAction.action`~~

**`banhammer.RedditItem.get_author()`**

 - [x] ~~`praw.models.Submission.author`~~
 - [x] ~~`praw.models.Comment.author`~~
 - [x] ~~`praw.models.ModmailConversation.authors`~~
 - [x] ~~`praw.models.ModAction.author`~~

**`banhammer.RedditItem.is_author_removed()`**

 - [x] ~~`praw.models.Redditor.name`~~

**`banhammer.RedditItem.get_item_url()`**

 - [x] ~~`praw.models.Submission.subreddit`~~
 - [ ] `praw.models.Submission.__str__()`
 - [x] ~~`praw.models.Comment.subreddit`~~
 - [x] ~~`praw.models.Comment.submission`~~
 - [ ] `praw.models.Comment.__str()`
 - [x] ~~`praw.models.ModmailConversation.id`~~
 - [ ] `praw.models.Message.was_comment`
 - [ ] `praw.models.Message.__str__()`
 - [x] ~~`praw.models.Subreddit.display_name`~~

**`banhammer.MessageBuilder.get_item_message()`**

 - [ ] `praw.models.Comment.__str__()`
 - [x] ~~`praw.models.Comment.subreddit`~~
 - [x] ~~`praw.models.Comment.author`~~
 - [x] `praw.models.Comment.permalink`
 - [x] ~~`praw.models.Comment.title`~~ -> doesn't exist
 - [x] ~~`praw.models.Comment.selftext`~~ -> doesn't exist
 - [ ] `praw.models.Submission.__str__()`
 - [x] ~~`praw.models.Submission.subreddit`~~
 - [x] ~~`praw.models.Submission.author`~~
 - [x] ~~`praw.models.Submission.permalink`~~
 - [x] ~~`praw.models.Submission.title`~~
 - [x] ~~`praw.models.Submission.selftext`~~

## Helpers

### Classes

### Functions
