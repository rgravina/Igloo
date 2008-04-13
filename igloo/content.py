from zope.interface import implements
from axiom.item import Item
from axiom.attributes import text, reference, AND
from axiom import dependency
from iigloo import *

class Site(Item):
    """A website. Contains information like site title etc."""
    typeName = 'Site'
    title = text()
    shortDescription = text()

class WebResource(Item):
    """A web resource powerup"""
    implements(IWebResource)
    typeName = "WebResource"
    path = text()
    powerupInterfaces = (IWebResource,) 

class Tag(Item):
    """A tag"""
    typeName = "Tag"
    name = text()

    def __repr__(self):
        return self.name

class TagItem(Item):
    """A link between a tag and an Item"""
    typeName = "TagItem"
    tag = reference()
    item = reference()
    
class TaggedItem(Item):
    """A tagging powerup"""
    implements(ITaggedItem)
    typeName = "TaggedItem"
    #XXX:figure out how to avoid 
    dummy = text()

    powerupInterfaces = (ITaggedItem,) 

    def addTag(self, tag):
        tagItem = self.store.findOrCreate(Tag, name=tag)
        self.store.findOrCreate(TagItem, tag=tagItem, item=dependency.installedOn(self))


    def removeTag(self, tag):
        tagItem = self.store.findFirst(Tag, name=tag)
        ref = self.store.findFirst(TagItem, tag=tagItem, item=dependency.installedOn(self))
        if ref:
            ref.deleteFromStore()

    def tags(self):
        return self.store.query(Tag, AND(TagItem.item == dependency.installedOn(self), TagItem.tag == Tag.storeID), 
                                sort=Tag.name.ascending)

    def related(self):
        #XXX; this is likely inefficient. Figure out how to do as a query
        """Returns a list of all TaggedItems which share at least one tag in common with this tagged Item"""
        articles = []
        for taggedItem in self.store.query(TaggedItem):
            article = dependency.installedOn(taggedItem)
            if dependency.installedOn(self) != article:
                for tag in taggedItem.tags():
                    if tag in self.tags():
                        articles.append(article)
                        break
        return articles
