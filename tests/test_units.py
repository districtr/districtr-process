from districtr_process.units import Units
from districtr_process.column_set import ColumnSet
from districtr_process.columns import PopulationColumn
import pytest


@pytest.fixture
def units_with_problems():
    return Units(
        "lowell",
        "Lowell",
        "precinct",
        [
            ColumnSet(
                "population",
                "Population",
                total=None,
                subgroups=[
                    PopulationColumn("Data", "data"),
                    PopulationColumn("Data 2", "data2"),
                    PopulationColumn(
                        "Data 3", "data3"
                    ),  # should error because values are strings
                ],
            )
        ],
    )


class TestUnits:
    def test_raises_for_bad_columns(self, units_with_problems, gdf_with_data):
        with pytest.raises(ValueError):
            units_with_problems.raise_for_problems(gdf_with_data)

    def test_can_get_problems(self, gdf_with_data, units_with_problems):
        problems = units_with_problems.problems(gdf_with_data)
        assert len(problems) > 0
