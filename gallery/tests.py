from django.test import TestCase
from django.urls import reverse
from .models import Category, Image
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date

class GalleryViewsTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Category 1')
        image_content = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',
            content_type='image/gif'
        )

        self.image = Image.objects.create(
            title='Зображення ТЕСТ',
            image=image_content,
            created_date=date.today(),
            age_limit=10,
        )
        self.image.categories.add(self.category)

    def test_gallery_correct_template(self):
        url = reverse('main')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gallery.html')
        self.assertIn(self.category, response.context['categories'])

    def test_gallery_contains_image(self):
        images_in_category = list(self.category.image_set.all())
        self.assertIn(self.image, images_in_category)

    def test_image_correct_template(self):
        url = reverse('image_detail', args=[self.image.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image_detail.html')
        self.assertEqual(response.context['image'], self.image)