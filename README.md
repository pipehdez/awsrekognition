python3 -m venv env
source env/bin/activate  
python3 -m pip install -r requirement.txt
python3 manage.py runserver
ollama run llama3
pip freeze index.py > requirements.txt

curl -X POST http://localhost:8000/predict/ -d "input=write a horror story"
