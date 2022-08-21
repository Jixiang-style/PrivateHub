import xadmin

from .models import ArticleCollection
class ArticleCollectionModelAdmin(object):
    list_display = ["id","name"]
xadmin.site.register(ArticleCollection,ArticleCollectionModelAdmin)

from .models import Special
class SpecialModelAdmin(object):
    list_display = ["id","name"]
xadmin.site.register(Special,SpecialModelAdmin)

from .models import Article
class ArticleModelAdmin(object):
    list_display = ["id","name"]
xadmin.site.register(Article,ArticleModelAdmin)

from .models import SpecialArticle
class SpecialArticleModelAdmin(object):
    list_display = ["id","name"]
xadmin.site.register(SpecialArticle,SpecialArticleModelAdmin)
from .models import SpecialManager
class SpecialManagerModelAdmin(object):
    list_display = ["id","name"]
xadmin.site.register(SpecialManager,SpecialManagerModelAdmin)

from .models import SpecialFocus
class SpecialFocusModelAdmin(object):
    list_display = ["id","name"]
xadmin.site.register(SpecialFocus,SpecialFocusModelAdmin)

from .models import SpecialCollection
class SpecialCollectionModelAdmin(object):
    list_display = ["id","name"]
xadmin.site.register(SpecialCollection,SpecialCollectionModelAdmin)

from .models import ArticleImage
class ArticleImageModelAdmin(object):
    list_display = ["id","name"]
xadmin.site.register(ArticleImage,ArticleImageModelAdmin)
