import unittest
from axiom.store import Store
from axiom.item import Item
from axiom.attributes import text, reference, bytes
from axiom import dependency
from igloo.content import Content, ContentType, Site
from igloo.iigloo import IContent, IContentType
from zope.interface import implements

class Page(Item):
    """A Page in the LHMU site."""
    implements(IContentType)
    path = u"pages"
    name = u"Web Page"
    title = text()
    description = text()
    body = text()
    image = bytes()
    branch = reference()
    
    resource = reference()
    content = reference()
    def __init__(self, **kw):
        Item.__init__(self, **kw)
        self.resource = WebResource(store=self.store)
        dependency.installOn(self.resource, self)
        self.content = Content(store=self.store)
        dependency.installOn(self.content, self)

    def __repr__(self):
        return self.title

class Article(Item):
    """A News Article"""
    implements(IContentType)
    path = u"news"
    name = u"News Item"
    title = text()
    author = text()
    text = text()
    content = reference()
    def __init__(self, **kw):
        Item.__init__(self, **kw)
        self.content = Content(store=self.store)
        dependency.installOn(self.content, self)

#class ContentDocFileTest(doctest.DocTestCase):
#    pass
#    def test_readme(self):
#        doctest.DocFileTest('content.txt') 

class ContentTypeTest(unittest.TestCase):
    def setUp(self):
        self.store = Store()
        self.site = Site(store=self.store, title=u"Tech News")
        self.site.registerContentType(Page)
        self.site.registerContentType(Article)
        contentTypes = list(self.site.getContentTypes())
        self.assertEquals(len(contentTypes), 2)

    def test_basic(self):
        articleNevow = Article(store=self.store, title=u"Introducing Nevow, one kickass web framework.")
        self.site.addContent(articleNevow)
        self.assertTrue(articleNevow.path == u"news")
        contentType = self.store.findFirst(ContentType, ContentType.name == u"News Item")
        self.assertTrue(contentType == IContent(articleNevow).type)
        content = list(self.site.getContentForType(contentType))
        self.assertEquals(len(content), 1)
        self.assertEquals(content[0], articleNevow)

if __name__ == '__main__':
    unittest.main()
