export MLFLOW_TRACKING_URI=http://mlflow-perrault-clement-dev.apps.rm1.0a51.p1.openshiftapps.com
export MLFLOW_S3_ENDPOINT_URL=http://minio-api-perrault-clement-dev.apps.rm1.0a51.p1.openshiftapps.com
export AWS_ACCESS_KEY_ID=minio
export AWS_SECRET_ACCESS_KEY=minio123

uv run python -c "
import mlflow
import joblib
import pickle

client = mlflow.MlflowClient()
runs = client.search_runs(experiment_ids=['1'], order_by=['start_time DESC'], max_results=1)
if runs:
    run_id = runs[0].info.run_id
    print(f'Downloading model from run {run_id}')
    path = client.download_artifacts(run_id, 'model_final/model_final.joblib', './src/titanic/api/resources/')
    model = joblib.load('./src/titanic/api/resources/model_final.joblib')
    with open('./src/titanic/api/resources/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print('Model downloaded and saved as model.pkl')
else:
    print('No runs found!')
"
