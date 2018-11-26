# Install twisted asyncio loop
# From https://github.com/scrapy/scrapy/pull/3485/files#diff-db40cdeb37dd3705600b2b5a4af7e115
def _install_asyncio_reactor():
    try:
        import asyncio
        from twisted.internet import asyncioreactor
    except ImportError:
        pass
    else:
        # FIXME maybe we don't need this? Adapted from pytest_twisted
        from twisted.internet.error import ReactorAlreadyInstalledError
        try:
            asyncioreactor.install(asyncio.get_event_loop())
        except ReactorAlreadyInstalledError:
            import twisted.internet.reactor
            if not isinstance(twisted.internet.reactor,
                              asyncioreactor.AsyncioSelectorReactor):
                raise
_install_asyncio_reactor()
del _install_asyncio_reactor


from .http import PuppeteerRequest
from .middlewares import PuppeteerMiddleware
