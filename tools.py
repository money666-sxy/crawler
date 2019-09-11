import datetime

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
    like_rate = days / like_count
    if like_rate > 3:
        pass  # 优秀文章
    else:
        pass


def text_fix(text):
    '''去除json信息中的html标签'''
    text = text.replace(
        r"<em class='search-result-highlight'>", "").replace(r"</em>", "")
    return text