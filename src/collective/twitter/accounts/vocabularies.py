# -*- coding: utf-8 -*-

from zope.component import getUtility
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

from plone.registry.interfaces import IRegistry


class AccountsVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        registry = getUtility(IRegistry)
        accounts = registry['collective.twitter.accounts']
        if accounts:
            vocab = accounts.keys()
        else:
            vocab = []

        return SimpleVocabulary.fromValues(vocab)
