import os
import csv
import datetime
import string
import random

from django.conf import settings

class BaseMixin:
    def get_current_schemas(self, username: str) -> list:
        """
        Return a list of schemas.
        """
        path_schemas = os.path.join(settings.MEDIA_ROOT, username)
        if os.path.exists(path_schemas):
            return self._get_schemas_list(path_schemas)
        else:
            os.mkdir(path_schemas)
            return []

    def get_data_schemas(self, name: str, username: str) -> list:
        path_schemas = os.path.join(settings.MEDIA_ROOT, username, 'data_schemas')
        if not os.path.exists(path_schemas):
            os.mkdir(path_schemas)
        files_list = self._get_schemas_list(path_schemas)
        return self._clean_schemas_list(name, files_list)


    def get_schema_info(self, name: str, username: str) -> list:
        """
        Return a list of schema's column headers
        """
        for schema in self._get_schemas_list(os.path.join(settings.MEDIA_ROOT, username)):
            match schema:
                case {'name': schema_name, 'modified': date} if schema_name == name:
                    return self._read_csv_header(os.path.join(settings.MEDIA_ROOT, username,
                                                              f'{schema_name}_{date}.csv'))

    def save_schema(self, data: dict, username: str) -> bool:
        path_schemas = os.path.join(settings.MEDIA_ROOT, username)

        for file_name in os.listdir(path_schemas):
            if data.get('name_schema')[0].strip() in file_name:
                new_file_name = self._rename_schema(path_schemas, file_name)
                if new_file_name:
                    break
        else:
            now_date = datetime.datetime.now().strftime("%Y-%B-%d")
            new_file_name = f'{data.get("name_schema")[0].strip()}_{now_date}.csv'

        header_list: list = self._build_data_header(data)
        return self.create_schema(path_schemas, new_file_name, header_list)

    def delete_schema(self, name: str, username: str) -> bool:
        path_schemas = os.path.join(settings.MEDIA_ROOT, username)
        for file in self._get_schemas_list(path_schemas):
            if file.get('name') == name:
                os.remove(os.path.join(path_schemas, f'{file.get("name")}_{file.get("modified")}.csv'))
                return os.path.exists(os.path.join(path_schemas, f'{file.get("name")}_{file.get("modified")}.csv'))
        else:
            return False

    def data_generate(self, rows: int, name: str, username: str):
        schema_info = self.get_schema_info(name, username)
        data_for_write = []
        for i in range(rows):
            row_i = []
            for column in schema_info:
                match column:
                    case {'name': _, 'type': 'full name', 'order': _}:
                        row_i.append(self.generate_full_name())
                    case {'name': _, 'type': 'job', 'order': _}:
                        row_i.append(self.generate_job())
                    case {'name': _, 'type': 'phone number', 'order': _}:
                        row_i.append(self.generate_phone_number())
                    case {'name': _, 'type': 'email', 'order': _}:
                        row_i.append(self.generate_email())
                    case {'name': _, 'type': 'data', 'order': _}:
                        row_i.append(self.generate_data())
            data_for_write.append(row_i)
        return data_for_write

    @classmethod
    def generate_full_name(cls):
        letters = string.ascii_lowercase
        first_name = ''.join(random.choice(letters) for i in range(random.randint(4, 9))).capitalize()
        last_name = ''.join(random.choice(letters) for i in range(random.randint(4, 9))).capitalize()
        return f"{first_name} {last_name}"

    @classmethod
    def generate_job(cls):
        letters = string.ascii_lowercase
        company = ''.join(random.choice(letters) for i in range(random.randint(4, 12))).capitalize()
        return company

    @classmethod
    def generate_phone_number(cls):
        letters = string.digits
        phone_number = ''.join(random.choice(letters) for i in range(random.randint(11, 12)))
        return '+' + phone_number

    @classmethod
    def generate_email(cls):
        letters = string.ascii_letters
        email_list = ['gmail.com', 'yahoo.com', 'planeks.net']
        name_email = ''.join(random.choice(letters) for i in range(random.randint(4, 15)))
        return f"{name_email}@{random.choice(email_list)}"

    @classmethod
    def generate_data(cls):
        start_date = datetime.datetime.now()
        end_date = start_date + datetime.timedelta(days=50)
        random_date = start_date + (end_date - start_date) * random.random()
        return str(random_date)

    @classmethod
    def create_schema(cls, path: str, name: str, header_list: list) -> bool:
        try:
            with open(os.path.join(path, name), 'w') as file:
                writer = csv.writer(file)
                writer.writerow(header_list)
            return True
        except FileNotFoundError:
            return False

    @classmethod
    def _build_data_header(cls, data:dict) -> list:
        count = 1
        header_list = []

        for i in range(len(data.get('order'))):
            for el in data.get('order'):
                if el == str(count):
                    el_index = data.get('order').index(el)
                    header_list.append(
                        f'{data.get("name_input")[el_index]} ({data.get("type_select")[el_index]})'
                    )
                    count += 1
        return header_list

    @classmethod
    def _rename_schema(cls, path: str, name: str) -> str:
        now_date = datetime.datetime.now().strftime("%Y-%B-%d")
        new_name = f'{name.rsplit("_", 1)[0]}_{now_date}.csv'
        os.rename(f'{path}/{name}', f'{path}/{new_name}')
        if os.path.exists(f'{path}/{new_name}'):
            return new_name

    @classmethod
    def _read_csv_header(cls, path_schemas: str) -> list:
        """
        Create a list of header column in csv template
        """
        data = None
        with open(os.path.join(path_schemas), 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data = row
                break
        if data:
            data = list(map(lambda x: {
                'name': x.split('(')[0].strip(),
                'type': x.split('(')[1].rstrip(')'),
                'order': data.index(x) + 1
            }, data))
            return data
        else:
            return []

    @classmethod
    def _get_schemas_list(cls, path_schemas: str) -> list:
        """
        Read directory and create a list of schemas.
        """
        schemas_list = []
        for file in os.listdir(path_schemas):
            if '.csv' in file:
                schemas_list.append({
                    'name': file.rsplit('_', 1)[0],
                    'modified': file.rsplit('_', 1)[1].rsplit('.', 1)[0],
                    'link': file
                })
        return schemas_list

    @classmethod
    def _clean_schemas_list(cls, name: str, files_list: list) -> list:
        clean_list = []
        for el in files_list:
            if el.get('name') == name:
                clean_list.append(el)
        return clean_list
