from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category 

class bid(models.Model):  # Convención de nombres: se recomienda que las clases empiecen con mayúscula
    bid_amount = models.FloatField(default=0)  # Cambié el nombre a bid_amount para mayor claridad
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bids")  # Cambié 'comentKey' a 'bids'

    def __str__(self):
        return str(self.bid_amount)  # Cambié el método a devolver el valor como cadena

class Lista(models.Model): 
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.ForeignKey(bid, on_delete=models.CASCADE, null=True, blank=True, related_name="price_bids")  # Cambié 'priceBid' a 'price_bids'
    url = models.URLField(max_length=3000)
    activate = models.BooleanField(default=True)
    # ower
    key = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="listas")  # Cambié 'listasKey' a 'listas'
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="listas")  # Cambié 'listasCat' a 'listas'
    listWatch = models.ManyToManyField(User, blank=True, related_name="watch_lists")  # Cambié 'listaWatch' a 'watch_lists'

    def __str__(self):
        return f"titulo: {self.title} | precio: {self.price} | description: {self.description}"

class comentarios(models.Model):  # Cambié el nombre de la clase a 'Comentarios'
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="comentarios")  # Cambié 'comentKey' a 'comentarios'
    listing = models.ForeignKey(Lista, on_delete=models.CASCADE, blank=True, null=True, related_name="comentarios")  # Cambié 'listKey' a 'comentarios'
    comentario = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user} comentó en {self.listing}"
