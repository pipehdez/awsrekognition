from django.db import models
from .aws import detect_text
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

# Create your models here.
class OcrAws(models.Model):
	image = models.ImageField(upload_to = 'images', null = True, blank = True)
	text = models.TextField(null=True, blank= True)
	result_json = models.JSONField(null=True, blank=True)
	questions = models.TextField(null=True, blank=True)

	# def save(self, *args, **kwargs):
		
	# 	if self.image:
	# 		self.image.open()			
	# 		image_bytes = self.image.read()  # Lee la imagen como bytes
	# 		self.image.seek(0) 
	# 		textDetections = detect_text(image_bytes)	
	# 		self.result_json = textDetections['json']
	# 		# newText = ''
	# 		# i = 0		
	# 		# pattern = r"^\d\s"	
	# 		# isQuestionPrevious = False		
	# 		# for text in textDetections:
	# 		# 	if text['DetectedText'] != 'Yes' and text['DetectedText'] != 'No':
	# 		# 		isQuestion = bool(re.match(pattern, text['DetectedText']))
	# 		# 		if i == 0:
	# 		# 			newText = text['DetectedText']
	# 		# 		else:
	# 		# 			if isQuestion:
	# 		# 				isQuestionPrevious = isQuestion
	# 		# 				newText = newText + '\n\n' + text['DetectedText']
	# 		# 			else:
	# 		# 				if isQuestionPrevious and not isQuestion:
	# 		# 					newText = newText + ' ' + text['DetectedText']
	# 		# 					isQuestionPrevious = False
	# 		# 				else:
	# 		# 					newText = newText + '\n\n' + text['DetectedText']
	# 		# 		i = i + 1
								
	# 		self.text = textDetections['text']
	# 	super(OcrAws, self).save(*args, **kwargs)