from django.test import TestCase
from django.urls import reverse, resolve
from ..views import signup
from django.contrib.auth.models import User
#from django.contrib.auth.forms import SignUpForm
from ..forms import SignUpForm
# Create your tests here.

class SignUp(TestCase):
    def setUp(self):
        self.url = reverse('signup')
        self.response= self.client.get(self.url)

    def test_user_sign_up(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_sign_up_resolver(self):
        view = resolve('/account/')
        self.assertEquals(view.func,signup)

    def test_sign_up_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_sign_up_csrf_token(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

class successful_signup_test(TestCase):
    def setUp(self):
        url = reverse('signup')
        data={'username':'user1','email':'user1@user.com' ,'password1':'pass12345','password2':'pass12345'}
        self.response=self.client.post(url, data)
        self.home_url = reverse('home')

    def test_successful_signup(self):
        self.assertTrue(User.objects.exists())

    def test_redirect_after_user_creation(self):
        self.assertRedirects(self.response, self.home_url)

    def test_user_auth(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

#    def test_form_input(self):
#        self.assertContains(self.response,'type="text"', 1)
#        self.assertContains(self.response,'type="email"', 1)
#        self.assertContains(self.response,'type="password"', 2)
