from abc import ABC, abstractmethod

import geopandas as gpd
import pandas as pd


class MapBuildingToBuildingClusterInterface(ABC):
    @abstractmethod
    def map_building_to_building_cluster(
        self,
        building_cluster_polygons: gpd.GeoDataFrame,
        building_polygons: gpd.GeoDataFrame,
    ) -> None:
        pass

    @abstractmethod
    def _merge(
        self,
        building_cluster_polygons: gpd.GeoDataFrame,
        building_polygons: gpd.GeoDataFrame,
    ) -> pd.DataFrame:
        pass
