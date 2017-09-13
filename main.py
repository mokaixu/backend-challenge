import math
import json
import requests

BASE_URL = 'https://backend-challenge-winter-2017.herokuapp.com/customers.json'

type_dict = {"string": str, "number": int, "boolean": bool}


def is_valid_length(word, length_validation_obj):
    """Returns whether word is valid based on JSON object for length"""
    if 'min' in length_validation_obj and len(word) < length_validation_obj['min']:
        return False
    if 'max' in length_validation_obj and len(word) > length_validation_obj['max']:
        return False
    else:
        return True


def is_valid_type(customer_val, type_val):
    """Returns whether the value corresponding to
       a customer's data fields are of valid type"""
    if type_dict.get(type_val) == type(customer_val):
        return True
    else:
        return False


def get_invalid_customers(all_invalid_customers, page_num):
    """Returns list of invalid customer IDs and their
       corresponding invalid fields"""
    resp = requests.get(BASE_URL,  data= {'page': page_num})
    data = json.loads(resp.text)

    customers = data['customers']
    validations = data['validations']

    for customer in customers:
        invalid_customer_fields = []

        for validation in validations:
            # since validation is an object with one key-value pair, we take the first key
            field = list(validation.keys())[0]

            if field in customer and customer[field] is not None:

                if ('type' in validation[field] and not
                        is_valid_type(customer[field], validation[field]['type'])):
                    invalid_customer_fields.append(field)

                if ('length' in validation[field] and not
                        is_valid_length(customer[field], validation[field]['length'])):
                    invalid_customer_fields.append(field)

            else:
                if ('required' in validation[field] and
                        validation[field]['required'] is True):
                    invalid_customer_fields.append(field)

        if len(invalid_customer_fields) != 0:
            invalid_customer = {'id': customer['id'],
                                'invalid_fields': invalid_customer_fields}
            all_invalid_customers.append(invalid_customer)

            
def get_data(url):
    """Retrieves JSON data from endpoint"""
    resp = requests.get(url)
    return json.loads(resp.text)
    

def main():

    all_invalid_customers = []
    data = get_data(BASE_URL)
    total_pages = data['pagination']['total']
    per_page = data['pagination']['per_page']
    current_page = data['pagination']['current_page']
    num_pages = math.ceil(total_pages / per_page)

    for page in range(1, num_pages + 1):
        get_invalid_customers(all_invalid_customers, page)

    result = json.dumps({"invalid_customers": all_invalid_customers})
    print(result)

if __name__ == "__main__":
    main()
