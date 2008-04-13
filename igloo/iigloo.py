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
    """Tells Igloo that this is a piece of content that should be listed in the admin for users to edit"""
    name = Attribute("""Name for the content type""")
