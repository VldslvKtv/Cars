from django.db import models


class Marks(models.Model):
    mark = models.CharField(max_length=150, db_index=True)

    objects = models.Manager()

    def __str__(self):
        return self.mark


class Models(models.Model):
    model = models.CharField(max_length=150)
    fk_model = models.ForeignKey(Marks, on_delete=models.CASCADE, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.model




