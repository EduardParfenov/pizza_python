# Заказ #
from Pizza import Pizza, PizzaBBQ, PizzaPepperoni, PizzaSeafood
import datetime


class Order:
    def __init__(self):
        # Список с заказанными пиццами
        self.amount = []
        # Ширина чека
        self.len_card = 52

        # Время создания и готовности заказа
        self.order_creation_time = datetime.datetime.now()
        self.preparation_time = datetime.timedelta()

        # Подсчёт всех пицц и их полной стоимости
        self.total_pizzas_amount = 0
        self.total_price = 0

        # Статус готовности заказа
        self.readiness = False

    # Узнаём время готовности заказа
    def find_preparation_time(self):
        # Проходимся по всем пиццам в заказе и выбираем макс. время
        # для приготовления.
        biggest_time_preparing = max([pizza.time_preparing for pizza in self.amount])\
            if len(self.amount) > 0 else self.preparation_time
        self.preparation_time = biggest_time_preparing \
            if self.preparation_time < biggest_time_preparing else self.preparation_time

    # метод добавления пицц
    def add_amount(self):
        add_amount = input('\nДобавить пиццу в заказ? да/нет\n'
                           '->: ').lower().strip()

        while add_amount != 'нет':
            if add_amount == 'да':
                select = input('\nКакую пиццу желаете выбрать?\n'
                               '1. "Маргарита" \n'
                               '2. "Барбекю" \n'
                               '3. "Пепперони" \n'
                               '4. "Пицца с морепродуктами" \n'
                               '->: ')

                def connect_file_pizza(a):
                    pizza = a
                    # Добавить ингредиент
                    pizza.add_filling()
                    # Удалить ингредиент
                    pizza.del_filling()
                    # Выводим информацию о выбранной пицце
                    # с учётом добавленных и удалённых ингредиентов
                    pizza.get_info()
                    # time.sleep(2)
                    # Добавляем её в заказ
                    self.amount.append(pizza)
                    # Добавляем пиццу и её стоимость
                    self.total_pizzas_amount += 1
                    self.total_price += pizza.new_price
                    return pizza

                if select == '1':
                    connect_file_pizza(Pizza())
                elif select == '2':
                    connect_file_pizza(PizzaBBQ())
                elif select == '3':
                    connect_file_pizza(PizzaPepperoni())
                elif select == '4':
                    connect_file_pizza(PizzaSeafood())
                else:
                    print(f'Сделайте выбор согласно меню!')
                add_amount = ''
            elif add_amount == 'нет':
                print('Выбор закончен.')
                break
            else:
                print('Выберите "да" или "нет"!')
                add_amount = input('\nХотите добавить пиццу в заказ? да/нет\n'
                                   '->: ').lower().strip()
        self.find_preparation_time()
        print('Ваш заказ:')
        self.show_orders()

    # Вывод информации о заказе
    def show_orders(self):
        # Проверяем готовность заказа
        self.readiness = True \
            if datetime.datetime.now() > self.order_creation_time + self.preparation_time else False

        def dist(x):
            distance = self.len_card - len(x)
            return distance

        # Словари для сохранения стоимости и подсчёта пицц
        pizza_amount = dict()
        pizza_cost = dict()

        for num in range(len(self.amount)):
            # Переменная, которая принимает пиццы из списка self.amount по имени
            pizza_name = self.amount[num].name
            # Храним стоимость каждой пиццы
            cost = self.amount[num].new_price
            if pizza_name in pizza_amount:
                pizza_amount[pizza_name] += 1
                pizza_cost[pizza_name] += cost
            else:
                pizza_amount[pizza_name] = 1
                pizza_cost[pizza_name] = cost

        # Добавляем текст вывода в переменные чтоб в дальнейшем их
        # вывести в отформатированном формате
        total_pizza = f' Всего заказано пицц: {len(self.amount)} шт.'
        order_creation_time = f' Время заказа: {self.order_creation_time.strftime("%d-%m-%y %H:%M:%S")}'
        ready_time = self.order_creation_time + self.preparation_time
        order_preparation_time = f' Время готовности:' \
                                 f' {ready_time.strftime("%d-%m-%y %H:%M:%S") if self.readiness is False else "Ваш заказ готов."}'
        total_price_string = f' Сумма: {self.total_price} р.'

        # Вывод заказа
        print(f'+{"-" * self.len_card}+\n'
              f'|{total_pizza}{" " * dist(total_pizza)}|\n'
              f'|{" " * self.len_card}|')
        # Выводим название, количество и сумму каждого вида пиццы
        for pizzas, pizza_sum in zip(pizza_amount.items(), pizza_cost.values()):
            output = f' {pizzas[0]} - {pizzas[1]} шт. - {pizza_sum} руб.'
            print(f'|{output}{" " * dist(output)}|')
        print(f'|{" " * self.len_card}|\n'
              f'|{total_price_string}{" " * dist(total_price_string)}|\n'
              f'|{" " * self.len_card}|\n'
              f'|{order_creation_time}{" " * dist(order_creation_time)}|\n'
              f'|{order_preparation_time}{" " * dist(order_preparation_time)}|\n'
              f'+{"-" * self.len_card}+')
