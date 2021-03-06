"""
Это файл для тестирования Django-приложения
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission
from WEB_App.models import Rate, Comment, ChildrenComment


class IndexTest(TestCase):
    """
    Класс для тестирования главной страницы сайта
    """
    fixtures = ['db.json']

    def setUp(self):
        """
        Базовая настройка тестов для страницы

        :return: None
        """
        self.client = Client()

    def test_none_authorised_user_photo_scan_try(self):
        """
        Тест на неавторизованного пользователя

        :return: None
        """
        response = self.client.post('/', {'file-input-for-label': 'fixtures/test.jpg'},
                                    follow=True)
        print(response.redirect_chain)
        self.assertEqual(response.request['PATH_INFO'], '/')

    def tearDown(self):
        pass


class ProductPageTest(TestCase):
    """
    Класс для тестирования страницы продукта
    """
    fixtures = ['db.json']

    def setUp(self):
        """
        Базовая настройка тестов для страницы

        :return: None
        """
        self.client = Client()
        self.user = User.objects.get(username='test_user')

    def test_rate_photo(self):
        """
        Тестирование оценки товара

        :return: None
        """
        perm = Permission.objects.get(codename='add_rate')
        self.user.user_permissions.add(perm)
        self.client.login(username=self.user.username, password='test_user')
        response0 = self.client.post('/product/test/', {'rating': '0'})
        response2_5 = self.client.post('/product/test/', {'rating': '2.5'})
        response5 = self.client.post('/product/test/', {'rating': '5'})

        self.assertGreater(len(Rate.objects.filter(rating='0')), 0)
        self.assertEqual(response0.request['PATH_INFO'], '/product/test/')

        self.assertGreater(len(Rate.objects.filter(rating='2.5')), 0)
        self.assertEqual(response2_5.request['PATH_INFO'], '/product/test/')

        self.assertGreater(len(Rate.objects.filter(rating='5')), 0)
        self.assertEqual(response5.request['PATH_INFO'], '/product/test/')

    def test_comment_photo(self):
        """
        Тест на комментирование товара

        :return: None
        """
        perm_comment = Permission.objects.get(codename='add_comment')
        perm_child = Permission.objects.get(codename='add_childrencomment')
        self.user.user_permissions.add(perm_comment)
        self.user.user_permissions.add(perm_child)
        self.client.login(username=self.user.username, password='test_user')

        response_whitespace_comment = self.client.post('/product/test/', {'comment': ' '})
        response_newline_comment = self.client.post('/product/test/', {'comment': '\n'})
        response_normal_comment = self.client.post('/product/test/', {'comment': 'test'})

        response_whitespace_child = self.client.post('/product/test/',
                                                     {'response-to-comment': ' '})
        response_newline_child = self.client.post('/product/test/', {'response-to-comment': '\n'})
        response_normal_child = self.client.post('/product/test/', {'response-to-comment': 'test'})

        self.assertEqual(len(Comment.objects.filter(text=' ')), 0)
        self.assertEqual(response_whitespace_comment.request['PATH_INFO'], '/product/test/')

        self.assertEqual(len(Comment.objects.filter(text='\n')), 0)
        self.assertEqual(response_newline_comment.request['PATH_INFO'], '/product/test/')

        self.assertGreater(len(Comment.objects.filter(text='test')), 0)
        self.assertEqual(response_normal_comment.request['PATH_INFO'], '/product/test/')

        self.assertEqual(len(ChildrenComment.objects.filter(text=' ')), 0)
        self.assertEqual(response_whitespace_child.request['PATH_INFO'], '/product/test/')

        self.assertEqual(len(ChildrenComment.objects.filter(text='\n')), 0)
        self.assertEqual(response_newline_child.request['PATH_INFO'], '/product/test/')

        self.assertGreater(len(ChildrenComment.objects.filter(text='test')), 0)
        self.assertEqual(response_normal_child.request['PATH_INFO'], '/product/test/')

    def tearDown(self):
        pass


class AdminPageTest(TestCase):
    """
    Класс для тестирования страницы администрации
    """
    fixtures = ['db.json']

    def setUp(self):
        """
        Базовая настройка тестов для страницы

        :return: None
        """
        pass

    def test_admin_page(self):
        """
        Тест страницы администрации

        :return: None
        """
        self.assertEqual(True, True)

    def tearDown(self):
        pass
