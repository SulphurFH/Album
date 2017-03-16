# import datetime
from haystack import indexes
from books.models import BookInfo


class BookInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    bauthor = indexes.CharField(model_attr='bauthor')
    # btitle = indexes.CharField(model_attr='btitle')
    # bcontent = indexes.CharField(model_attr='bcontent')

    def get_model(self):
        return BookInfo

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        # return self.get_model().books.all()
        # return self.get_model().books.filter(bpub_date__lte=datetime.datetime.now())
        return self.get_model().books.filter(isDelete__lte = 0,isrelease__lte = 1)