from django.db import models
from mainapp.models import Business, BusinessPost, BusinessPostComment, Product
from users.models import CustomUser
from rating.models import BusinessRating, ProductRating

# Create your models here.
class ReportCategory(models.Model):
    name = models.CharField(max_length=50)
    priority = models.PositiveIntegerField()

    def __str__(self):
        return f'Name: {self.name}, Priority: {self.priority}'


class ReportBusiness(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'Prority: {self.business}'

class ReportProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'Prority: {self.product}'

class ReportBusinessReview(models.Model):
    review = models.ForeignKey(BusinessRating, models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'Prority: {self.review.id}'

class ReportBusinessPost(models.Model):
    post = models.ForeignKey(BusinessPost, models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'Prority: {self.post.id}'

class ReportBusinessComment(models.Model):
    comment = models.ForeignKey(BusinessPostComment, models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'Prority: {self.id}'

class ReportProductReview(models.Model):
    review = models.ForeignKey(ProductRating, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'Prority: {self.id}'

class Contact(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)