from simplekml import Kml

from sqlalchemy.schema import Column, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.types import Float, Integer, Text

from tropofy.app import AppWithDataSets, Step, StepGroup
from tropofy.database.tropofy_orm import DataSetMixin
from tropofy.widgets import KMLMap, SimpleGrid


class Store(DataSetMixin):
    name = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    @classmethod
    def get_table_args(cls):
        return (UniqueConstraint('name', 'data_set_id'),)


class Performance(DataSetMixin):
    store_name = Column(Text, nullable=False)
    year = Column(Integer, nullable=False)
    sales = Column(Float, nullable=False, default=0)
    expenses = Column(Float, nullable=False, default=0)

    @classmethod
    def get_table_args(cls):
        return (
            UniqueConstraint(
                'store_name',
                'year',
                'data_set_id'
            ),
            ForeignKeyConstraint(
                ['store_name', 'data_set_id'],
                ['store.name', 'store.data_set_id'],
                ondelete='CASCADE',
                onupdate='CASCADE',
            ),
        )


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
                name='Performances',
                steps=[
                    Step(
                        name='Performances',
                        widgets=[SimpleGrid(Performance)]
                    )
                ]
            ),
            StepGroup(
                name='Map',
                steps=[
                    Step(name='Map', widgets=[MyKMLMap()])
                ]
            )
        ]
