import geopandas as gpd
from pyogrio import set_gdal_config_options
from flask import Flask

from services.map_building_to_build_cluster_service import (
    MapBuildingToBuildingClusterService,
)
from utils.building_util import BuildingUtil

set_gdal_config_options(
    {
        "SHAPE_RESTORE_SHX": "YES",
    }
)

app = Flask(__name__)


class MapBuildingToBuildingClusterCommand:
    def __init__(self) -> None:
        self.map_building_to_building_cluster = MapBuildingToBuildingClusterService()

    def map(self):
        building_points: gpd.GeoDataFrame = BuildingUtil.get_building_points(
            file_name="match_build_gwangju.txt"
        )

        building_cluster_polygons: gpd.GeoDataFrame = (
            BuildingUtil.get_building_cluster_polygons(
                file_name="building_cluster_polygons_4326.shp"
            )
        )

        self.map_building_to_building_cluster.map_building_to_building_cluster(
            building_cluster_polygons=building_cluster_polygons,
            building_points=building_points,
        )


@app.cli.command("map")
def map_command():
    MapBuildingToBuildingClusterCommand().map()
