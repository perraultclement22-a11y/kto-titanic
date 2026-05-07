export MLFLOW_S3_ENDPOINT_URL=http://minio-api-perrault-clement-dev.apps.rm1.0a51.p1.openshiftapps.com
export AWS_ACCESS_KEY_ID=minio
export AWS_SECRET_ACCESS_KEY=minio123
uv run python ./src/titanic/training/main.py --input_data_path "titanic.csv" --n_estimators 100 --max_depth 10 --random_state 42
