import os
import datetime
import csv

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from frontend import utils


@csrf_exempt
def generate_data(request):
    if request.method == 'POST':
        base_mixin = utils.BaseMixin()
        data_for_write = base_mixin.data_generate(int(request.POST.get('rows')), request.POST.get('name'),
                                               request.POST.get('user'))

        path_schemas = os.path.join(settings.MEDIA_ROOT, request.POST.get('user'), 'data_schemas')
        if not os.path.exists(path_schemas):
            os.mkdir(path_schemas)

        now_date = datetime.datetime.now().strftime("%Y-%B-%d-%H-%M-%S")
        file_name = f"{request.POST.get('name')}_{now_date}.csv"
        with open(os.path.join(path_schemas, file_name), 'w') as file:
            writer = csv.writer(file)
            writer.writerows(data_for_write)

        return JsonResponse(
            {'date': now_date,
             'file_name': file_name}
        )
