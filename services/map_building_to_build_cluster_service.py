import geopandas as gpd

from interfaces.map_building_to_building_cluster_interface import (
    MapBuildingToBuildingClusterInterface,
)
from utils.dataframe_util import (
    SaveFile,
    AddColumn,
)


class MapBuildingToBuildingClusterService(MapBuildingToBuildingClusterInterface):
    def map_building_to_building_cluster(
        self,
        building_cluster_polygons: gpd.GeoDataFrame,
        building_points: gpd.GeoDataFrame,
    ) -> None:
        merged_building_and_building_cluster: gpd.GeoDataFrame = self._merge(
            building_cluster_polygons=building_cluster_polygons,
            building_points=building_points,
        )

        merged_building_and_building_cluster = (
            AddColumn.convert_xy_to_longitude_and_latitude(
                df=merged_building_and_building_cluster,
                x_key="건물중심점_x좌표",
                y_key="건물중심점_y좌표",
            )
        )

        merged_building_and_building_cluster = merged_building_and_building_cluster[
            ["latitude", "longitude"]
        ]

        SaveFile.df_to_csv(
            df=merged_building_and_building_cluster,
            file_name="merged.csv",
        )

    def _merge(
        self,
        building_cluster_polygons: gpd.GeoDataFrame,
        building_points: gpd.GeoDataFrame,
    ) -> gpd.GeoDataFrame:
        # 빌딩 클러스터 폴리곤 안에 속하는 빌딩 join
        merged_building_and_building_cluster = gpd.sjoin(
            building_cluster_polygons,
            building_points,
            how="inner",
            predicate="contains",
        )

        return merged_building_and_building_cluster
