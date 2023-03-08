from git import Repo
import json
import os
from pathlib import Path
import requests
from rocrate.rocrate import ROCrate
from rocrate.model.contextentity import ContextEntity
import shutil


def instantiate_rocrate(path, profile):
    crate = ROCrate()
    context_entity = crate.add(
        ContextEntity(
            crate,
            identifier=profile,
            properties={
                "@type": "CreativeWork",
                "name": "<name>",
                "version": "<version>"
            },
        )
    )
    crate.root_dataset["conformsTo"] = context_entity
    crate.write(path)


def clone_profile_crate_repo(data_rocrate_path, profile_rocrate_path):
    crate = ROCrate(data_rocrate_path)
    profile_uri = crate.root_dataset["conformsTo"]["@id"]
    response = requests.get(f"{profile_uri}/ro-crate-metadata.json")
    with open("/ro-crate-metadata.json", "w") as f:
        f.write(response.content.decode("utf-8"))
    profile_crate = ROCrate("/")
    profile_crate_repo = profile_crate.root_dataset["crateRepo"]
    Repo.clone_from(profile_crate_repo, profile_rocrate_path)
    shutil.rmtree(profile_rocrate_path / Path(".git"))


def get_sembench_config_path(path):
    return Path(ROCrate(path).root_dataset["sembenchConfigPath"])


if __name__ == "__main__":
    GITHUB_WORKSPACE = Path("/github/workspace")
    SEMBENCH_WORKSPACE = Path("~sembench_data_cache")
    PROFILE = os.getenv("PROFILE")

    if not (GITHUB_WORKSPACE / Path("ro-crate-metadata.json")).exists():
        instantiate_rocrate(GITHUB_WORKSPACE, PROFILE)

    clone_profile_crate_repo(
        data_rocrate_path=GITHUB_WORKSPACE,
        profile_rocrate_path=GITHUB_WORKSPACE / SEMBENCH_WORKSPACE
    )

    SEMBENCH_CONFIG_PATH = get_sembench_config_path(GITHUB_WORKSPACE / SEMBENCH_WORKSPACE)

    sembench_kwargs = {
        "INPUT_DATA_LOCATION": str(GITHUB_WORKSPACE),
        "SEMBENCH_DATA_LOCATION": str(GITHUB_WORKSPACE / SEMBENCH_WORKSPACE),
        "SEMBENCH_CONFIG_PATH": str(GITHUB_WORKSPACE / SEMBENCH_WORKSPACE / SEMBENCH_CONFIG_PATH),
    }

    with open(GITHUB_WORKSPACE / Path("~sembench_kwargs.json"), "w") as f:
        json.dump(sembench_kwargs, f)
