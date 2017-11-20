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
