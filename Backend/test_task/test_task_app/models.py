from django.db import models

# Create your models here.
class Occupation(models.Model):
    name          = models.CharField(max_length=200)
    company_name  = models.CharField(max_length=100)
    position_name = models.CharField(max_length=100)
    hire_date     = models.DateField()
    fire_date     = models.DateField(null=True, blank=True)
    salary        = models.PositiveIntegerField()
    fraction      = models.PositiveIntegerField()
    base          = models.PositiveIntegerField()
    advance       = models.PositiveIntegerField()
    by_hours      = models.BooleanField()

    # Имя: name (varchar 200)
    # Компания: company_name (varchar 100)
    # Должность: position_name (varchar 100)
    # Дата приёма: hire_date (date)
    # Дата увольнения: fire_date (date, null)
    # Ставка, руб.: salary (int)
    # Ставка, %: fraction (int)
    # База, руб.: base (int)
    # Аванс, руб.: advance (int)
    # Почасовая оплата: by_hours (boolean)