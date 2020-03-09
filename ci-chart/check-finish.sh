#!/bin/bash

duration=$1
namespace=$2
curr=0
while ([[ $(kubectl get pods -l app=api -n $namespace -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]] ||
      [[ $(kubectl get pods -l app=app -n $namespace -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]] ||
      [[ $(kubectl get pods -l app=nginx -n $namespace -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]] ||
      [[ $(kubectl get pods -l app=redis -n $namespace -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]] ||
      [[ $(kubectl get pods -l app=worker -n $namespace -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]] ||
      [[ $(kubectl get pods -l app=postgres -n $namespace -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]]) &&
      [ $curr -lt $duration ]; do 
    curr=$[$curr + 1]
    echo "waiting for finish-pod: $curr/$duration" && sleep 1; 
done

if [[ "$curr" == "$duration" ]]; then
  exit 1
fi
echo "All Done"