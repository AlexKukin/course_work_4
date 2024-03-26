import requests
from abc import ABC, abstractmethod
from src.vacancy import Vacancy
import os


class Parser(ABC):
    """
    Aбстрактный класс. Должен уметь подключаться к API и получать вакансии.
    При инициализации сохраняет считанные данные в файл на диск. С замещением файла.
    """

    def __init__(self, file_worker, keyword):
        self.file_worker = file_worker
        vacancies = self.load_vacancies(keyword)
        self.file_worker.save_vacancies_to_disk(vacancies)

    @abstractmethod
    def load_vacancies(self, keyword):
        """ Загрузка вакансий из удаленного ресурса """
        pass

    @abstractmethod
    def get_vacancies(self):
        """ Чтение вакансий с файла на диске """
        pass


class HeadHunterAPI(Parser):
    """
    Класс для работы с API HeadHunter
    """
    def __init__(self, file_worker, keyword=""):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        super().__init__(file_worker, keyword)

    def get_vacancies(self):
        """ Чтение вакансий с файла на диске """
        return self.file_worker.read_vacancies_from_disk()

    def load_vacancies(self, keyword=""):
        """ Загрузка вакансий из удаленного ресурса HH.ru"""
        self.params['text'] = keyword
        hh_vacancies = []
        page_max_count = 10
        while self.params.get('page') != page_max_count:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            self.params['page'] += 1
            print(f"Чтение страницы hh №{self.params['page'] } из {page_max_count}")
            hh_vacancies.extend(response.json()['items'])
        self.params['page'] = 0
        return Vacancy.cast_to_object_list(hh_vacancies)
