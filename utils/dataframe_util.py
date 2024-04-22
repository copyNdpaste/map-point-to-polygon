import os
import pandas as pd
import geopandas as gpd

from pyproj import Proj, transform
from typing import List, Optional, Union


class ReadDataFrame:
    @staticmethod
    def read(file_name: str):
        return gpd.read_file(
            os.path.join(os.getcwd(), file_name),
            encoding="cp949",
        )


class ModifyColumns:
    @staticmethod
    def rename(polygons_and_entrances: pd.DataFrame) -> gpd.GeoDataFrame:
        return polygons_and_entrances.rename(
            columns={
                "geometry_x": "geometry",
            },
            inplace=False,
        )


class AddColumn:
    @staticmethod
    def convert_xy_to_geometry(
        df: gpd.GeoDataFrame,
        x_key: str,
        y_key: str,
        from_crs: str = None,
        to_crs: str = None,
    ):
        df["geometry"] = gpd.points_from_xy(
            df[x_key],
            df[y_key],
            crs=from_crs,
        )

        return gpd.GeoDataFrame(
            df,
            geometry="geometry",
        ).to_crs({"init": to_crs})



    @staticmethod
    def convert_xy_to_longitude_and_latitude(
        df: gpd.GeoDataFrame, x_key: str, y_key: str
    ) -> gpd.GeoDataFrame:
        epsg5179 = Proj(init="epsg:5179")
        wgs84 = Proj(init="epsg:4326")

        longitude, latitude = transform(
            epsg5179,
            wgs84,
            df[x_key],
            df[y_key],
        )

        df["latitude"] = latitude
        df["longitude"] = longitude

        return df


class ConvertFile:
    @staticmethod
    def convert_csv_to_df(file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path, dtype=str)

    @staticmethod
    def convert_txt_to_df(file_path: str, columns: List[str]) -> pd.DataFrame:
        return pd.read_csv(
            file_path,
            sep="|",
            engine="python",
            encoding="cp949",
            names=columns,
            dtype=str,
        )


class SaveFile:
    @staticmethod
    def df_to_csv(
        df: Union[gpd.GeoDataFrame, pd.DataFrame], file_name: str
    ) -> Optional[str]:
        return df.to_csv(os.path.join(os.getcwd(), file_name), index=False)


class DropRows:
    @staticmethod
    def drop(
        stations: gpd.GeoDataFrame, to_be_dropped_ids: List[str]
    ) -> gpd.GeoDataFrame:
        return stations.drop(stations.query("id in @to_be_dropped_ids").index)


class MergeDataFrame:
    @staticmethod
    def merge_inner(
        left: pd.DataFrame, right: pd.DataFrame, on: List[str]
    ) -> pd.DataFrame:
        return pd.merge(left=left, right=right, how="inner", on=on)

    @staticmethod
    def spatial_join(
        left: pd.DataFrame, right: pd.DataFrame, how: str, predicate: str
    ) -> gpd.GeoDataFrame:
        return gpd.sjoin(left, right, how=how, predicate=predicate)


class ModifyDataFrame:
    @staticmethod
    def modify_to_epsg_4326(df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        df = df.set_geometry("geometry")
        df.crs = "epsg:4326"
        return df
