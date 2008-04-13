from zope.interface import Interface, Attribute

class IStore(Interface):
    """ Interface used to remember the store in the site object """
    
class IWebResource(Interface):
    """Has a path that is added to the end of the URL."""
    path = Attribute("""Path name in URL. E.g. if path was "this-object" this resource would the located at /path/to/this-object""")

class ITaggedItem(Interface):
    """Maintains a list of tags for some Item"""
    tags = Attribute("""A list of tags associated with that item""")
