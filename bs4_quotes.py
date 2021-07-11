from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

quotes_page = "https://bluelimelearning.github.io/my-fav-quotes/"
uClient = urlopen(quotes_page)
html_page = uClient.read()
uClient.close()

soup_page = bs(html_page, "html.parser")
quotes = soup_page.findAll("div", {"class":"quotes"})



for quote in quotes:
    fav_quote = quote.findAll("p", {"class": "aquote"})
    aquote = fav_quote[0].text.strip()

    fav_author = quote.findAll("p", {"class": "author"})
    author = fav_author[0].text.strip()



    print(author)
    print(aquote)
    print()

print(len(quotes))