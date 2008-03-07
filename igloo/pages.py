from nevow import inevow, rend, tags as T, loaders, static, guard, accessors
from content import Site
from iigloo import IStore
from authentication import createAdmin

class IglooPage(rend.Page):
    addSlash = True
    templatesDir = "templates"
    child_styles = static.File('styles')
    child_images = static.File('images')
    child_javascript = static.File('javascript')
    child_admin = createAdmin()
    
    @staticmethod
    def loadTemplate(name):
        return loaders.xmlfile(name, templateDir=IglooPage.templatesDir)

    def childFactory(self, ctx, name):
        #need this because we can't have dots in attribute names, so can't use favourites.ico
        if name == "favicon.ico":
            return static.File('images/favicon.ico')

    def render_title(self, context, data):
        store = IStore(context)
        site = store.findFirst(Site)
        return site.title

    def render_description(self, context, data):
        store = IStore(context)
        site = store.findFirst(Site)
        return site.shortDescription

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

class AdminMainPage(IglooPage):
    docFactory = IglooPage.loadTemplate('admin/main.html')

    def render_menu(self, ctx, data):
        return T.ul(id="menu")[
                     T.li[T.a(href="/admin")["ADMIN HOME"]],
                     T.li[T.a(href="/admin/general")["SITE DETAILS"]],
                     T.li[T.a(href="/admin/users")["USER ADMINISTRATION"]],
                     T.li[T.a(href="/admin/contact")["CONTACT INFORMATION"]],
                     T.li[T.a(href="/admin/news")["NEWS"]],
                     T.li[T.a(href="/admin/portfolios")["PORTFOLIOS"]],
                     T.li[T.a(href=guard.LOGOUT_AVATAR)["LOGOUT"]],
                     ]

    def logout(self):
        ## self.original is the page's main data -- the object that was passed in to the constructor, and
        ## the object that is initially passed as the 'data' parameter to renderers
        print "%s logged out!" % self.original
