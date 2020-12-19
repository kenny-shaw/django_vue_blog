from drf_haystack.serializers import HaystackSerializer, HaystackSerializerMixin, HighlighterMixin
from api.serializers import articleserializer
from api import models
from api.search_indexes import ArticleIndex
# from haystack.utils import Highlighter
from rest_framework.fields import CharField

from django.utils.html import strip_tags
from haystack.utils import Highlighter as HaystackHighlighter


class Highlighter(HaystackHighlighter):
    """
    自定义关键词高亮器，不截断过短的文本（例如文章标题）
    """

    def highlight(self, text_block):
        self.text_block = strip_tags(text_block)
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)
        if len(text_block) < self.max_length:
            start_offset = 0
        return self.render_html(highlight_locations, start_offset, end_offset)


class HighlightedCharField(CharField):
    """
    自定义序列化显示，将查询处的内容进行高亮显示
    """

    def to_representation(self, value):
        value = super().to_representation(value)
        request = self.context["request"]
        query = request.query_params.get('text')
        highlighter = Highlighter(query)
        return highlighter.highlight(value)


class ArticleForSearchSerializer(HaystackSerializerMixin, articleserializer.ArticleReadListSerializer):
    # 高亮显示
    title = HighlightedCharField()
    summary = HighlightedCharField(source="content_text")

    class Meta(articleserializer.ArticleReadListSerializer.Meta):
        # index_classes=[ArticleIndex]
        search_fields = ["text"]
