import os

from dotenv import load_dotenv
from fastapi import status
from fastapi.responses import JSONResponse
from supabase import Client, create_client

load_dotenv()

supabase_url: str = os.environ["SUPABASE_URL"]
supabase_key: str = os.environ["SUPABASE_KEY"]

supabase: Client = create_client(supabase_url, supabase_key)
bucket_name: str = "energiease"


def upload_to_supabase(file, file_name: str):
    try:
        # Get Bucket and Upload
        file_bytes = file.read()

        response = supabase.storage.from_(bucket_name).upload(
            file=file_bytes, path=file_name, file_options={"content-type": "image/jpeg"}
        )

        if response.status_code != 200:
            resp = {
                "message": "Error Uploading Files",
                "Error": response["error"]["message"],  # type: ignore
                "status": status.HTTP_400_BAD_REQUEST,
            }

            return JSONResponse(content=resp, status_code=status.HTTP_400_BAD_REQUEST)

        # Get Public Url
        public_url = supabase.storage.from_(bucket_name).get_public_url(file_name)

        resp = {
            "message": "Successfully Retrieved Url",
            "public_url": public_url,
            "status": status.HTTP_200_OK,
        }

        return JSONResponse(content=resp, status_code=status.HTTP_200_OK)

    except Exception as e:
        resp = {
            "message": "Error Uploading File",
            "Error": f"{str(e)}",  # type: ignore
            "status": status.HTTP_400_BAD_REQUEST,
        }

        return JSONResponse(content=resp, status_code=status.HTTP_400_BAD_REQUEST)


# test = upload_to_supabase("app/server/utils/test.jpg", "test.png")

# print(jsonable_encoder(test.body))
