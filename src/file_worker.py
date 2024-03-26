from abc import ABC, abstractmethod
from src.vacancy import Vacancy
from typing import List
from config import DATA_DIR_PATH
import os
import json


class FileWorker(ABC):

    def __init__(self, file_name: str):
        self.file_path = os.path.join(DATA_DIR_PATH, file_name)

    @abstractmethod
    def save_vacancies_to_disk(self, vacancies: List[Vacancy]):
        """Сохранение полученных вакансии в файл на диск"""
        pass

    @abstractmethod
    def read_vacancies_from_disk(self):
        """Чтение вакансий из файла на диске"""
        pass

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy):
        """Добавление вакансии в файл"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy):
        """Удаление вакансии из файла"""
        pass


class JsonWorker(FileWorker):

    def __init__(self, file_name: str):
        super().__init__(file_name)

    def save_vacancies_to_disk(self, vacancies: List[Vacancy]):
        """Сохранение полученных вакансии в Json файл на диск"""
        with open(self.file_path, 'w', encoding="utf-8") as file:
            json.dump(vacancies,
                      file,
                      default=lambda o: o.to_dict(),
                      indent=4,
                      ensure_ascii=False)

    def read_vacancies_from_disk(self) -> List[Vacancy]:
        """Чтение вакансий из Json файла на диске"""
        if not os.path.isfile(self.file_path):
            return []

        with open(self.file_path, 'r', encoding="utf-8") as file:
            data = json.load(file, object_hook=Vacancy.to_object)
        return data

    def add_vacancy(self, vacancy: Vacancy):
        """Добавление вакансии в Json файл"""
        vacancies = self.read_vacancies_from_disk()
        vacancies.append(vacancy)
        self.save_vacancies_to_disk(vacancies)

    def delete_vacancy(self, vacancy: Vacancy):
        """Удаление вакансии из Json файла"""
        vacancies = self.read_vacancies_from_disk()
        vacancy_by_id = next((e for e in vacancies if e.id == vacancy.id), None)
        if vacancy_by_id:
            vacancies.remove(vacancy_by_id)
        self.save_vacancies_to_disk(vacancies)
