import datetime
import os


class Terminal:
    def __init__(self):
        # Отдельно сохраняется информация о продавце(если вдруг будем добавлять в класс
        # новые свойства/методы) и его ФИО
        self.current_seller = None
        self.current_seller_info = None

        # Списки с готовыми заказами и заказами в процессе готовки. Также список с актуальными пиццами
        self.orders = list()
        self.ready_orders = list()
        self.dishes_from_menu = list()

        # Информация об активации терминала
        self.start_working_time = None
        self.activ = False

        # Информация для чека. Количество заказов, проданных пицц и суммарная выручка
        self.orders_made = 0
        self.sold_pizzas = 0
        self.total_revenue = 0

    # Метод для включения терминала, принимает на вход экземпляр класса "Salesman"
    def start_working(self, current_seller: object):
        if self.activ is False:
            self.activ = True
            self.current_seller = current_seller
            self.current_seller_info = self.current_seller.fio
            self.start_working_time = datetime.datetime.now()
            return print(f'\n\nСмена открыта.Добро пожаловать.\n'
                         f'Ответственный продавец: {self.current_seller_info!r}\n')
        else:
            return print(f'\n\nСмена уже была открыта.\n'
                         f'Ответственный продавец: {self.current_seller_info!r}\n')

    '''
    Метод для прекращения работы терминала.
    
    Создаёт чек(и файл для чеков если такого ещё нет) с информацией продаж за день.
    А также обнуляет всю информацию в самом терминале.
    '''
    def end_working(self):
        # Проверяет активность смены.
        if self.activ is True:
            path = os.getcwd() + '\\checks\\'
            # Создаёт папку с чеками если таковой ещё не было.
            if os.path.exists(path) is False:
                os.mkdir(path)
            # Записываем время закрытия.
            closing_time = datetime.datetime.now()
            # Записываем всю информацию в файл.
            with open(path + closing_time.strftime('%d.%m.%y') + '.txt', 'a+', encoding='utf-8') as file_with_checks:
                day_info = f'{closing_time.strftime("%d.%m.%Y")}\n' \
                           f'Ответственный продавец: {self.current_seller_info}\n\n' \
                           f'Время открытия смены: {self.start_working_time.strftime("%X")}\n' \
                           f'Время закрытия смены: {closing_time.strftime("%X")}\n' \
                           f'Сделано заказов: {self.orders_made} шт.\n' \
                           f'Продано пицц: {self.sold_pizzas}\n' \
                           f'Суммарная выручка: {self.total_revenue} р.\n\n'
                file_with_checks.write(day_info)

            # Обнуляем информацию
            self.activ = False
            self.start_working_time = None
            self.current_seller = None
            self.current_seller_info = None
            self.sold_pizzas = self.orders_made = self.total_revenue = 0
            return print('Смена успешно закрыта.')
        else:
            return print('Смена закрыта.')

    # Вывод меню
    def print_menu(self):
        print('Меню: ')
        for _ in range(len(self.dishes_from_menu)):
            self.dishes_from_menu[_].get_info()

    # Создание заказа
    def create_order(self, new_order):
        self.orders.append(new_order)
        self.orders_made += 1
        self.sold_pizzas += len(self.orders[-1].amount)
        for pizza in self.orders[-1].amount:
            self.total_revenue += pizza.new_price

    # Проверка активных заказов
    def check_orders(self):
        for each_order in range(len(self.orders)):
            current_order = self.orders[each_order]
            if current_order.readiness is True:
                self.ready_orders.append(current_order)
                self.orders.pop(each_order)

        print(f'В процессе приготовления: {len(self.orders)}\n')
        for ord_num in range(len(self.orders)):
            print(f"Заказ №{ord_num+1} - ")
            self.orders[ord_num].show_orders()

    # Добавление пиццы в меню
    def add_dish_to_menu(self, dish: object):
        self.dishes_from_menu.append(dish)
