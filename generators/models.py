
from django.db import models

class Polynomial(models.Model):
    degree = models.IntegerField()
    first_number = models.IntegerField()
    second_number = models.IntegerField()
    letter = models.CharField(max_length=1)

    def __str__(self):
        return f"Степінь: {self.degree}, Перше число: {self.first_number}, Друге число: {self.second_number}, Буква: {self.letter}"
