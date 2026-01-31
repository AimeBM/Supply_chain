import subprocess
import sys

processes = [
    ["uvicorn", "api.main:app", "--reload"],
    ["streamlit", "run", "app/app.py"]
]

for p in processes:
    subprocess.Popen(p)

print("🚀 FastAPI + Streamlit launched")
input("Press ENTER to stop...")
