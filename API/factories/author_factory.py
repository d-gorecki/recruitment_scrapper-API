import factory
from factory.faker import faker

from crawler.models.author import Author


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    full_name = faker.Faker().name()
    author_uri = "".join(full_name.strip().lower().split(" "))
    top_used_words = {"top_word": 1}
