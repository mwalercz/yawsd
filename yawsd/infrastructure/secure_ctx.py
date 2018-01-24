from OpenSSL import SSL
from twisted.internet import ssl

from definitions import PK_PATH, CERT_PATH


class CtxFactory(ssl.ClientContextFactory):
    def getContext(self):
        self.method = SSL.SSLv23_METHOD
        ctx = ssl.ClientContextFactory.getContext(self)
        ctx.use_certificate_file(CERT_PATH)
        ctx.use_privatekey_file(PK_PATH)

        return ctx