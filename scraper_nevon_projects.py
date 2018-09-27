from urllib2 import urlopen
from urllib2 import HTTPError
from urllib2 import URLError
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.projects_similarity
db.projects.delete_many({})

BASE_URI = u"http://nevonprojects.com/project-ideas/software-project-ideas/"

try:
    html = urlopen(BASE_URI)
except HTTPError as e:
    print(e)
except URLError:
    print("URI not found")
else:
    soup = BeautifulSoup(html, "lxml")
    lis = soup.findAll("li")

    for i, li in enumerate(lis):
        if (i > 65 and i < 279):
            print(li.a.get('href'))

            try:
                html = urlopen(li.a.get('href'))
            except HTTPError as e:
                print(e)
            except URLError:
                print("URI not found")
            else:
                soup = BeautifulSoup(html, "lxml")
                h1s = soup.findAll("h1")
                tds = soup.findAll("td")

                try:
                    print(h1s[0].getText())
                    print(tds[0].getText())

                    id = db.projects.insert_one({
                        'name': h1s[0].getText().strip(),
                        'description': tds[0].getText().strip()
                    }).inserted_id
                except:
                    print(u"Something failed!")
