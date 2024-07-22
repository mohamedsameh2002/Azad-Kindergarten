from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.validators import MaxValueValidator, MinValueValidator



class Teacher (models.Model):
    name=models.CharField(max_length=200)
    number = models.DecimalField(max_digits=5, decimal_places=0)
    def __str__(self) -> str:
        return self.name


class DeleteHomework (models.Model):
    date = models.DateField(auto_now_add=True)



class Homework(models.Model):
    THE_YEARS=[
        ('KG1','KG1'),
        ('KG2','KG2'),
    ]
    year = models.CharField(max_length=10, choices=THE_YEARS)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True)
    homework = models.TextField(max_length=2000)
    date = models.DateField(auto_now_add=True)
    image_1 = models.ImageField(upload_to='homework_images/',blank=True,null=True)
    image_2 = models.ImageField(upload_to='homework_images/',blank=True,null=True)
    image_3 = models.ImageField(upload_to='homework_images/',blank=True,null=True)
    def __str__(self) -> str:
        return self.year

    def save(self, *args, **kwargs):
        # Resize image_1
        if self.image_1:
            self.image_1 = self.resize_image(self.image_1)
        # Resize image_2
        if self.image_2:
            self.image_2 = self.resize_image(self.image_2)
        # Resize image_3
        if self.image_3:
            self.image_3 = self.resize_image(self.image_3)
        
        super().save(*args, **kwargs)

    def resize_image(self, image_field):
        img = Image.open(image_field)
        output = BytesIO()
        img = img.resize((800, 800))  # Adjust the size as needed
        img.save(output, format='png', quality=85)  # Adjust quality as needed
        output.seek(0)
        return ContentFile(output.read(), name=image_field.name)



class DeleteHomework (models.Model):
    delete=models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)