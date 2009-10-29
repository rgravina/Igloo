from axiom.item import Item
from axiom.attributes import AND
from axiom import dependency
from nevow import inevow, rend, tags as T, loaders, static, guard, accessors
from content import Site, Content, ContentType
from iigloo import IStore, IWebResource

import formal

class IglooPage(rend.Page):
    addSlash = True
    templatesDir = "templates"
    child_styles = static.File('styles')
    child_images = static.File('images')
    child_javascript = static.File('javascript')
    child_formal_css = formal.defaultCSS

    @staticmethod
    def loadTemplate(name):
        return loaders.xmlfile(name, templateDir=IglooPage.templatesDir)

    def render_title(self, context, data):
        store = IStore(context)
        site = store.findFirst(Site)
        return site.title

    def render_description(self, context, data):
        store = IStore(context)
        site = store.findFirst(Site)
        return site.shortDescription
#workaround for the fact we can't have dots in method names
setattr(IglooPage, "child_favicon.ico",  static.File('images/favicon.ico'))

class AdminPage(IglooPage):
    def render_menu(self, ctx, data):
        return T.ul(id="menu")[
                 T.li[T.a(href="/admin")["Admin Home"]],
                 T.li[T.a(href="/admin/general")["Site Details"]],
                 T.li[T.a(href="/admin/users")["User Administration"]],
                 T.li[T.a(href=guard.LOGOUT_AVATAR)["Logout"]]]


class AdminLoginPage(IglooPage):
    docFactory = IglooPage.loadTemplate('admin.html')

    def render_loginFailureMessage(self, context, data):
        request = inevow.IRequest(context)
        if request.args.has_key("login-failure"):
            return context.tag[request.args["login-failure"]]
        return ""
    
    def render_loginForm(self, ctx, data):
        return ctx.tag(action=guard.LOGIN_AVATAR, method='post')

    def render_menu(self, ctx, data):
        return T.ul(id="menu")[T.li[T.a(href="/")["Home"]]]

class AdminSettingsPage(IglooPage):
    docFactory = IglooPage.loadTemplate('admin/general.html')

class AdminContentEditPage(formal.ResourceMixin, AdminPage):
    docFactory = IglooPage.loadTemplate('admin/content-edit.html')

    def __init__(self, content):
        self.content = content

    def form_edit(self, ctx):
        form = formal.Form()
        form.addField('aString', formal.String())
        form.addAction(self.submitted)
        return form

    def submitted(self, ctx, form, data):
        print form, data

class AdminContentListingPage(AdminPage):
    """Lists all content of a certain type"""
    docFactory = IglooPage.loadTemplate('admin/content-list.html')

    def __init__(self, contentType):
        print "in AdminContentListingPage constructor"
        self.contentType = contentType

    def locateChild(self, context, segments):
        store = IStore(context)
        if segments:
            content = store.findFirst(Content, AND(Content.type == self.contentType))
            return AdminContentEditPage(dependency.installedOn(content)), segments[1:]

    def data_list(self, context, data):
        store = IStore(context)
        site = store.findFirst(Site)
        return site.getContentForType(self.contentType)
    
    def render_item(self, context, item):
        return context.tag[T.a(href="/admin/content/%s/%s/edit" % (item.path, IWebResource(item).path))[item.title]]
        
class AdminContentPage(AdminPage):        
    def locateChild(self, context, segments):
        store = IStore(context)
        if segments:
            typeName = segments[0]
            contentType = store.findFirst(ContentType, ContentType.path == unicode(typeName))
            return AdminContentListingPage(contentType), segments[1:]

class AdminMainPage(AdminPage):
    """Main admin page. Lists content types so user can select one to edit"""
    docFactory = IglooPage.loadTemplate('admin/main.html')
    child_general = AdminSettingsPage()
    child_content = AdminContentPage()
    
    def logout(self):
        ## self.original is the page's main data -- the object that was passed in to the constructor, and
        ## the object that is initially passed as the 'data' parameter to renderers
        print "%s logged out!" % self.original

    def data_content(self, context, data):
        store = IStore(context)
        site = store.findFirst(Site)
        return site.getContentTypes()
    
    def render_content(self, context, contentType):
        return context.tag[T.a(href="/admin/content/%s" % contentType.path)[contentType.name]]
