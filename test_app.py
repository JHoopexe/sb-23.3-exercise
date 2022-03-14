
from app import app
from unittest import TestCase

class BloglyTestCase(TestCase):
    def test_home(self):
        with app.test_client() as client:
            res = client.get('/')

            self.assertEqual(res.status_code, 302)

    def test_users(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertIn('<title>Blogly</title>', html)

    def test_user_new(self):
        with app.test_client() as client:
            res = client.get('/users/new')
            
            self.assertEqual(res.status_code, 200)

    def test_user_new_post(self):
        with app.test_client() as client:
            res = client.post('/users/new', data = {
                'first': 'John', 
                'last': 'Wick', 
                'image': 'https://d2cbg94ubxgsnp.cloudfront.net/Pictures/480x270/9/9/3/512993_shutterstock_715962319converted_920340.png'})

            self.assertEqual(res.status_code, 302)

    def test_user(self):
        with app.test_client() as client:
            res = client.get('/users/1')
            html = res.get_data(as_text=True)

            self.assertIn('<h1>Posts</h1>', html)

    def test_user_post_new(self):
        with app.test_client() as client:
            res = client.get('/users/1/posts/new')

            self.assertEqual(res.status_code, 200)

    
    def test_post_edit(self):
        with app.test_client() as client:
            res = client.get('/posts/1/edit')

        self.assertEqual(res.status_code, 200)
