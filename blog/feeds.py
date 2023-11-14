from django.db.models.base import Model
from django.utils.safestring import SafeText
import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatechars_html
from django.urls import reverse_lazy 
from .models import Post


class LatestPostsFeed(Feed):
# В приведенном выше исходном коде мы определили новостную ленту,
# создав подкласс класса Feed фреймворка синдицированных новостных лент.
# Атрибуты title, link и description соответствуют элементам RSS <title>,
# <link> и <description> в указанном порядке.

    title = 'My blog'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog.'
    
    def items(self):
        return Post.published.all()[:5]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return truncatechars_html(markdown.markdown(item.body), 30)
    
    def item_pubdate(self, item):
        return item.publish
    
    