from django.http import response
from django.test import TestCase
from django.urls import reverse
from django.urls.base import resolve

from boards.models import Board
from .views import home,board_topic
# Create your tests here.

class HomeTest(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response  =self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func , home)

class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name = 'Python',description = 'A very simple and easy programming language')

    def test_board_topics_view_success_status_code(self):
        url = reverse(board_topic,kwargs={'id':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_board_topics_view_page_not_found_status_code(self):
        url = reverse(board_topic,kwargs={'id':5})
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)
    
    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/board/1')
        self.assertEquals(view.func ,board_topic)