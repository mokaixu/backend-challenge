import requests, json, math

def validate_length(obj, word):
    if "min" in obj and len(word) < obj["min"]:
        return False
    if "max" in obj and len(word) > obj["max"]:
        return False
    else:
        return True
    
BASE_URL = "https://backend-challenge-winter-2017.herokuapp.com/customers.json"





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
    resp = requests.get(BASE_URL+"?page=" + str(page_num))
    data = json.loads(resp.text)

    total_pages = data['pagination']['total']
    per_page = data['pagination']['per_page']
    current_page = data['pagination']['current_page']
    num_pages = math.ceil(total_pages / per_page)

    customers = data['customers']
    validations = data['validations']

    for customer in customers:
        invalid_per_customer = []

        for validation in validations:
            root_key = list(validation)[0]
            

            if root_key in customer and customer[root_key] is not None:
                
                # you can probably get rid of this for loop
                # if validation[root_key][type] is not null (aka it exists) check if it is valid
                if 'type' in validation[root_key] and not is_valid_type(customer[root_key], validation[root_key]['type']):
                    invalid_per_customer.append(root_key)
                   # print("the invalid key of "  + str(customer["id"]) + "is " + root_key)

                    # check that the string associated with the length is not null
                if 'length' in validation[root_key] and not validate_length(validation[root_key]['length'], customer[root_key]):
                    invalid_per_customer.append(root_key)
                   # print("the invalid key of "  + str(customer["id"]) + "is " + root_key)
            else:
                if 'required' in validation[root_key] and validation[root_key]['required'] == True:
                    invalid_per_customer.append(root_key)
                   # print("the invalid key of " + str(customer["id"])+  "is " + root_key)
        if len(invalid_per_customer) != 0:
            invalid_customer = {'id': customer['id'], 'invalid_fields': invalid_per_customer}
            customerData.append(invalid_customer)
        
    
def main():
    resp = requests.get(BASE_URL)
    data = json.loads(resp.text)
    all_invalid_customers = []

    total_pages = data['pagination']['total']
    per_page = data['pagination']['per_page']
    current_page = data['pagination']['current_page']
    num_pages = math.ceil(total_pages / per_page)
    
    for page in range(1, num_pages+1):
        get_invalid_customers(all_invalid_customers, page)
        
    result = json.dumps({"invalid_customers": all_invalid_customers})
    print(result)

main()

    



                  
        
                  
    
    
    
