from kubernetes import client, config
from kubernetes.utils import create_from_dict
import json

from .db_connect import Database

class Kubernetes:
    def __init__(self, key, url):
        self.configuration = client.Configuration()
        self.configuration.api_key['authorization'] = key
        self.configuration.api_key_prefix['authorization'] = 'Bearer'
        self.configuration.host = url
        self.configuration.verify_ssl = False
        self.client = client.ApiClient(self.configuration)
        self.v1 = client.CoreV1Api(self.client)
    def get_k8s_config(self):
        return self.v1
    def create_namespace(self, name: str):
        body = client.V1Namespace(metadata=client.V1ObjectMeta(name=name))
        return self.v1.create_namespace(body)

    def namespace_exists(self, name: str):
        namespaces = self.v1.list_namespace()
        for ns in namespaces.items:
            if ns.metadata.name == name:
                return True
        return False

    def create_in_k8s(self, db: Database, user_id, challenge_id):
        if not self.namespace_exists(user_id):
            self.create_namespace(user_id)
        manifest = db.get_image_manifest(challenge_id)
        manifest_service = db.get_service_manifest(challenge_id)
        response = []
        if manifest:
            json_manifest = json.loads(manifest)
            response.append(create_from_dict(self.client, json_manifest, namespace=user_id))
        if manifest_service:
            json_manifest_service = json.loads(manifest_service)
            response.append(create_from_dict(self.client, json_manifest_service, namespace=user_id))
        return response

    def delete_deploy(self, user_id, challenge_id):
        self.v1.delete_namespaced_service(challenge_id, namespace=user_id)
        return self.v1.delete_namespaced_pod(challenge_id, namespace=user_id)


