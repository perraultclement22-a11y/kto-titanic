import logging
import os
from pathlib import Path

import boto3
import pandas as pd


ARTIFACT_PATH = "path_output"
PROFILING_PATH = "profiling_reports"


def load_data(path: str) -> str:
  logging.warning(f"load_data on path : {path}")

  Path("./dist/").mkdir(parents=True, exist_ok=True)
  local_path = Path("./dist/", "data.csv")
  logging.warning(f"to path : {local_path}")

  s3_client = boto3.client(
    "s3",
    endpoint_url=os.environ.get("MLFLOW_S3_ENDPOINT_URL"),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
  )

  s3_client.download_file("kto-titanic", path, local_path)
  df = pd.read_csv(local_path)
  logging.warning(f"data loaded, shape : {df.shape}")

  return local_path
