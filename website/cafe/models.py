from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("reviewed", "Reviewed"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    position = models.CharField(max_length=60)
    message = models.TextField()
    cv = models.FileField(upload_to="cvs/", blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.position}"
class Coffee(models.Model):
    CATEGORY_COFFEE = "COFFEE"
    CATEGORY_DESSERT = "DESSERT"

    CATEGORY_CHOICES = [
        (CATEGORY_COFFEE, "Coffee"),
        (CATEGORY_DESSERT, "Dessert"),
    ]

    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default=CATEGORY_COFFEE
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="coffees/", blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
