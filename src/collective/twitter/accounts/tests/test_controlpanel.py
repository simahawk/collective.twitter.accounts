# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles

from plone.registry.interfaces import IRegistry

from collective.twitter.accounts.config import PROJECTNAME
from collective.twitter.accounts.testing import INTEGRATION_TESTING


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='twitter-controlpanel')
        view = view.__of__(self.portal)
        self.failUnless(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                          '@@twitter-controlpanel')

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertTrue('TwitterSettings' in actions)

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertTrue('TwitterSettings' not in actions)


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING
    record = 'collective.twitter.accounts'

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_record_in_registry(self):
        self.assertTrue(self.record in self.registry.records,
                        'record is not in configuration registry')

    def test_record_removed_from_registry(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        self.assertTrue(self.record not in self.registry.records,
                         'record still in configuration registry')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
