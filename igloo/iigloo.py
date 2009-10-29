from zope.interface import Interface, Attribute

class IStore(Interface):
    """ Interface used to remember the store in the site object """
    
class IWebResource(Interface):
    """Has a path that is added to the end of the URL."""
    path = Attribute("""Path name in URL. E.g. if path was "this-object" this resource would the located at /path/to/this-object""")

class ITaggedItem(Interface):
    """Maintains a list of tags for some Item"""
    def tags(self):
        """Returns a sorted list of tags associated with this item"""

class IContentType(Interface):
    """A content type. These are used to to say a particular IContent is a certain type"""
    name = Attribute("""Name for the content type""")
    path = Attribute("""Path at which this content type will be listed in the admin""")

    
class IForm(Interface):
    """Creates an edit form"""
    def form(self):
        """Returns a edit form for this content type"""

class IContent(Interface):
    """Tells the admin that a particular Item is content"""
    type = Attribute("""Reference to ContentType object""")

