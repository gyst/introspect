import md.testing
import md.testing.browser
import ith.testing
import ith.browser.testing

INTERFACE = 'InterfaceClass zope.interface.Interface'


class DebuggerViewletTest(md.testing.browser.TestCase):
    layer = ith.browser.testing.layer

    def setUp(self):
        self.app = ith.testing.add_application()
        self.therapist = ith.testing.add_therapist(
            'charlotte@example.com', 'secret')
        self.client = ith.testing.add_client(
            'bert@example.com', first_name='Bert')

    def test_public_debug_link(self):
        browser = md.testing.browser.Browser()
        browser.open(u'/app')
        self.assertIn('debugger', browser.contents)
        self.assertNotIn(INTERFACE, browser.contents)

    def test_public_debug_info(self):
        browser = md.testing.browser.Browser()
        browser.open(u'/app/?debug=1')
        self.assertIn(INTERFACE, browser.contents)

    def test_frontend_debug_link(self):
        browser = self.login(self.client, url='/app/c/')
        self.assertIn('debugger', browser.contents)
        self.assertNotIn(INTERFACE, browser.contents)

    def test_frontend_debug_info(self):
        browser = self.login(self.client, url='/app/')
        browser.open(browser.url + '?debug=1')
        self.assertIn(INTERFACE, browser.contents)

    def test_backend_debug_link(self):
        browser = self.login(self.therapist, url='/app/c/')
        self.assertIn('debugger', browser.contents)
        self.assertNotIn(INTERFACE, browser.contents)

    def test_backend_debug_info(self):
        browser = self.login(self.therapist, url='/app/c/')
        browser.open(browser.url + '?debug=1')
        self.assertIn(INTERFACE, browser.contents)
