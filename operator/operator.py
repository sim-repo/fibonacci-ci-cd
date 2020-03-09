import kopf
import yaml
import kubernetes
import kubernetes.client as k8s
import time
from jinja2 import Environment, FileSystemLoader
import random

def render_template(filename, vars_dict):
    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template(filename)
    yaml_manifest = template.render(vars_dict)
    json_manifest = yaml.load(yaml_manifest)
    return json_manifest


@kopf.on.create('otus.homework', 'v1', 'ci')
def on_create(body, spec, **kwargs):

    tmp_namespace = body['spec']['tmp_namespace']
    image_postgres = body['spec']['image_postgres']
    image_redis = body['spec']['image_redis']
    image_api = body['spec']['image_api']
    image_worker = body['spec']['image_worker']
    image_nginx = body['spec']['image_nginx']
    image_app = body['spec']['image_app']

    create_namespace(tmp_namespace)

    # 1. PG:
    pg_stateful = render_template('pg-stateful.yml.j2', {
        'namespace': tmp_namespace,
        'image_postgres': image_postgres
        }
    )

    pg_svc = render_template('pg-svc.yml.j2', {
        'namespace': tmp_namespace
        }
    )

    # 2. Redis:
    red_dep = render_template('redis-dep.yml.j2', {
        'namespace': tmp_namespace,
        'image_redis': image_redis
        }
    )

    red_svc = render_template('redis-svc.yml.j2', {
        'namespace': tmp_namespace
        }
    )

    # 3. API:
    api_dep = render_template('api-dep.yml.j2', {
        'namespace': tmp_namespace,
        'image_api': image_api
        }
    )

    api_svc = render_template('api-svc.yml.j2', {
        'namespace': tmp_namespace
        }
    )

    # 4. Worker:
    worker_dep = render_template('worker-dep.yml.j2', {
        'namespace': tmp_namespace,
        'image_worker': image_worker
        }
    )


    # 5. nginx:
    nginx_dep = render_template('nginx-dep.yml.j2', {
        'namespace': tmp_namespace,
        'image_nginx': image_nginx
        }
    )

    nginx_svc = render_template('nginx-svc.yml.j2', {
        'namespace': tmp_namespace
        }
    )

    #6. app
    app_dep = render_template('app-dep.yml.j2', {
        'namespace': tmp_namespace,
        'image_app': image_app
        }
    )

    app_svc = render_template('app-svc.yml.j2', {
        'namespace': tmp_namespace
        }
    )

    #7. ingress
    ingress = render_template('ingress.yml.j2', {
        'namespace': tmp_namespace
        }
    )


    success_finish_dep = render_template('finish-deployment.yml.j2', {
        'namespace': tmp_namespace }
    )



    ### dependencies: ###
    #pg:
    kopf.append_owner_reference(pg_stateful, owner=body)
    kopf.append_owner_reference(pg_svc, owner=body)
    #redis:
    kopf.append_owner_reference(red_dep, owner=body)
    kopf.append_owner_reference(red_svc, owner=body)
    #api:
    kopf.append_owner_reference(api_dep, owner=body)
    kopf.append_owner_reference(api_svc, owner=body)
    #worker:
    kopf.append_owner_reference(worker_dep, owner=body)
    #nginx:
    kopf.append_owner_reference(nginx_dep, owner=body)
    kopf.append_owner_reference(nginx_svc, owner=body)
    #app:
    kopf.append_owner_reference(app_dep, owner=body)
    kopf.append_owner_reference(app_svc, owner=body)
    #ingress:
    kopf.append_owner_reference(ingress, owner=body)
    #finish:
    kopf.append_owner_reference(success_finish_dep, owner=body)


    core_v1 = kubernetes.client.CoreV1Api()
    api = kubernetes.client.AppsV1Api()

    ### deploy: ###
    #pg:
    api.create_namespaced_stateful_set(tmp_namespace, pg_stateful)
    core_v1.create_namespaced_service(tmp_namespace, pg_svc)
    #redis:
    api.create_namespaced_deployment(tmp_namespace, red_dep)
    core_v1.create_namespaced_service(tmp_namespace, red_svc)
    #api:
    api.create_namespaced_deployment(tmp_namespace, api_dep)
    core_v1.create_namespaced_service(tmp_namespace, api_svc)
    #worker:
    api.create_namespaced_deployment(tmp_namespace, worker_dep)
    #nginx:
    api.create_namespaced_deployment(tmp_namespace, nginx_dep)
    core_v1.create_namespaced_service(tmp_namespace, nginx_svc)
    #app
    api.create_namespaced_deployment(tmp_namespace, app_dep)
    core_v1.create_namespaced_service(tmp_namespace, app_svc)
    #ingress
    ext = kubernetes.client.ExtensionsV1beta1Api()
    ext.create_namespaced_ingress(tmp_namespace, ingress)

    api.create_namespaced_deployment(tmp_namespace, success_finish_dep)
    



# namespaces >>>>>>>>>>>>>>>>>>>>>

def create_namespace(namespace: str):
    core_v1 = k8s.CoreV1Api()

    try:
        core_v1.delete_namespace(namespace)
    except kubernetes.client.rest.ApiException:
        pass

    time.sleep(10)
    core_v1.create_namespace( body={
                              "metadata": {
                                  "name": namespace
                                  }
                              })

def _delete_namespace(ns_name: str) -> None:
    core_v1 = k8s.CoreV1Api()
    core_v1.delete_namespace(ns_name)

# namespaces <<<<<<<<<<<<<<<<<<<<<<<<<
