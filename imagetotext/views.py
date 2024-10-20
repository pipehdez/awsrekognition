from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from imagetotext.models import OcrAws
from imagetotext.serializers import OcrAwsSerializer
from rest_framework import status, viewsets, permissions
from .aws import detect_text
from ollama import Client
# import ollama
import os
import json

class OcrAwsViewSet(viewsets.ModelViewSet):
	model = OcrAws
	queryset = model.objects.all()
	serializer_class = OcrAwsSerializer
	nombre_modulo = 'OcrAws'

	#  def get_permissions(self):
    #     if self.action in ['create','openDiligenceProcess','saveDiligenceProcess','saveDiligenceAnexoTemp',\
    #             'getAnexo','getNoRadicado','getCuadro','getLinkObjetivo', 'getContestacionSuperior',\
    #             'getDocumento','saveSignProcess','getAdjunto','getCertificado', 'saveDiligenceTemp',\
    #             'contestarNormal','contestarRechazo','contestarVistoBueno','getControlAcceso','list','getFiltros',]:         
    #         permission_classes = [permissions.AllowAny]
    #     else:           
    #         permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
            
    #     return [permission() for permission in permission_classes]

	def create(self, request, *args, **kwargs):
		print('request', request.data)
		if request.method == 'POST':
			try:
				client = Client(host='http://localhost:11434')
				image = request.FILES['image']
				image.open()	
				image_bytes = image.read()
				image.seek(0) 
				textDetections = detect_text(image_bytes)	
				
				ocrAws = OcrAws()	
				ocrAws.image = image
				ocrAws.text = textDetections['text']
				ocrAws.result_json = textDetections['json']
				print('text', textDetections['text'])
				language = request.data['language']
				# prompt = """Analiza el siguiente texto y extrae todas las preguntas y datos de formulario en una estructura JSON. El formato debe ser un array de objetos con la siguiente estructura: [{ procedureName: 'string', tasks: [{ "taskName": 'string', "done": boolean }]}]. , añádelas; de lo contrario, no las incluyas. No devuelvas ningún texto adicional, solo el JSON. . Asegúrate de que el JSON sea válido y siga estrictamente el formato especificado, los valores deben venir en el idioma """ + language + """."""

				# Analiza el siguiente texto: saca la comprobación de titulo como el procedureName y saca los conceptos: revisando conforme y datos de formulario en una misma estructura y devuelvelo en una estructura json y en el idioma """ + languaje + """, ejemplo de como debe devolver la estructura: [{ procedureName: 'string', tasks: [{ "taskName": 'string', "done": boolean }]}] , importante: No incluyas ningún texto adicional en tu respuesta, Solo el JSON, Asegúrate de que el JSON sea válido y siga exactamente la estructura proporcionada:
				prompt = f"""
				Analiza el siguiente texto: {textDetections['text']} identifica el encabezado como procedureName y cada punto de la lista de verificación como tasks. Debes devolver un JSON válido, estrictamente en el siguiente formato:
				[{{
					"procedureName": "string",
					"tasks": [
						{{ 
							"taskName": "string", "done": false 
						}}
					]}}
					]
					Donde:
					procedureName será el encabezado de la sección principal.
					taskName será cada uno de los elementos de la lista de verificación.
					El valor done debe ser siempre false.
					los taskName estaran escritos en {language} y no devuelvas ningún texto adicional fuera de este JSON. Solo devuelve el JSON sin comentarios ni explicaciones.
				"""
				# prompt = """
				# 	Analiza el siguiente texto: la informacion del este formulario como un objeto json, lo mas importante la lista de tarea en elcuadro con respuesta de si/no en este formato: tasks: [{ "taskName": 'string', "done": boolean }] y el nombre de la comprobacion como procedureName: 'string' el objeto al final debe quedar asi el ejemplo: [{ procedureName: 'string', tasks: [{ "taskName": 'string', "done": boolean }]}] importante: No incluyas ningún texto adicional en tu respuesta, Solo el JSON, Asegúrate de que el JSON sea válido y siga exactamente la estructura proporcionada, y por ultimo el idioma debe ser """ + languaje
				
				#os.environ['PROMPT']

				# ollama respose
				response = client.chat(model='llama3.2:1b', messages=[
					{
						'role': 'system',
						'content': 'Entrenado para ayudarte a extraer información de textos. Por favor, sigue las instrucciones cuidadosamente.',
					},
					{
						'role': 'user',
						'content': prompt,
					},
				])

				print(response['message']['content'].replace('`', ''))
				ocrAws.questions = response['message']['content'].replace('`', '')
				ocrAws.save()

				content = response['message']['content'].replace('`', '')
				if content:
					parsed_data = json.loads(content)
				else:
					parsed_data = None

				# data: response json
				return Response({
					'message': 'success', 
					'data': parsed_data
				}, status=status.HTTP_201_CREATED)

			except Exception as e:                
				return Response({
					'message': 'error',
					'data': 'Invalid JSON format in response content.'
				}, status=status.HTTP_400_BAD_REQUEST)
    