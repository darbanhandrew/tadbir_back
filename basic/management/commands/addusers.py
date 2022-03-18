from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
import json
import codecs

from basic.models import User, Role, BimeShavanadeGharardad, Gharardad


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        data1 = json.load(codecs.open(
            BASE_DIR / 'media/data.json', 'r', 'utf-8-sig'))
        data2 = json.dumps(data1)
        for json_user in data1["NewDataSet"]:
            print(json_user["melli_code"])
            user = User.objects.create_user(
                json_user["melli_code"], '', json_user["melli_code"][-6:])
            user.melli_code = json_user["melli_code"]
            user.first_name = json_user["fisrt_name"]
            user.last_name = json_user["last_name"]
            user.age = 1400 - int(json_user["age"])
            if json_user["is_asli"] == "True":
                user.is_asli = True
            else:
                user.is_asli = False
            user.roles.add(Role.objects.get(pk=1))
            user.save()
            if json_user["bime"] == "ma":
                BimeShavanadeGharardad.objects.create(
                    bimeshavande=user, gharardad=Gharardad.objects.first())
            else:
                BimeShavanadeGharardad.objects.create(
                    bimeshavande=user, gharardad=Gharardad.objects.last())
        self.stdout.write(self.style.SUCCESS('Successfully closed poll'))
