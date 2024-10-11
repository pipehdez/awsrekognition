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

	def save(self, *args, **kwargs):
		
		super(OcrAws, self).save(*args, **kwargs)
		if self.image:
			
			photo = self.image  # Suponiendo que puedes pasar self.image directamente
			self.text = detect_text(photo)  # Consumimos el método detect_text y guardamos el resultado en el campo 'text'
		super(OcrAws, self).save(*args, **kwargs)