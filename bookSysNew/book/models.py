from django.db import models


# Create your models here.
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    pub_date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    publisher = models.ForeignKey(to="Publish", on_delete=models.CASCADE)
    authors = models.ManyToManyField("Author")

    def __str__(self):
        return self.title


class Publish(models.Model):
    name = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    addr = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    ad = models.OneToOneField("AuthorDetail", on_delete=models.CASCADE)


class AuthorDetail(models.Model):
    tel = models.CharField(max_length=32)
    email = models.CharField(max_length=32)


class User(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
