from fastapi import FastAPI, status

app = FastAPI()


@app.get("/")
async def root():
    return


@app.get("/health_check", status_code=status.HTTP_200_OK)
async def health_check():
    return
