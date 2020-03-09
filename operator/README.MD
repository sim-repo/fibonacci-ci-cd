cd ./operator
docker build -t neogeowild/micro-service:latest .
docker push neogeowild/micro-service:latest



kubectl delete crd ci.otus.homework micro-service

kubectl delete cr ci.otus.homework micro-service
a
apply cr.yml

kubectl delete pvc postgres-micro-service -n ranbow

kubectl delete pv -l app=postgres -n tmp


k get pv -n ranbow
k get pvc -n ranbow

