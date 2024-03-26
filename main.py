from src.vacancy import Vacancy, SalaryRange
from src.file_worker import JsonWorker
from src.head_hunter_api import HeadHunterAPI
from src.utils import Utils
from typing import List

# По данному ключевому слову будет выполнять request c hh
MAIN_KEYWORD = "Python"


def user_interaction():
    """Функция для взаимодействия с пользователем"""

    # данные ключевые слова ищутся как подстроки в том, что загрузило по ключевому слову MAIN_KEYWORD
    filter_words = input("Введите ключевые слова для фильтрации вакансий через пробел: ").lower().split()

    # Максимальное кол-во вакансий в выводе
    top_n = 0
    while True:
        try:
            top_n = int(input("Введите количество вакансий для вывода в топ N: "))
        except ValueError:
            print("Введенные границы диапазона должны быть целыми числами")
            continue
        break

    # Диапазон зарплат.
    while True:
        salary_range = input("Введите диапазон зарплат: ").replace(' ', '').split('-')  # Пример: 100000 - 150000     ["80000", "200000"]
        if len(salary_range) != 2:
            print('Введенный диапазон должен состоять из двух целых чисел')
            continue
        try:
            salary_range = range(int(salary_range[0]), int(salary_range[1]))
        except ValueError:
            print("Введенные границы диапазона должны быть целыми числами")
            continue
        break

    # Json file worker
    json_worker = JsonWorker(file_name="vacancies.json")

    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterAPI(json_worker, keyword=MAIN_KEYWORD)

    # # Проверка добавления / удаления своей вакансии на диск # #
    vacancy = Vacancy("0", "Python Developer", "", SalaryRange(100_000, 150_000), "Опыт работы от 3 лет...",
                      "Разработка согласно ТЗ...")
    # Сохранение информации о вакансиях в файл + проверка
    hh_api.file_worker.add_vacancy(vacancy)
    vacancies_list = hh_api.file_worker.read_vacancies_from_disk()
    if vacancy in vacancies_list:
        print('Вакансия добавлена успешно')
    else:
        print('Ошибка добавления вакансии')

    # Удаление информации о вакансиях из файла + проверка
    hh_api.file_worker.delete_vacancy(vacancy)
    vacancies_list = hh_api.file_worker.read_vacancies_from_disk()
    if vacancy not in vacancies_list:
        print('Вакансия удалена успешно')
    else:
        print('Ошибка удаления вакансии')

    # # Блок сортировки/фильтрации вакансий согласно введенным пользователем параметрам
    filtered_vacancies = Utils.filter_vacancies(vacancies_list, filter_words)
    ranged_vacancies = Utils.get_vacancies_by_salary(filtered_vacancies, salary_range)  # что за валюта не учитывается.
    sorted_vacancies = Utils.sort_vacancies_by_salary(ranged_vacancies)
    top_vacancies = Utils.get_top_vacancies(sorted_vacancies, top_n)

    # Вывод информации о подобранных вакансиях
    Utils.print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
