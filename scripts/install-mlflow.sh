#!/bin/bash
oc apply -f https://raw.githubusercontent.com/guillaume-thomas/kto-mlflow/main/k8s/minio.yml
oc apply -f https://raw.githubusercontent.com/guillaume-thomas/kto-mlflow/main/k8s/mysql.yml
oc apply -f https://raw.githubusercontent.com/guillaume-thomas/kto-mlflow/main/k8s/mlflow.yml
oc apply -f https://raw.githubusercontent.com/guillaume-thomas/kto-mlflow/main/k8s/dailyclean.yml
