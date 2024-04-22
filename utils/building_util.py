import os

import geopandas as gpd

from utils.dataframe_util import (
    AddColumn,
    ConvertFile,
    ModifyDataFrame,
    ReadDataFrame,
)

build_columns = [
    "주소관할읍면동코드",
    "시도명",
    "시군구명",
    "읍면동명",
    "도로명코드",
    "도로명",
    "지하여부",
    "건물본번",
    "건물부번",
    "우편번호",
    "건물관리번호",
    "시군구용건물명",
    "건축물용도분류",
    "행정동코드",
    "행정동명",
    "지상층수",
    "지하층수",
    "공동주택구분",
    "건물수",
    "상세건물명",
    "건물명변경이력",
    "상세건물명변경이력",
    "거주여부",
    "건물중심점_x좌표",
    "건물중심점_y좌표",
    "출입구_x좌표",
    "출입구_y좌표",
    "시도명(영문)",
    "시군구명(영문)",
    "읍면동명(영문)",
    "도로명(영문)",
    "읍면동구분",
    "이동사유코드",
]


class BuildingUtil:
    @staticmethod
    def get_building_points(file_name: str) -> gpd.GeoDataFrame:
        building_file_path = os.path.join(os.getcwd(), file_name)

        building_df = ConvertFile.convert_txt_to_df(
            file_path=building_file_path, columns=build_columns
        )

        building_df = AddColumn.convert_xy_to_geometry(
            x_key="건물중심점_x좌표",
            y_key="건물중심점_y좌표",
            df=building_df,
            from_crs="epsg:5179",
            to_crs="epsg:4326",
        )

        return building_df

    @staticmethod
    def get_building_polygons(file_name: str) -> gpd.GeoDataFrame:
        building_polygons = ReadDataFrame.read(file_name)

        building_polygons = ModifyDataFrame.modify_to_epsg_4326(building_polygons)

        return building_polygons

    @staticmethod
    def get_building_cluster_polygons(file_name: str) -> gpd.GeoDataFrame:
        building_cluster_polygons = ReadDataFrame.read(
            file_name=file_name
        )

        building_cluster_polygons = ModifyDataFrame.modify_to_epsg_4326(
            df=building_cluster_polygons
        )

        return building_cluster_polygons
