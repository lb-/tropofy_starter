from simplekml import Kml

from sqlalchemy.schema import Column, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.types import Float, Integer, Text

from tropofy.app import AppWithDataSets, Step, StepGroup
from tropofy.database.tropofy_orm import DataSetMixin
from tropofy.widgets import Chart, KMLMap, SimpleGrid


class PeformanceBarChart(Chart):
    def get_chart_type(self, app_session):
        return Chart.BARCHART

    def get_table_schema(self, app_session):
        return {
            'year': ('string', 'Year'),
            'sales': ('number', 'Sales'),
            'expenses': ('number', 'expenses'),
        }

    def get_table_data(self, app_session):
        results = []
        years = [
            year for row in
            app_session.data_set.query(Performance.year).distinct()
            for year in row
        ]
        for year in years:
            performances = app_session.data_set.query(
                Performance).filter_by(year=year)
            results.append({
                'year': year,
                'sales': sum(p.sales for p in performances),
                'expenses': sum(p.expenses for p in performances)
            })
        return results

    def get_column_ordering(self, app_session):
        return ['year', 'sales', 'expenses']

    def get_order_by_column(self, app_session):
        return 'year'

    def get_chart_options(self, app_session):
        return {
            'title': 'Company Performance',
            'vAxis': {
                'title': 'year',
                'titleTextStyle': {'color': 'red'}
            }
        }


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
        step_groups = []

        step_group_1 = StepGroup(name='Input')
        step_group_1.add_step(
            Step(name='Stores', widgets=[SimpleGrid(Store)]))
        step_group_1.add_step(
            Step(name='Performances', widgets=[SimpleGrid(Performance)]))
        step_groups.append(step_group_1)

        step_group_2 = StepGroup(name='Output')
        step_group_2.add_step(
            Step(name='Map', widgets=[MyKMLMap()]))
        step_group_2.add_step(
            Step(name='Chart', widgets=[PeformanceBarChart()]))
        step_groups.append(step_group_2)

        return step_groups
