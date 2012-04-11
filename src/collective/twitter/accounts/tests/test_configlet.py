# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.registry.interfaces import IRegistry

from collective.twitter.accounts import config

from collective.twitter.accounts.testing import INTEGRATION_TESTING

class RegistryTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        # set up settings registry
        self.registry = getUtility(IRegistry)

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
                          
    def test_record_in_registry(self):
        self.failUnless("collective.twitter.accounts" in self.registry.records,
                    'record is not in configuration registry')


class RegistryUninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.registry = getUtility(IRegistry)
        # uninstall the package
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[config.PROJECTNAME])
        
    def test_record_removed_from_registry(self):
        self.failIf("collective.twitter.accounts" in self.registry.records,
                    'record still in configuration registry')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)