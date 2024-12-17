from services.deploy_type.deploy_type import DeployType


def get_deploy_types():
    return [
        DeployType("deploy_type_bluegreen", "Services - Blue Green"),
        DeployType("deploy_type_safe", "Services - Safe"),
        DeployType("deploy_type_rolling_update", "Services - Rolling Update"),
        DeployType("deploy_type_canary", "Services - Canary"),
        DeployType("deploy_type_config_bluegreen", "Configurations - Blue Green"),
        DeployType("deploy_type_config_rolling_update", "Configurations - Rolling Update"),
        DeployType("deploy_type_config_canary", "Configurations - Canary"),
    ]
