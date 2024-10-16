python3 -m venv env
source env/bin/activate  
python3 -m pip install -r requirement.txt
python3 manage.py runserver
ollama run llama3
pip freeze index.py > requirements.txt

curl -X POST http://localhost:8000/predict/ -d "input=write a horror story"

prompt:

Analiza el siguiente texto: saca las preguntas y datos de formulario en una misma estructura y devuelvelo en una estructura json, ejemplo: [{ question: "", type: "", options: [{ "label": "", "value": "" },]}] puedes incluir firmas y fechas solo si es necesario o se encuentra en el texto, importante: No incluyas ningún texto adicional en tu respuesta, Solo el JSON, Si no puedes determinar el tipo de input, usa "text" por defecto, Asegúrate de que el JSON sea válido y siga exactamente la estructura proporcionada:
