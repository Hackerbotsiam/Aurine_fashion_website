from django.db import models
from django.utils.text import slugify

# ১. ক্যাটাগরি (Ladies Cloth, Perfume)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ২. প্রোডাক্ট (ছবি, দাম, ডেসক্রিপশন, ক্যাটাগরি)
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ৩. প্রোডাক্ট সাইজ (S, M, L, XL, 50ml, 100ml)
class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size_name = models.CharField(max_length=50, help_text="e.g. S, M, L, XL, 50ml, 100ml")

    def __str__(self):
        return f"{self.product.name} - {self.size_name}"


# 4. Hero Carousel Slide
class HeroSlide(models.Model):
    title = models.CharField(max_length=200, default="Clean Lines. Conscious Living.")
    subtitle = models.CharField(max_length=300, default="Timeless essentials for the modern minimalist. Designed to simplify your wardrobe.")
    image = models.ImageField(upload_to='hero_slides/', help_text="Upload background image for the slide")
    order = models.IntegerField(default=0, help_text="Sorting order in the carousel")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
