import os
import sys
from typing import List

from client_models.collection import Collection
from utils.config import Config
from utils.exceptions import CollectionNotFound

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from client_models.collection_config import CollectionConfig
from server_models.api import (
    CreateCollectionRequest,
    ListCollectionsResponse,
    DeleteCollectionRequest,
)


class NautilusDB:
    @classmethod
    def init(cls, api_key: str = None, account_name: str = Config.DEMO_ACCOUNT):
        Config.api_key = api_key
        Config.account_name = account_name

    @classmethod
    def create_collection(
            cls,
            collection_name: str,
            config: CollectionConfig = CollectionConfig.file_upload()) -> Collection:
        config.validate()
        url = Config.get_base_url() + '/collections/create'
        req = CreateCollectionRequest(name=collection_name,
                                      dimension=config.dimension,
                                      description=config.description,
                                      metas=config.metadata_columns)
        Config.post(url=url, data=req.model_dump_json())
        return Collection(collection_name)

    @classmethod
    def collection(cls, collection_name: str) -> Collection:
        return Collection(collection_name)

    @classmethod
    def list_collections(cls) -> List[Collection]:
        url = Config.get_base_url() + '/collections/list'
        resp = Config.get(url=url)
        return [Collection(name) for name in
                ListCollectionsResponse.model_validate(resp.json()).names]

    @classmethod
    def delete_collection(cls, collection_name: str):
        req = DeleteCollectionRequest(name=collection_name)
        url = Config.get_base_url() + '/collections/delete'
        Config.post(url=url, data=req.model_dump_json())


if __name__ == '__main__':
    NautilusDB.create_collection("rkang-test-ut")
    NautilusDB.list_collections()
    try:
        NautilusDB.delete_collection("rkang-test-ut-dne")
    except CollectionNotFound:
        pass

    NautilusDB.delete_collection("rkang-test-ut")
