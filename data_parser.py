import requests
import bs4
from itertools import chain
from datetime import datetime
from database import Database
from requests.exceptions import RequestException, Timeout, ConnectionError, ConnectTimeout, ReadTimeout


class StatData:
    UKRSTAT_INITIAL_YEAR = 2007
    URL_TEMPLATE_7_13 = "http://www.ukrstat.gov.ua/" + \
                        "operativ/operativ{0:d}/ct/icv/icv_u/icv_m{1}.html"
    URL_TEMPLATE_14 = "http://www.ukrstat.gov.ua/" + \
                      "operativ/operativ{0:d}/ct/icv/icv_u/icv_pm{1}_u.html"
    PAGE_TABLE_IDENT = ["table", "MsoNormalTable", 'td']

    def __init__(self, start_year, end_year):
        self.start_year = start_year
        self.end_year = end_year
        self.current_date = datetime.now()
        self.url_format_7_13 = lambda year: self.URL_TEMPLATE_7_13.format(year, str(year)[-2:])
        self.url_format_14 = lambda year: self.URL_TEMPLATE_14.format(year, str(year)[-2:])
        self.fych = 2013

    @property
    def years(self):
        return range(self.start_year, self.end_year + 1)

    @property
    def urls(self):
        return tuple(self.__urls())

    @property
    def datatable(self):
        return tuple(self.data(url) for url in self.__urls())

    @property
    def all_data(self):
        return {year: data for year, data in zip(self.years, self.data)}

    @property
    def current_year_data(self):
        return self.data(self.url_format_14(self.current_date.year))

    def data(self, url):
        try:
            return self.parse_url_data(url)
        except (RequestException, Timeout, ConnectionError, ConnectTimeout, ReadTimeout):
            print("Can't get data from www.ukrstat.gov.ua. Check internet connection!")

    def __urls(self):
        urls_7_13, urls_14plus = (range,) * 2
        if (self.start_year < self.UKRSTAT_INITIAL_YEAR or self.end_year > self.current_date.year
            or self.end_year < self.start_year):
            raise AssertionError("Date year out of ukrstat.gov data scope!")

        if self.UKRSTAT_INITIAL_YEAR <= self.start_year <= self.fych:
            urls_7_13 = (self.url_format_7_13(year) for year in self.years if year <= self.fych)

        if (self.UKRSTAT_INITIAL_YEAR <= self.start_year <= self.current_date.year
            and self.fych < self.end_year <= self.current_date.year):
            urls_14plus = (self.url_format_14(year) for year in self.years if year > self.fych)

        return chain(urls_7_13, urls_14plus)

    def parse_url_data(self, url):
        data = []
        respond = requests.get(url)
        if respond.ok:
            bs_data = bs4.BeautifulSoup(respond.content, "html.parser")
            tds = bs_data.find_all(*self.PAGE_TABLE_IDENT)
            try:
                for ind in range(3, 26, 2):
                    d = tds[0].contents[3].contents[ind].text.strip()
                    data.append(float(d.replace(',', '.')))
            except ValueError:
                pass
        return tuple(data)

    def __len__(self):
        current_data_len = self.current_year_data
        return len(tuple(current_data_len)) if current_data_len else 0


if __name__ == "__main__":
    sd = StatData(2007, 2016)
    years = sd.years
    urls = sd.urls
    data = sd.datatable
    l = len(sd)
    #print(sd.datatable)
    print(Database().get_all_entries())
    pass
