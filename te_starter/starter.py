from collections import OrderedDict

from simplekml import Kml

from sqlalchemy.schema import Column
from sqlalchemy.types import Float, Text

from tropofy.app import AppWithDataSets, Step, StepGroup
from tropofy.database.tropofy_orm import DataSetMixin
from tropofy.widgets import KMLMap, SimpleGrid


class Store(DataSetMixin):
    name = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)


class MyKMLMap(KMLMap):
    def get_kml(self, app_session):
        kml = Kml()
        stores = app_session.data_set.query(Store).all()
        for store in stores:
            kml.newpoint(
                name=store.name,
                coords=[(store.longitude, store.latitude)]
            )
        return kml.kml()


class MyFirstApp(AppWithDataSets):
    def get_name(self):
        return 'Starter App'

    def get_gui(self):
        return [
            StepGroup(
                name='Stores',
                steps=[
                    Step(name='stored', widgets=[SimpleGrid(Store)])
                ]
            ),
            StepGroup(
                name='Map',
                steps=[
                    Step(name='Map', widgets=[MyKMLMap()])
                ]
            )
        ]
