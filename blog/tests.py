from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
from django.utils import timezone
from django.contrib.auth.models import User


def create_post(title, content, author):
    blog_post = Post.objects.create(
        title=title,
        content=content,
        created=timezone.now(),
        author=author
    )

    return blog_post

class TestView(TestCase):
    def setup(self):
        self.client = Client()
        self.author_000 = User.objects.create(username='smith', password='nopassword')

    def check_navbar(self, soup):
        navbar = soup.find('div', id='navbar')
        self.assertin('Blog', navbar.text)
        self.assertin('About me', navbar.text)

    def test_index(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        self.assertEqual(title.text, 'Blog')

        self.check_navbar(soup)

        self.assertEqual(Post.objects.count(), 0)

        post_000 = create_post(
            title='The first Post',
            content='hello',
            author=self.author_000,
        )

        self.assertGreater(Post.objects.count(), 0)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.body
        self.assertNotin('아직 게시물이 없습니다.', body.text)
        self.assertin(post_000.title, body.text)

        post_000_more_info_btn = body.find('a', id='more-info-post-{}', format(post_000.pk))
        self.assertEqual(post_000_more_info_btn['href'], post_000.get_absolute_url())

    def test_post_detail(self):
        post_000 = create_post(
            title='The first Post',
            content='hello',
            author=self.author_000
        )

        self.assertGreater(Post.objects.count(), 0)
        post_000_url = post_000.get_absolute_url()
        self.assertEqual(post_000_url, '/blog/{}', format(post_000.pk))

        response = self.client.get(post_000_url)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title

        self.assertEqual(title.text, '{} - Blog', format(post_000.title))

        self.check_navbar(soup)

        body = soup.body

        main_diy = body.find('diy', id='main_diy')
        self.assertin(post_000.title, main_div.text)
        self.assertin(post_000.author.username, main_div.text)

        self.assertin(post_000.content, main_diy)





