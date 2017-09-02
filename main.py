import math
import json
import requests

BASE_URL = 'https://backend-challenge-winter-2017.herokuapp.com/customers.json'


def is_valid_length(obj, word):
    if 'min' in obj and len(word) < obj['min']:
        return False
    if 'max' in obj and len(word) > obj['max']:
        return False
    else:
        return True


def is_valid_type(customer_val, type_val):
    field_type = str(type(customer_val).__name__)

    if field_type == 'str' and type_val == 'string':
        return True
    if field_type == 'int' and type_val == 'number':
        return True
    if field_type == 'bool' and type_val == 'boolean':
        return True
    else:
        return False


def get_invalid_customers(all_invalid_customers, page_num):
    resp = requests.get(BASE_URL + '?page=' + str(page_num))
    data = json.loads(resp.text)

    customers = data['customers']
    validations = data['validations']

    for customer in customers:
        invalid_customer_fields = []

        for validation in validations:
            field = list(validation)[0]

            if field in customer and customer[field] is not None:

                if ('type' in validation[field] and not
                        is_valid_type(customer[field], validation[field]['type'])):
                    invalid_customer_fields.append(field)

                if ('length' in validation[field] and not
                        is_valid_length(validation[field]['length'], customer[field])):
                    invalid_customer_fields.append(field)

            else:
                if ('required' in validation[field] and
                        validation[field]['required'] is True):
                    invalid_customer_fields.append(field)

        if len(invalid_customer_fields) != 0:
            invalid_customer = {'id': customer['id'],
                                'invalid_fields': invalid_customer_fields}
            all_invalid_customers.append(invalid_customer)


def main():
    resp = requests.get(BASE_URL)
    data = json.loads(resp.text)
    all_invalid_customers = []

    total_pages = data['pagination']['total']
    per_page = data['pagination']['per_page']
    current_page = data['pagination']['current_page']
    num_pages = math.ceil(total_pages / per_page)

    for page in range(1, num_pages + 1):
        get_invalid_customers(all_invalid_customers, page)

    result = json.dumps({"invalid_customers": all_invalid_customers})
    print(result)


main()
