import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
class Movie:
    def __init__(self, mainpage="http://asilmedia.org/films/tarjima_kinolar//"):
        self.mainpage = mainpage
        self.kino = []
        self.serial = []
        self.dict_serial = {}

    def get_movies(self):
        req = requests.get(self.mainpage)
        soup = BeautifulSoup(req.content, "html.parser")
        articles = soup.find_all("article", class_="shortstory-item moviebox to-ripple is-green anima")
        for article in articles:
            film_link = article.find("a", class_="flx flx-column flx-column-reverse")
            film_one_link = film_link.get("href")
            kino = film_link.find("div", class_="genre txt-ellipsis")
            if kino.text.strip() == "Tarjima Kinolar":
                self.kino.append(film_one_link)

    def get_serial(self):
        req = requests.get(self.mainpage)
        soup = BeautifulSoup(req.content, "html.parser")
        articles = soup.find_all("article", class_="shortstory-item moviebox to-ripple is-green anima")
        for article in articles:
            film_link = article.find("a", class_="flx flx-column flx-column-reverse")
            film_one_link = film_link.get("href")
            kino = film_link.find("div", class_="genre txt-ellipsis")
            if kino.text.strip() == "Seriallar":
                self.serial.append(film_one_link)

    def get_movie_datas(self):
        movie_data_list = []
        for kino in self.kino:
            request = requests.get(kino)
            soup = BeautifulSoup(request.content, "html.parser")
            main = soup.find_all("div", class_="content-main flx-fx")

            for soup in main:
                name = soup.find("h2", itemprop="name").text.strip()
                image_url = soup.find("img", itemprop="contentUrl")
                image_one_url = f"http://asilmedia.org/{image_url.get('src')}"
                download_list = soup.find("div", class_="download-list d-hidden")
                download = download_list.find_all("a", rel="noreferrer")
                link_download = []
                dict_movie = {}
                for type in download:
                    link = type.get("href")
                    encoded_link = quote(link, safe=':/')
                    link_download.append(encoded_link)
                    dict_movie[f"{name}_name"] = link_download
                    dict_movie[f"{name}_image"] = image_one_url
                movie_data_list.append(dict_movie)
        return movie_data_list

    def get_serial_datas(self):
        serial_data_list = []
        for serial in self.serial:
            request = requests.get(serial)
            soup = BeautifulSoup(request.content, "html.parser")
            main = soup.find_all("div", class_="content-main flx-fx")

            for soup in main:
                name = soup.find("h2", itemprop="name").text.strip()
                image_url = soup.find("img", itemprop="contentUrl")
                image_one_url = f"http://asilmedia.org/{image_url.get('src')}"
                download_list = soup.find("div", class_="download-list d-hidden")
                download = download_list.find_all("a", target="blank")
                serial_data = {}
                dict_serial = {}
                for link in download:
                    link_text = link.text.strip()
                    link_href = link.get("href")
                    serial_data[link_text] = quote(link_href.strip(), safe=':/')
                    dict_serial["serial_name"] = name
                    dict_serial[f"serial_image"] = image_one_url
                    dict_serial[f"serial_parts"] = serial_data
                serial_data_list.append(dict_serial)
        return serial_data_list


obj = Movie()
obj.get_movies()
print(obj.get_movie_datas())
