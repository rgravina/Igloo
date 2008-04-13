from nevow import inevow, rend, tags as T, loaders, static, guard, accessors
from content import Site
from iigloo import IStore

class IglooPage(rend.Page):
    addSlash = True
    templatesDir = "templates"
    child_styles = static.File('styles')
    child_images = static.File('images')
    child_javascript = static.File('javascript')

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
        return T.ul(id="menu")[T.li[T.a(href="/")["HOME"]]]

class AdminSettingsPage(IglooPage):
    docFactory = IglooPage.loadTemplate('admin/general.html')

class AdminContentPage(IglooPage):
    docFactory = IglooPage.loadTemplate('content.html')
    
    def locateChild(self, context, segments):
        # Let parent class have a go first
        child, remainingSegments = rend.Page.locateChild(self, context, segments)
        if child:
            return child, remainingSegments
        store = IStore(context)
        if segments:
            #have requested some news article
            path = segments[0]
            article = store.findFirst(Content)
            #now check if they have requested an operation of some kind
            return NewsArticlePage(article), []
        return None, []

class AdminMainPage(IglooPage):
    docFactory = IglooPage.loadTemplate('admin/main.html')
    child_general = AdminSettingsPage()
    child_content = AdminContentPage()
    
    def render_menu(self, ctx, data):
        return T.ul(id="menu")[
                     T.li[T.a(href="/admin")["ADMIN HOME"]],
                     T.li[T.a(href="/admin/general")["SITE DETAILS"]],
                     T.li[T.a(href="/admin/users")["USER ADMINISTRATION"]],
                     T.li[T.a(href=guard.LOGOUT_AVATAR)["LOGOUT"]]]

    def logout(self):
        ## self.original is the page's main data -- the object that was passed in to the constructor, and
        ## the object that is initially passed as the 'data' parameter to renderers
        print "%s logged out!" % self.original

