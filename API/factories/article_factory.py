import factory
from factory.faker import faker
from crawler.models.article import Article

fake = faker.Faker()


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    author = fake.name()
    title = "title"
    content = "content"
