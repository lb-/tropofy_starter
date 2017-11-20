"""
Author:      www.tropofy.com

Copyright 2015 Tropofy Pty Ltd, all rights reserved.

This source file is part of Tropofy and governed by the Tropofy terms of service
available at: http://www.tropofy.com/terms_of_service.html

This source file is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the license files for details.
"""

from collections import OrderedDict

from sqlalchemy.schema import Column
from sqlalchemy.types import Float, Text

from tropofy.app import AppWithDataSets, Step, StepGroup
from tropofy.database.tropofy_orm import DataSetMixin
from tropofy.widgets import SimpleGrid


class Store(DataSetMixin):
    name = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)


class MyFirstApp(AppWithDataSets):
    def get_name(self):
        return "My First App"

    def get_gui(self):
        return OrderedDict([
            ('stores', StepGroup(
                name='Stores',
                steps=OrderedDict([
                    ('stores', Step(
                        name='Stores',
                        widgets=[SimpleGrid(Store)]
                    ))
                ]),
            )),
        ])
