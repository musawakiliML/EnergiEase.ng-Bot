import uvicorn

if __name__ == "__main__":
   '''Run Application Server'''
   uvicorn.run("app.server.app:app", host='0.0.0.0', port=8000, reload=True)