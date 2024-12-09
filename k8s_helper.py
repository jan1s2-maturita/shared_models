from kubernetes import client, config
class Kubernetes:
    def __init__(self, key, url):
        self.configuration = client.Configuration()
        self.configuration.api_key['authorization'] = key
        self.configuration.api_key_prefix['authorization'] = 'Bearer'
        self.configuration.host = url
        self.configuration.verify_ssl = False
        self.v1 = client.CoreV1Api(client.ApiClient(self.configuration))
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

    def create_in_k8s(self, db, user_id, image_id):
        if not self.namespace_exists(user_id):
            self.create_namespace(user_id)
        manifest = db.get_image_manifest(image_id)
        return self.v1.create_namespaced_pod(user_id, manifest)

    def delete_deploy(self, user_id, image_id):
        return self.v1.delete_namespaced_pod(image_id, namespace=user_id)


