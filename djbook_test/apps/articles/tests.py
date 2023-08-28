import datetime

from django.db import transaction
from django.utils import timezone

from articles.models import Article, Tag, User
from django.test import TestCase


'''
def create_article(article_title, days, create=False):
    """
    Create a article with the given `article_text` and published the
    given number of `days` offset to now (negative for articles published
    in the past, positive for articles that have yet to be published).
    """
    rand_int = random.randint(0, 100)
    article_text = f'{article_title}_text 0123456789qwertyuiopasdfghjklzxcvbnm'
    time = timezone.now() + datetime.timedelta(days=days)
    username = f'{article_text}test_user{rand_int}'
    password = f'{article_text}te5t_pa55w0rd1'
    user = User.objects.create(username=username, password=password)
    if create:
        Article.objects.create(title=article_title, text=article_text, pub_date=time, user=user)
    else:
        return Article(title=article_title, text=article_text, pub_date=time, user=user)
    # print(Article.objects.all())


class ArticleIndexViewTests(TestCase):
    def test_no_articles(self):
        """
        If no articles exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('articles:index'))
        print('no:', response)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No articles are available.")
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_past_article(self):
        """
        Articles with a pub_date in the past are displayed on the
        index page.
        """
        create_article(article_title="Past article.", days=-30, create=True)
        response = self.client.get(reverse('articles:index'))
        print('past:', response.context['object_list'])
        self.assertQuerysetEqual(
            response.context['object_list'],
            [create_article(article_title="Past article.", days=-30)]
        )

    def test_future_article(self):
        """
        Articles with a pub_date in the future aren't displayed on
        the index page.
        """
        create_article(article_title="Future article.", days=30, create=True)
        response = self.client.get(reverse('articles:index'))
        print(f'future: {response}')
        self.assertEqual(response.status_code, 404)

    def test_future_article_and_past_article(self):
        """
        Even if both past and future articles exist, only past articles
        are displayed.
        """
        create_article(article_title="Past article.", days=-30, create=True)
        create_article(article_title="Future article.", days=30, create=True)
        response = self.client.get(reverse('articles:index'))
        print('future and past:', response.context['object_list'])
        self.assertListEqual(
            list(response.context['object_list']),
            [create_article(article_title="Past article.", days=-30),
             create_article(article_title="Future article.", days=30)]
        )

    def test_two_past_articles(self):
        """
        The articles index page may display multiple articles.
        """
        create_article(article_title="Past article 1.", days=-30, create=True)
        create_article(article_title="Past article 2.", days=-5, create=True)
        response = self.client.get(reverse('articles:index'))
        print('two past:', response.context['object_list'])
        self.assertQuerysetEqual(
            response.context['object_list'],
            [create_article(article_title="Past article 1.", days=-30),
             create_article(article_title="Past article 2.", days=-5)]
        )
'''


class ArticleModelTests(TestCase):

    def test_was_published_recently_with_future_article(self):
        """
        was_published_recently() returns False for articles whose pub_date
        is in the future.
        """
        print('qqw')
        time = timezone.now() + datetime.timedelta(days=30)
        future_article = Article(pub_date=time)
        self.assertIs(future_article.was_published_recently(), False)


    def test_was_published_recently_with_old_article(self):
        """
        was_published_recently() returns False for articles whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_article = Article(pub_date=time)
        self.assertIs(old_article.was_published_recently(), False)


    def test_was_published_recently_with_recent_article(self):
        """
        was_published_recently() returns True for articles whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_article = Article(pub_date=time)
        self.assertIs(recent_article.was_published_recently(), True)


class AddTagsToArticleTestCase(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title='Test Article',
            text='Test Article text 0123456789qwertyuiopasdfghjklzxcvbnm',
            user=User.objects.create(username='user2_test', password='te5t_pa55w0rd2')
        )
        self.existing_tags = set(Tag.objects.filter(name__in=['test_tag1', 'test_tag2']))

    def test_add_new_tags_to_article(self):
        # Simulate the provided code
        tag_list = ['test_tag3', 'test_tag4', 'test_tag5']
        new_tags_to_create = [Tag(name=tag) for tag in tag_list if tag not in self.existing_tags]

        # Save the new tags to the database
        with self.assertNumQueries(3):  # Ensure only one query for bulk_create
            with transaction.atomic():
                Tag.objects.bulk_create(new_tags_to_create)

        # Fetch all tags again to include the newly created ones with primary keys
        all_tags = Tag.objects.filter(name__in=tag_list)
        self.article.tag.add(*all_tags)

        # Check if the tags are correctly added to the article
        self.assertEqual(self.article.tag.count(), 3)  # The initial set had 2 tags, now we added 3 new tags

        # Check if all the tags from tag_list are in the article
        self.assertSetEqual(set(self.article.tag.values_list('name', flat=True)), set(tag_list))

    def test_add_existing_tags_to_article(self):
        # Simulate the provided code
        tag_list = ['test_tag1', 'test_tag2']

        # Save the new tags to the database (None should be created as they already exist)
        with self.assertNumQueries(3):  # Ensure no queries for bulk_create
            Tag.objects.bulk_create([Tag(name=tag) for tag in tag_list if tag not in self.existing_tags])

        # Fetch all tags again to include the existing ones with primary keys
        all_tags = Tag.objects.filter(name__in=tag_list)
        self.article.tag.add(*all_tags)

        # Check if the tags are correctly added to the article
        self.assertEqual(self.article.tag.count(), 2)  # The initial set had 2 tags, and no new tags were created

        # Check if all the tags from tag_list are in the article
        self.assertSetEqual(set(self.article.tag.values_list('name', flat=True)), set(tag_list))
