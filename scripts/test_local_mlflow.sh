export KUBE_MLFLOW_TRACKING_URI=http://mlflow-perrault-clement-dev.apps.rm1.0a51.p1.openshiftapps.com
export MLFLOW_TRACKING_URI=http://mlflow-perrault-clement-dev.apps.rm1.0a51.p1.openshiftapps.com
export MLFLOW_S3_ENDPOINT_URL=http://minio-api-perrault-clement-dev.apps.rm1.0a51.p1.openshiftapps.com
export AWS_ACCESS_KEY_ID=minio
export AWS_SECRET_ACCESS_KEY=minio123

uv run mlflow run ./src/titanic/training -e main --env-manager=local -P path=titanic.csv --experiment-name kto-titanic
