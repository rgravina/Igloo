from twisted.cred import portal, checkers, credentials
from nevow import inevow, guard
from zope.interface import implements
import pages

class AdminRealm:
    """A simple implementor of cred's IRealm.
       For web, this gives us the AdminLoginPage.
    """
    implements(portal.IRealm)
    def requestAvatar(self, avatarId, mind, *interfaces):
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

def createAdmin():
    realm = AdminRealm()
    porta = portal.Portal(realm)
    myChecker = checkers.InMemoryUsernamePasswordDatabaseDontUse()
    myChecker.addUser("admin","admin")
    porta.registerChecker(checkers.AllowAnonymousAccess(), credentials.IAnonymous)
    porta.registerChecker(myChecker)
    res = guard.SessionWrapper(porta)
    return res