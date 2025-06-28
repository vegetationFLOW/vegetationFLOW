from fastapi import FastAPI
import vegetationFLOW_core
import ee
import os
import google.auth

app = FastAPI()

@app.get("/veg_v/")
def get_status():
    print(vegetationFLOW_core.__version__)
    try:
        credentials, _ = google.auth.load_credentials_from_file(
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
            scopes=["https://www.googleapis.com/auth/earthengine.readonly"]
        )
        ee.Initialize(credentials)
        print("Successfuly")
    except Exception as e:
        print(e)
