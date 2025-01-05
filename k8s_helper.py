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
        self.configuration.debug = True
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
        if not self.namespace_exists(str(user_id)):
            self.create_namespace(str(user_id))
        manifest = db.get_image_manifest(challenge_id)
        manifest_service = db.get_service_manifest(challenge_id)
        response = []
        if manifest:
            print(manifest)
            json_manifest = json.loads(manifest)
            print(json_manifest)
            json_manifest['metadata']['name'] = str(challenge_id)
            response.append(create_from_dict(self.client, json_manifest, namespace=user_id))
        if manifest_service:
            json_manifest_service = json.loads(manifest_service)
            print(json_manifest_service)
            json_manifest_service['metadata']['name'] = str(challenge_id)
            response.append(create_from_dict(self.client, json_manifest_service, namespace=user_id))
        return response

    def delete_deploy(self, user_id, challenge_id):
        self.v1.delete_namespaced_service(challenge_id, namespace=user_id)
        return self.v1.delete_namespaced_pod(challenge_id, namespace=user_id)
    # access box name is "accessbox_user_id" in namespace user_id
    def execute_command(self, user_id, command):
        try:
            self.v1.connect_get_namespaced_pod_exec("accessbox", user_id, command=command, stderr=True, stdin=False, stdout=True, tty=False)
            return True
        except Exception as e:
            return False
    def get_logs(self, user_id):
        try:
            data = self.v1.read_namespaced_pod_log("accessbox", user_id)
            return data
        except Exception as e:
            return None
    def create_accessbox(self, user_id):
        if not self.namespace_exists(user_id):
            self.create_namespace(user_id)
        body = client.V1Pod(metadata=client.V1ObjectMeta(name="accessbox"), spec=client.V1PodSpec(containers=[client.V1Container(name="accessbox", image="kalilinux/kali-last-release:latest", command=["sleep", "7200"])]))
        return self.v1.create_namespaced_pod(namespace=user_id, body=body)


