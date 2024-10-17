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
				prompt = os.environ['PROMPT']
				# ollama respose
				response = client.chat(model='llama3.2:1b', messages=[
					{
						'role': 'user',
						'content': f"{prompt}:\n{textDetections['text']}",
					},
				])

				print(response['message']['content'])
				ocrAws.questions = response['message']['content']
				ocrAws.save()

				return Response({'message': 'success', 'data': response['message']['content']}, status=status.HTTP_201_CREATED)

			except Exception as e:                
				raise e
    