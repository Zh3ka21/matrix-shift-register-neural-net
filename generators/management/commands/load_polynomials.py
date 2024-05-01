# management/commands/load_polynomials.py

import json
from django.core.management.base import BaseCommand
from generators.models import Polynomial

class Command(BaseCommand):
    help = 'Завантаження поліномів з JSON-файлу в базу даних'

    def handle(self, *args, **kwargs):
        with open('irreducible_polynoms.json', 'r') as file:
            data = json.load(file)

        for degree, items in data.items():
            for item in items:
                for key, value in item.items():
                    if key and value and any(char.isdigit() for char in value):  # Проверяем, что ключ и значение не пустые и есть хотя бы одна цифра в значении
                        if value[-1].isalpha():  # Проверяем, что последний символ является буквой
                            first_number, second_number = int(key), int(value[:-1])
                            letter = value[-1]
                        else:
                            first_number, second_number = int(key), int(value)
                            letter = ''  # Если нет буквы, устанавливаем пустую строку
                        polynomial = Polynomial.objects.create(degree=int(degree), first_number=first_number, second_number=second_number, letter=letter)
                        self.stdout.write(self.style.SUCCESS(f'Поліном {polynomial} успішно додано'))