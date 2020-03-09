#!/bin/bash

namespace=$1

function try() {
    [[ $- = *e* ]]; SAVED_OPT_E=$?
    set +e
}

function throw() {
    exit $1
}

function catch() {
    export ex_code=$?
    (( $SAVED_OPT_E )) && set +e
    return $ex_code
}

function throwErrors() {
    set -e
}

function ignoreErrors() {
    set +e
}

export CrdDelException=99
export NSException=100
export HelmException=101
export CrdException=102
export OperatorException=103


try
(   
    [[ $(kubectl delete crd ci.otus.homework micro-service) ]] # remove crd
    [[ $(kubectl delete pvc -l app=postgres -n $namespace) ]] # remove pvc
    [[ $(kubectl delete deployment ci-operator -n stages) ]] # remove operator
    [[ $(kubectl create namespace $namespace) ]] # create ns
    [[ $(helm del cichart) ]] # remove chart-release
    [[ $(kubectl apply -f ./operator/crd.yml) ]] # create crt
    [[ $(kubectl apply -f ./operator/operator.yml) ]] # create operator
    echo "finished"
)



catch || {
    case $ex_code in
        $NSException)
            echo "Error has occured: namespace"
        ;;
        $HelmException)
            echo "Error has occured: helm"
        ;;
        $CrdException)
            echo "Error has occured: crd"
        ;;
        $OperatorException)
            echo "Error has occured: operator"
        ;;
        *)
            echo "An unexpected exception was thrown"
            throw $ex_code
        ;;
    esac
}


