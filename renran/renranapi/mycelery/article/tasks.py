from django.utils import timezone as datetime

from mycelery.main import app
from article.models import Article
@app.task(name="interval_pub_article")

def interval_pub_article():
    """定时发布文章"""
    article_list = Article.objects.filter(pub_date__lte=datetime.now()).exclude(pub_date=None)
    print(article_list)
    for article in article_list:
        article.pub_date = None
        article.is_public = True
        article.save()
