from django.core.management import BaseCommand
from main.models import Category, Product
from users.models import User


class Command(BaseCommand):
	def handle (self, *args, **options):

		# создание суперюзера
		user = User.objects.create(
			email='admin@sky.pro',
			first_name = 'admin',
			last_name = 'SkyPro',
			is_staff = True,
			is_superuser = True
		)

		user.set_password('admin171717')
		user.save()


