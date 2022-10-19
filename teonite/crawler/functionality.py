from bs4 import BeautifulSoup
from requests import get, Response
from crawler.models import Article

URL: str = "https://teonite.com/blog/"
article_list: Response = get(URL)
bs = BeautifulSoup(article_list.content, features="html.parser")

for article in bs.find("div", class_="post-cards").find_all("article"):
    title_anchor = article.find("a", class_="title", href=True)
    title = title_anchor.get_text()
    article_detail = get("https://teonite.com" + title_anchor["href"])
    bs_article = BeautifulSoup(article_detail.content, features="html.parser")
    article_content = ""
    for p in bs_article.find("article", class_="post-content").find_all("p"):
        article_content += p.get_text()
    author = article.find("span", class_="author").get_text()

    db_article = Article.objects.filter(author=author, title=title)
    if not db_article:
        Article.objects.create(author=author, title=title, content=article_content)
