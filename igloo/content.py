from zope.interface import implements
from twisted.python import components
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
    
class TaggedItem(object):
    """Adds tagging functionalty to any Axiom Item"""
    implements(ITaggedItem)

    def __init__(self, context):
        self.context = context
        
    def addTag(self, tag):
        tagItem = self.context.store.findOrCreate(Tag, name=tag)
        self.context.store.findOrCreate(TagItem, tag=tagItem, item=self.context)

    def removeTag(self, tag):
        tagItem = self.context.store.findFirst(Tag, name=tag)
        ref = self.context.store.findFirst(TagItem, tag=tagItem, item=self.context)
        if ref:
            ref.deleteFromStore()

    def tags(self):
        return self.context.store.query(Tag, AND(TagItem.item == self.context, TagItem.tag == Tag.storeID), sort=Tag.name.ascending)

    def related(self):
        #XXX; this is likely inefficient. Figure out how to do as a query
        """Returns a list of all TaggedItems which share at least one tag in common with this tagged Item"""
        items = []
        for tagItem in self.context.store.query(TagItem):
            item = tagItem.item
            if self.context != item:
                for tag in ITaggedItem(item).tags():
                    if tag in self.tags():
                        items.append(item)
                        break
        return items
components.registerAdapter(TaggedItem, Item, ITaggedItem)

class ContentType(Item):
    """A content type powerup"""
    implements(IContentType)
    typeName = "ContentType"
    powerupInterfaces = (IContentType,) 
    name = text()
