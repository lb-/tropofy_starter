from simplekml import Kml

from sqlalchemy.schema import Column, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.types import Float, Integer, Text

from tropofy.app import AppWithDataSets, Step, StepGroup
from tropofy.database.tropofy_orm import DataSetMixin
from tropofy.widgets import Chart, KMLMap, SimpleGrid


def make_step_group(name, steps):
    """Make group where steps are an array of tuples with name, widgets."""
    step_group = StepGroup(name=name)
    for step in steps:
        step_name, step_widgets = step
        step_group.add_step(Step(name=step_name, widgets=step_widgets))
    return step_group


class StoreExpensesPieChart(Chart):
    def get_chart_type(self, app_session):
        return Chart.PIECHART

    def get_table_schema(self, app_session):
        return {
            'store': ('string', 'Store'),
            'expenses': ('number', 'expenses'),
        }

    def get_table_data(self, app_session):
        results = []
        stores = app_session.data_set.query(Store).all()
        for store in stores:
            performances = app_session.data_set.query(
                Performance).filter_by(store_name=store.name).all()
            results.append({
                'store': store.name,
                'expenses': sum(p.expenses for p in performances)
            })
        return results

    def get_column_ordering(self, app_session):
        return ['store', 'expenses']

    def get_chart_options(self, app_session):
        total_expense = sum(
            p.expenses for p in app_session.data_set.query(Performance).all()
        )
        title = 'Company Expenses: Total = ${expense}'.format(
            expense=str(total_expense))
        return {'title': title}


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


class Application(AppWithDataSets):
    def get_name(self):
        return 'Franchise Management'

    def get_examples(self):
        return {'Demo Data for Brisbane North': self.load_example_data}

    def get_gui(self):
        step_groups = []

        step_groups.append(
            make_step_group('Input', [
                ('Stores', [SimpleGrid(Store)]),
                ('Performances', [SimpleGrid(Performance)])
            ])
        )

        step_groups.append(
            make_step_group('Output', [
                ('Viz', [
                    {'widget': PeformanceBarChart(), 'cols': 6},
                    {'widget': StoreExpensesPieChart(), 'cols': 6},
                    {'widget': MyKMLMap(), 'cols': 12}
                ])
            ])
        )

        return step_groups

    @staticmethod  # to ensure self does not get passed in
    def load_example_data(app_session):
        app_session.data_set.add_all([
            Store(name="CLAYFIELD", latitude=-27.417536, longitude=153.056677),
            Store(name="SANDGATE", latitude=-27.321538, longitude=153.069267)
        ])

        app_session.data_set.add_all([
            Performance(
                store_name="CLAYFIELD", year=2011, sales=1000, expenses=400),
            Performance(
                store_name="CLAYFIELD", year=2012, sales=1170, expenses=460),
            Performance(
                store_name="SANDGATE", year=2011, sales=660, expenses=1120),
            Performance(
                store_name="SANDGATE", year=2012, sales=1030, expenses=540),
        ])
