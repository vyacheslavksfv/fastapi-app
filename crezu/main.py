from multiprocessing.spawn import freeze_support

import uvicorn

if __name__ == "__main__":
    freeze_support()

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
