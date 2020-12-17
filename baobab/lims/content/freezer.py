# -*- coding: utf-8 -*-
#
# This file is part of Bika LIMS
#
# Copyright 2011-2017 by it's authors.
# Some rights reserved. See LICENSE.txt, AUTHORS.txt.
from baobab.lims import bikaMessageFactory as _
from Products.Archetypes.public import *
from bika.lims.browser.widgets import ReferenceWidget as bika_ReferenceWidget
from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.Archetypes.public import Schema
from Products.Archetypes.public import registerType
from bika.lims.content.bikaschema import BikaSchema
from zope.interface import implements
from baobab.lims import config
from Products.CMFPlone.interfaces import IConstrainTypes
from baobab.lims.interfaces import IFreezer
from Products.Archetypes.public import BaseContent

StorageUnit = ReferenceField(
    'StorageUnit',
    allowed_types=('StorageUnit',),
    relationship='FreezerStorageUnit',
    widget=bika_ReferenceWidget(
        label=_("Storage Unit"),
        description=_("The storage unit associated with this freezer"),
        size=40,
        visible={'edit': 'visible',
                 'view': 'visible',
                 },
        catalog_name='portal_catalog',
        # base_query={'inactive_state': 'active',
        #             'review_state': 'available',
        #             },
        # colModel=[{'columnName': 'UID', 'hidden': True},
        #           {'columnName': 'Title', 'width': '50', 'label': _('Title')}
        #           ],
    )
)

schema = BikaSchema.copy() + Schema((
    StorageUnit,
))

schema['description'].schemata = 'default'
schema['description'].widget.visible = True



class Freezer(BaseContent):
    security = ClassSecurityInfo()
    implements(IFreezer, IConstrainTypes)
    displayContentsTab = False
    schema = schema
    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from bika.lims.idserver import renameAfterCreation
        renameAfterCreation(self)
    #
    # def Title(self):
    #     return safe_unicode(self.getField('SampleDonorID').get(self)).encode('utf-8')
    #
    # def Description(self):
    #     return "Gender %s : Age %s %s" % (self.getSex(), self.getAge(), self.getAgeUnit())
    #
    # def getSexes(self):
    #     return ['Male', 'Female', 'Unknown', 'Undifferentiated']
    #
    # def getAgeUnits(self):
    #     return ['Years', 'Months', 'Weeks', 'Days', 'Hours', 'Minutes']

registerType(Freezer, config.PROJECTNAME)