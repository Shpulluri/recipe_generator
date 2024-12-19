# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class SavedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id = models.IntegerField()
    recipe_title = models.CharField(max_length=255)
    recipe_image = models.URLField()
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe_id')

    def __str__(self):
        return f"{self.recipe_title} - {self.user.username}"