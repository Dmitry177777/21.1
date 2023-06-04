from django.core.management import BaseCommand
from main.models import Category, Product


class Command(BaseCommand):
	def handle (self, *args, **options):

		# очистка модели Category
		records = Category.objects.all()
		records.delete()

		category_list =[
			{
				'product_category': 'Посуда',
				'description': 'Тарелки, кружки и т.п.',
				'is_active': True
			},
			{
				'product_category': 'Сковородки',
				'description': 'Сковородки блинные, wok, сотейники',
				'is_active': True
			},
			{
				'product_category': 'Кастрюли',
				'description': 'Кастрюли, наборы кастрюль',
				'is_active': True
			},
			{
				'product_category': 'Товары для обуви, одежды',
				'description': 'Аксесуары для обуви и одежды',
				'is_active': True
			},
			{
				'product_category': 'Фурнитура',
				'description': 'Ручки, замки и фурнитура',
				'is_active': True
			},
			{
				'product_category': 'Ручная работа',
				'description': 'Авторские товары ручной работы',
				'is_active': True
			},
			{
				'product_category': 'Умный дом',
				'description': 'Аксесуары для умного дома',
				'is_active': True
			},
			{
				'product_category': 'Товар для ухода за животными',
				'description': 'Коврики,перенорски, игрушки для животных',
				'is_active': False
			},
			{
				'product_category': 'Инструменты ручные',
				'description': 'Пассатижи, отвертки, клещи',
				'is_active': True
			},

			{
				'product_category': 'Письменные принаджежности',
				'description': 'тетрадки, блокноты, бумага',
				'is_active': True
			},
			{
				'product_category': 'Печатная продукция',
				'description': 'Журналы, газеты, книги, энциклопедии',
				'is_active': False
			},
			{
				'product_category': 'Электронные издания',
				'description': 'Художественная литература, Проза, Журналистика, Историчесские эссе',
				'is_active': True
			},

		]
		category_objects =[]
		for category_item in category_list:
			category_objects.append(
				Category(**category_item)
			)
		Category.objects.bulk_create(category_objects)

		# очистка модели Product
		records = Product.objects.all()
		records.delete()

		product_list = [
			{
				'product_name': 'Тетрадь 20 стр.',
				'description': 'тетрадки',
				'product_category': Category.objects.get(product_category='Письменные принаджежности'),
				'is_active': True
			},
			{
				'product_name': 'Журнал',
				'description': 'Журналы',
				'product_category': Category.objects.get(product_category='Печатная продукция'),
				'is_active': False
			},
			{
				'product_name': 'Книга о войне',
				'description': 'Книги',
				'product_category': Category.objects.get(product_category='Печатная продукция'),
				'is_active': True
			},
			{
				'product_name': 'Книга о любви',
				'description': 'Книги',
				'product_category': Category.objects.get(product_category='Печатная продукция'),
				'is_active': True
			},
			{
				'product_name': 'умная розетка',
				'description': 'розетки электрические',
				'product_category': Category.objects.get(product_category='Умный дом'),
				'is_active': True
			},
			{
				'product_name': 'умная лампочка',
				'description': 'лампочки',
				'product_category': Category.objects.get(product_category='Умный дом'),
				'is_active': True
			},
			{
				'product_name': 'умная колонка',
				'description': 'колонки',
				'product_category': Category.objects.get(product_category='Умный дом'),
				'is_active': True
			},
			{
				'product_name': 'умная лампочка рев.2',
				'description': 'лампочки',
				'product_category': Category.objects.get(product_category='Умный дом'),
				'is_active': True
			},
			{
				'product_name': 'умная лампочка рев.3',
				'description': 'лампочки',
				'product_category': Category.objects.get(product_category='Умный дом'),
				'is_active': True
			},
			{
				'product_name': 'Мемуары маршала Жукова',
				'description': 'Книги',
				'product_category': Category.objects.get(product_category='Умный дом'),
				'is_active': True
			},
			{
				'product_name': 'Сковорода Tefal',
				'description': 'Tefal',
				'product_category': Category.objects.get(product_category='Сковородки'),
				'is_active': True
			},
			{
				'product_name': 'Сковорода Bork',
				'description': 'Bork',
				'product_category': Category.objects.get(product_category='Сковородки'),
				'is_active': True
			},
			{
				'product_name': 'Сковорода Russo',
				'description': 'Russo',
				'product_category': Category.objects.get(product_category='Сковородки'),
				'is_active': True
			},
			]


		product_objects = []
		for product_item in product_list:
			product_objects.append(
				Product(**product_item)
			)
		Product.objects.bulk_create(product_objects)


