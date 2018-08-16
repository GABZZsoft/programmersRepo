from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from .views import home, board_topics, new_topic
from .models import Board, Topic, Post
from .forms import NewTopicForm
# Create your tests here.

class HomeTest(TestCase):
    def setUp(self):
        self.board=Board.objects.create(name='Django', description='Django description')
        self.url = reverse('home')
        self.response = self.client.get(self.url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolve_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        boards_topic_url=reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(boards_topic_url))

class BoardTopicsTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django description')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk':self.board.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk':99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolve_board_topics_view(self):
        view = resolve('/1/')
        self.assertEquals(view.func, board_topics)

    def test_board_topic_view_contain_link_back_homepage(self):
        board_topic_url = reverse('board_topics', kwargs={'pk':1})
        response = self.client.get(board_topic_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))

    def test_board_topic_view_contain_link_newTopic(self):
        board_topic_url = reverse('board_topics', kwargs={'pk':1})
        response = self.client.get(board_topic_url)
        new_topic_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))



class NewTopicTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Flask', description='Flask Discussion')
        User.objects.create_user(username='tester', email='tester@test.com', password='123')
        self.url = reverse('new_topic', kwargs={'pk':self.board.id})
        self.response = self.client.get(self.url)

    def test_newt_topic_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_new_topic_view_not_success(self):
        url = reverse('new_topic', kwargs={'pk':99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_confirm_right_view(self):
        view = resolve('/1/new')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_contain_link_back_board_topic(self):
        new_topic = reverse('new_topic', kwargs={'pk': self.board.id})
        response = self.client.get(new_topic)
        board_topic = reverse('board_topics', kwargs={'pk':self.board.id })
        self.assertContains(response, 'href="{0}"'.format(board_topic))

    def test_csrf(self):
        new_topic_url = reverse('new_topic',kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post(self):
        new_topic_url = reverse('new_topic', kwargs={'pk':1})
        data = {'subject':'test', 'message':'just testing',}
        response = self.client.post(new_topic_url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_invalid_post_data(self):
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_invalid_empty_post(self):
        url=reverse('new_topic', kwargs={'pk':1})
        data = {'subject':'', 'message':''}
        response= self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())

    def test_context_contains_form(self):
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_post_invalid_data(self):
        url=reverse('new_topic', kwargs={'pk':1})
        response = self.client.post(url,{})
        form = response.context.get('form')
        self.assertTrue(form.errors)
        self.assertEquals(response.status_code, 200)
