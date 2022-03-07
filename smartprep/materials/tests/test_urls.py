from django.test import SimpleTestCase
from django.urls import reverse, resolve
from materials.views import course, cart


class TestUrls(SimpleTestCase):
    def test_course_url(self):
        url = reverse('course')
        self.assertEqual(resolve(url).func, course)

    def test_cart_url(self):
        url = reverse('cart')
        self.assertEqual(resolve(url).func, cart)
