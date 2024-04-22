from commands.map_building_to_building_cluster_command import (
    MapBuildingToBuildingClusterCommand,
)


def test_when_map_building_to_building_cluster_then_success():
    MapBuildingToBuildingClusterCommand().map()
