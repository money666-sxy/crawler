import datetime

from items.article_item import ArticleItem

def like_rate(article):
    '''发布时间/点赞数'''

    '''article.first_shared_at() 2019-04-21T07:22:12.000Z'''
    like_count = article.like_count
    first_shared_at = article.first_shared_at
    share_year = first_shared_at[0:4]
    share_month = first_shared_at[5:7]
    share_day = first_shared_at[8:10]
    if share_month[0] == '0':
        share_month = share_month[1]
    if share_day[0] == '0':
        share_day = share_day[1]
    days = (datetime.datetime.today() - datetime.datetime(int(share_year), int(share_month), int(share_day))).days
    if like_count == 0:
        return 0
    like_rate = days / like_count
    return like_rate


def text_fix(text):
    '''去除json信息中的html标签'''
    text = text.replace(
        r"<em class='search-result-highlight'>", "").replace(r"</em>", "")
    return text

async def create_article(text, db_queue):
    for item in text:
        article = ArticleItem()
        article.id = item['id']
        article.title = text_fix(item['title'])
        article.content = text_fix(item['content'])
        article.slug = item['slug']
        article.author.id = item['user']['id']
        article.author.nickname = item['user']['nickname']
        article.author.author_avatar_url = item['user']['avatar_url']
        article.notebook.id = item['notebook']['id']
        article.notebook.name = item['notebook']['name']
        article.commentable = item['commentable']
        article.public_comments_count = item['public_comments_count']
        article.like_count = item['likes_count']
        article.views_count = item['views_count']
        article.total_rewards_count = item['total_rewards_count']
        article.first_shared_at = item['first_shared_at']
        db_queue.put(article)