from twisted.cred import portal, checkers, credentials
from nevow import inevow, guard
from axiom import userbase
from axiom import dependency
from zope.interface import implements

class AdminRealm(object):
    """Returns the admin login page for anonylmous users, or the admin main page for logged in users"""
    implements(portal.IRealm)
    def requestAvatar(self, avatarId, mind, *interfaces):
        import pages
        for iface in interfaces:
            if iface is inevow.IResource:
                # do web stuff
                if avatarId is checkers.ANONYMOUS:
                    resc = pages.AdminLoginPage()
                    resc.realm = self
                    return (inevow.IResource, resc, self.noLogout)
                else:
                    resc = pages.AdminMainPage(avatarId)
                    resc.realm = self
                    return (inevow.IResource, resc, resc.logout)
        raise NotImplementedError("Can't support that interface.")

    def noLogout(self):
        return None

def createLoginSystem(store):
    """Creates a axiom.userbase.LoginSystem on store and returns the LoginSystem"""
    loginSys = userbase.LoginSystem(store=store)
    dependency.installOn(loginSys, store)
    return loginSys

def createAdmin(store):
    """Creates the admin section of the site, guarded with Nevow guard."""
    realm = AdminRealm()
    cc = checkers.ICredentialsChecker(store)
    p = portal.Portal(realm, [checkers.AllowAnonymousAccess(), cc])
    resource = guard.SessionWrapper(p)
    return resource
