import base64, boto3
from django.conf import settings

def detect_text(photo):
	
	with photo.open("rb") as image_file:
		base64_image = base64.b64encode(image_file.read())
		imgBase64 = base64.decodebytes(base64_image)

		if imgBase64:
			client = boto3.client('rekognition',
				region_name = settings.REKOGNITION_REGION_NAME,
				aws_access_key_id = settings.REKOGNITION_ACCESS_KEY_ID,
				aws_secret_access_key = settings.REKOGNITION_SECRET_ACCESS_KEY)
			

			response = client.detect_text(
				Image = {
					'Bytes':imgBase64
				}
			)
			obj = []
			textDetections = response['TextDetections']
			for text in textDetections:
				# guarda en un array de objetos
				obj.append({
					'DetectedText': text['DetectedText']
				})
			texto_arma = ' '.join([word['DetectedText'] for word in obj])
				# print('Detected text:' + text['DetectedText'])
				# print('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
				# print('Id: {}'.format(text['Id']))
				# if 'ParentId' in text:
				# 	print('Parent Id: {}'.format(text['ParentId']))
				# print('Type:' + text['Type'])
				# print()
			return texto_arma

	# session = boto3.Session(profile_name='default')
	# client = session.client('rekognition')

	# response = client.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': photo}})

	# textDetections = response['TextDetections']
	# print('Detected text\n----------')
	# for text in textDetections:
	# 	print('Detected text:' + text['DetectedText'])
	# 	print('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
	# 	print('Id: {}'.format(text['Id']))
	# 	if 'ParentId' in text:
	# 		print('Parent Id: {}'.format(text['ParentId']))
	# 	print('Type:' + text['Type'])
	# 	print()
	# return len(textDetections)