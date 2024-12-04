python3 -m venv venv
source venv/bin/activate
export PYTHONPATH="$(pwd):$PYTHONPATH"
pip install uvicorn
pip install -r requirements.txt
cd app
uvicorn main:app --reload