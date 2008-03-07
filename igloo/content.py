from zope.interface import implements
from axiom.item import Item
from axiom.attributes import text, reference
from iigloo import IWebResource

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

    installedOn = reference()
    def installOn(self, other):
        assert self.installedOn is None, 'cannot install on more than Item'
        self.installedOn = other
        other.powerUp(self, IWebResource)
