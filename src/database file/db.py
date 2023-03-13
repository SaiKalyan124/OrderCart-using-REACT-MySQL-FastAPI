import pymongo
import xml.etree.ElementTree as ET
import os

# create a client object
# client = pymongo.MongoClient("mongodb://localhost:27017/")
myclient = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.vo5ipzy.mongodb.net/?retryWrites=true&w=majority")


# Create a database and collections to store the order data
db = myclient["order_database"]
# Check if collections exist, if not create them
if "orders" not in db.list_collection_names():
    orders_collection = db.create_collection("orders")
else:
    orders_collection = db["orders"]

if "orderlines" not in db.list_collection_names():
    orderlines_collection = db.create_collection("orderlines")
else:
    orderlines_collection = db["orderlines"]

if "customers" not in db.list_collection_names():
    customer_collection = db.create_collection("customers")
else:
    customer_collection = db["customers"]

if "addresses" not in db.list_collection_names():
    address_collection = db.create_collection("addresses")
else:
    address_collection = db["addresses"]


xml_file_path = os.path.join(os.path.dirname(__file__), 'sample.xml')
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Loop through each order in the XML file
for order in root.findall('./Orders/Order'):
    # Extract the order data
    reference_num = order.find('ReferenceNum').text
    country_code = order.find('CountryCode').text

    # Extract the customer data
    customer = order.find('Customer')
    customer_code = customer.find('CustomerCode').text
    first_name = customer.find('FirstName').text
    last_name = customer.find('LastName').text
    phone = customer.find('Phone').text
    email = customer.find('Email').text

    # Extract the address data
    address = order.find('Address')
    full_name = address.find('FullName').text
    address_type = address.find('AddressType').text
    address_line1 = address.find('AddressLine1').text
    address_line2 = address.find('AddressLine2').text

print(reference_num,country_code)

    # Insert the address data into the address collection
    # address_id = address_collection.insert_one({
    #     'full_name': full_name,
    #     'address_type': address_type,
    #     'address_line1': address_line1,
    #     'address_line2': address_line2,
    # }).inserted_id

    # # Insert the customer data into the customer collection
    # customer_id = customer_collection.insert_one({
    #     'customer_code': customer_code,
    #     'first_name': first_name,
    #     'last_name': last_name,
    #     'phone': phone,
    #     'email': email,
    #     'address_id': address_id
    # }).inserted_id

    # # Insert the order data into the orders collection
    # order_id = orders_collection.insert_one({
    #     'reference_num': reference_num,
    #     'country_code': country_code,
    #     'customer_id': customer_id
    # }).inserted_id

    # # Loop through each order line in the order
    # for orderline in order.findall('./OrderLines/OrderLine'):
    #     # Extract the order line data
    #     item_num = orderline.find('ItemNum').text
    #     item_description = orderline.find('ItemDescription').text

    #     # Insert the order line data into the orderlines collection
    #     orderline_id = orderlines_collection.insert_one({
    #         'order_id': order_id,
    #         'item_num': item_num,
    #         'item_description': item_description
    #     }).inserted_id

# orders = root.findall("./Orders/Order")

# # Display the order data and prompt the user to update it
# for order in orders:
#     print("Order details:")
#     print("Reference Number:", order.find("ReferenceNum").text)
#     print("Country Code:", order.find("CountryCode").text)
#     print("Full Name:", order.find("Address/FullName").text)
#     print("Address Type:", order.find("Address/AddressType").text)
#     print("Address Line 1:", order.find("Address/AddressLine1").text)
#     print("Address Line 2:", order.find("Address/AddressLine2").text)
#     print("Customer Code:", order.find("Customer/CustomerCode").text)
#     print("First Name:", order.find("Customer/FirstName").text)
#     print("Last Name:", order.find("Customer/LastName").text)
#     print("Phone:", order.find("Customer/Phone").text)
#     print("Email:", order.find("Customer/Email").text)

#     # Prompt the user to update the order
#     new_ref_num = input("Enter new reference number (leave empty to keep the same): ")
#     if new_ref_num:
#         order.find("ReferenceNum").text = new_ref_num

#     new_country_code = input("Enter new country code (leave empty to keep the same): ")
#     if new_country_code:
#         order.find("CountryCode").text = new_country_code

#     new_full_name = input("Enter new full name (leave empty to keep the same): ")
#     if new_full_name:
#         order.find("Address/FullName").text = new_full_name

#     new_address_type = input("Enter new address type (leave empty to keep the same): ")
#     if new_address_type:
#         order.find("Address/AddressType").text = new_address_type

#     new_address_line1 = input("Enter new address line 1 (leave empty to keep the same): ")
#     if new_address_line1:
#         order.find("Address/AddressLine1").text = new_address_line1

#     new_address_line2 = input("Enter new address line 2 (leave empty to keep the same): ")
#     if new_address_line2:
#         order.find("Address/AddressLine2").text = new_address_line2

#     new_customer_code = input("Enter new customer code (leave empty to keep the same): ")
#     if new_customer_code:
#         order.find("Customer/CustomerCode").text = new_customer_code

#     new_first_name = input("Enter new first name (leave empty to keep the same): ")
#     if new_first_name:
#         order.find("Customer/FirstName").text = new_first_name

#     new_last_name = input("Enter new last name (leave empty to keep the same): ")
#     if new_last_name:
#         order.find("Customer/LastName").text = new_last_name

#     new_phone = input("Enter new phone number (leave empty to keep the same): ")
#     if new_phone:
#         order.find("Customer/Phone").text = new_phone

#     new_email = input("Enter new email address (leave empty to keep the same): ")
#     if new_email:
#         order.find("Customer/Email").text = new_email

#     print("Order updated successfully.\n")