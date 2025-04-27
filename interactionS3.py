from dotenv import load_dotenv
load_dotenv()
import os
import boto3
from fastapi import FastAPI
from botocore.exceptions import BotoCoreError, ClientError

app = FastAPI()

ROLE_ARN = os.getenv("ASSUME_ROLE_ARN")
REGION = os.getenv("AWS_DEFAULT_REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")
STATIC_FILE_PATH = "uploads/teste.jpg"
LIST_KEY = S3_KEY = "uploads/teste.jpg" 
MIME_TYPE = "image/jpeg"

def get_temporary_s3_client():
    sts = boto3.client("sts")
    
    response = sts.assume_role(
        RoleArn=ROLE_ARN,
        RoleSessionName="upload-session",
        DurationSeconds=900  # 15 min
    )

    creds = response["Credentials"]

    s3 = boto3.client(
        "s3",
        region_name=REGION,
        aws_access_key_id=creds["AccessKeyId"],
        aws_secret_access_key=creds["SecretAccessKey"],
        aws_session_token=creds["SessionToken"],
    )

    return s3


@app.post("/upload")
def upload_file_to_s3():
    try:
        s3 = get_temporary_s3_client()

        with open(STATIC_FILE_PATH, "rb") as file_data:
            s3.upload_fileobj(
                Fileobj=file_data,
                Bucket=BUCKET_NAME,
                Key=S3_KEY,
                ExtraArgs={"ContentType": "image/jpeg"}
            )

        return {"message": f"Arquivo '{STATIC_FILE_PATH}' enviado para S3 com sucesso."}

    except (BotoCoreError, ClientError) as e:
        return {"error": str(e)}
    except FileNotFoundError:
        return {"error": f"Arquivo '{STATIC_FILE_PATH}' não encontrado."}


@app.get("/file")
def get_file_metadata():
    """
    Retorna metadados (ETag, tamanho, content‑type, data de última modificação)
    do objeto no S3.
    """
    s3 = get_temporary_s3_client()
    try:
        head = s3.head_object(Bucket=BUCKET_NAME, Key=LIST_KEY)
        return {
            "key": LIST_KEY,
            "size_bytes": head["ContentLength"],
            "etag": head["ETag"],
            "content_type": head["ContentType"],
            "last_modified": head["LastModified"]
        }
    except s3.exceptions.NoSuchKey:
        return {"error": f"Objeto '{LIST_KEY}' não encontrado"}, 404
    except Exception as e:
        return {"error": str(e)}, 500


@app.delete("/file")
def delete_file():
    """
    Remove o objeto do bucket.
    """
    s3 = get_temporary_s3_client()
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=LIST_KEY)
        return {"message": f"Arquivo '{LIST_KEY}' deletado do S3 com sucesso."}
    except s3.exceptions.NoSuchKey:
        return {"error": f"Objeto '{LIST_KEY}' não encontrado"}, 404
    except Exception as e:
        return {"error": str(e)}, 500
