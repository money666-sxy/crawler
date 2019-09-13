from items.notebook_item import NotebookItem
from items.user_item import UserItem


class ArticleItem(object):

    def __init__(self, article_id=None, title=None, content=None, public_comments_count=None, likes_count=None,
                 views_count=None, total_rewards_count=None, first_shared_at=None, like_rate=None):

        self.article_id = article_id
        self.title = title
        self.content = content
        self.public_comments_count = public_comments_count
        self.likes_count = likes_count
        self.views_count = views_count
        self.total_rewards_count = total_rewards_count
        self.first_shared_at = first_shared_at
        self.like_rate = 0
        self.author = UserItem()
        self.notebook = NotebookItem()


class RenMinArticalItem(object):

    def __init__(self, title, content, info_url, first_shared_at):
        self.title = title
        self.content = content
        self.info_url = info_url
        self.first_shared_at = first_shared_at
