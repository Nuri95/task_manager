poetry shell
cd src/
export PYTHONPATH=$PWD
cd task_manager/
python create_db.py
python -m uvicorn app:app --port 5000 --host 0.0.0.0