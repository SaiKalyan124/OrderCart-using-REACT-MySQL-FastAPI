import mysql.connector
import os
import xml.etree.ElementTree as ET
from fastapi import FastAPI, HTTPException, Request, APIRouter
import requests
import json
from pydantic import BaseModel,validator,Field
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Password@124#",
  database="Cart"
)
class order_items(BaseModel):
    ItemNum: str
    ItemDescription:str
class updated_order_date(BaseModel):
    CountryCode:str
    FullName:str
    AddressType:str
    AddressLine:str
    AddressLine2:str
    orderLines:list[order_items]
class Order(BaseModel):
    OrderID: int
    CustomerCode: str
    ReferenceNumber: str
    CountryCode:str
    FullName: str
    AddresType: str
    AddressLine1: str
    AddressLine2: str
    FirstName:str
    LastName:str
    Phone:str
    Email: str
    OrderLines: list[dict]

    # @validator('OrderLines')
    # def order_lines_must_not_be_empty(cls, v):
    #     if not v:
    #         raise ValueError('OrderLines must not be empty')
    #     return v


mycursor = mydb.cursor()
# Read XML to DB
@app.on_event("startup")
def read_xml_to_db():
  xml_file_path = os.path.join(os.path.dirname(__file__), 'sample.xml')
  tree = ET.parse(xml_file_path)
  root = tree.getroot()
  # Update the sequence numbers
  order_seq = 1
  order_line_seq = 1
  for order in root.findall('.//Order'):
    order.set('seq', str(order_seq))
    order_seq += 1
    for order_line in order.findall('.//OrderLine'):
        order_line.set('seq', str(order_line_seq))
        order_line_seq += 1
  tree.write('output.xml', encoding='utf-8')



  print("hello from read xml")

  # Loop through each order in the XML and insert into the OrderTable and OrderLineTable
  create_customer_table_query="""CREATE TABLE IF NOT EXISTS CustomerTable (	
                              CustomerCode varchar(255) PRIMARY KEY,	
                              FirstName varchar(255),	
                              LastName varchar(255),	
                              Phone varchar(255),	
                              Email varchar(255)
                              );"""
  create_order_table_query=""" CREATE TABLE IF NOT EXISTS OrderTable (    
                                OrderID INT PRIMARY KEY ,	
                                CustomerCode varchar(255),	
                                ReferenceNumber varchar(255),   
                                CountryCode varchar(255),   
                                FullName varchar(255),   
                                AddresType varchar(255),    
                                AddressLine1 varchar(255),    
                                AddressLine2 varchar(255),	
                                FOREIGN KEY (CustomerCode) REFERENCES CustomerTable(CustomerCode))
                                    ;"""
  create_order_line_table_query="""CREATE TABLE IF NOT EXISTS  OrderLineTable (	
                                    OrderLineID INT, 
                                    ItemNum varchar(255) PRIMARY KEY,	
                                    ItemDescription varchar(255)
                                    );"""
  create_order_to_orderlines="""CREATE TABLE IF NOT EXISTS orderToOrderLines(
                                OrderID INT,
                                ItemNum varchar(255),
                                PRIMARY KEY (ItemNum, OrderID),
                                FOREIGN KEY (OrderID) REFERENCES OrderTable(OrderID),
                                FOREIGN KEY (ItemNum) REFERENCES OrderLineTable(ItemNum)
                            );"""
  mycursor.execute(create_customer_table_query)
  mycursor.execute(create_order_table_query)
  mycursor.execute(create_order_line_table_query)
  mycursor.execute(create_order_to_orderlines)


  for order in root.findall('./Orders/Order'):        
      address = order.find('Address')
      customer = order.find('Customer')
      order_id=order.get('seq')    
      reference_number = order.find('ReferenceNum').text
      full_name = address.find('FullName').text
      address_type = address.find('AddressType').text
      address_line1 = address.find('AddressLine1').text
      address_line2 = address.find('AddressLine2').text
      customer_code = customer.find('CustomerCode').text
      country_code=order.find('CountryCode').text
      first_name=customer.find('FirstName').text
      last_name=customer.find('LastName').text
      phone=customer.find('Phone').text
      email=customer.find('Email').text
      

      # Insert Customer details
      customer_table_query='INSERT IGNORE INTO CustomerTable (CustomerCode, FirstName, LastName, Phone, Email) VALUES (%s, %s, %s, %s, %s)'
      customer_table_values=(customer_code, first_name, last_name, phone, email)
      mycursor.execute(customer_table_query,customer_table_values )
      
      # Insert Order Details
      order_table_query='INSERT IGNORE INTO OrderTable (OrderID, CustomerCode, ReferenceNumber,CountryCode, FullName, AddresType, AddressLine1, AddressLine2) VALUES (%s, %s, %s,%s,%s,%s, %s,%s)'
      order_table_values=(order_id, customer_code, reference_number,country_code, full_name, address_type, address_line1, address_line2 )
      mycursor.execute(order_table_query, order_table_values)      
      for order_line in order.find('OrderLines'):
            order_line_id = order_line.get('seq') 
            item_num = order_line.find('ItemNum').text
            item_description = order_line.find('ItemDescription').text
            order_line_table_query = 'INSERT IGNORE INTO OrderLineTable (OrderLineID, ItemNum, ItemDescription) VALUES (%s, %s, %s)'
            order_line_table_values = (order_line_id, item_num, item_description)
            mycursor.execute(order_line_table_query, order_line_table_values)
            order_to_orderlines_query="INSERT IGNORE INTO orderToOrderLines(OrderID,ItemNum) VALUES (%s,%s)"
            order_to_orderlines_values=(order_id,item_num)
            mycursor.execute(order_to_orderlines_query,order_to_orderlines_values)
      mydb.commit()

@app.get("/get_data/")
async def get_data():
  mycursor = mydb.cursor()

  # Select all the details of order
  select_query="""                
                SELECT o.OrderID, o.ReferenceNumber, o.CountryCode, o.FullName, o.AddresType, o.AddressLine1, o.AddressLine2, 
                    c.CustomerCode,c.FirstName, c.LastName, c.Phone, c.Email,
                    ol.OrderLineID,ol.ItemNum, ol.ItemDescription
                FROM OrderTable o
                INNER JOIN CustomerTable c ON o.CustomerCode = c.CustomerCode
                INNER JOIN orderToOrderLines oo ON o.OrderID = oo.OrderID
                INNER JOIN OrderLineTable ol ON oo.ItemNum = ol.ItemNum
                ORDER BY o.OrderID;
                """
  mycursor.execute(select_query)

  # fetch all rows as a list of dictionaries
  orders = mycursor.fetchall()

  # create a dictionary to store the order lines for each OrderID
  orders_dict = {}

  # Iterate through orders and add to orders_dict
  for order in orders:
      order_id = order[0]
      if order_id not in orders_dict:
          orders_dict[order_id] = {"OrderID": order_id,
                                  "ReferenceNumber": order[1],
                                  "CountryCode": order[2],
                                  "FullName":order[3],
                                  "AddresType":order[4],
                                  "AddressLine1":order[5],
                                  "AddressLine2":order[6],                                  
                                  "CustomerCode":order[7],
                                  "FirstName": order[8],
                                  "LastName": order[9],
                                  "Phone": order[10],
                                  "Email": order[11],                                   
                                  
                                  "OrderLines": []
                                  }
      order_line = {"OrderLineID": order[12],
                    "ItemNum": order[13],
                    "ItemDescription": order[14]}
      orders_dict[order_id]["OrderLines"].append(order_line)

  # convert the dictionary values to a list
  orders_list = list(orders_dict.values())


  select_all_items_in_order_line="SELECT * FROM OrderLineTable"
  mycursor.execute(select_all_items_in_order_line)
  all_order_lines=mycursor.fetchall()

  new_order_line_list = []
  for order_line in all_order_lines:
    item_dict = {'ItemNum': order_line[1], 'ItemDescription': order_line[2]}
    new_order_line_list.append(item_dict)
      
  # return orders and items_list as a dictionary
  return {"Orders": orders_list, "Items": new_order_line_list}

@app.post("/order_update/")
async def get_updated_data(request: Request):
    order_data = await request.json()
    print("Nothing",order_data)
    mycursor = mydb.cursor()

    # Update OrderTable with order data
    update_order_query = """UPDATE OrderTable SET CountryCode = %s, FullName = %s, AddresType = %s, AddressLine1 = %s, AddressLine2 = %s WHERE OrderID = %s"""
    order_values = (order_data['CountryCode'], order_data['FullName'], order_data['AddresType'], order_data['AddressLine1'], order_data['AddressLine2'], order_data['OrderID'])
    mycursor.execute(update_order_query, order_values)

    # Delete existing order lines associated with this order
    delete_order_to_order_lines_query = """DELETE FROM orderToOrderLines WHERE OrderID = %s"""
    delete_order_to_order_lines_values = (order_data['OrderID'],)
    mycursor.execute(delete_order_to_order_lines_query, delete_order_to_order_lines_values)

    delete_order_lines_query = """DELETE FROM OrderLineTable WHERE OrderLineID IN (SELECT ItemNum FROM orderToOrderLines WHERE OrderID = %s)"""
    delete_order_lines_values = (order_data['OrderID'],)
    mycursor.execute(delete_order_lines_query, delete_order_lines_values)

    # Insert new order lines associated with this order
    for order_line in order_data['OrderLines']:
        insert_order_line_query = """INSERT IGNORE INTO OrderLineTable (OrderLineID, ItemNum, ItemDescription) VALUES (%s, %s, %s)"""
        insert_order_line_values = (order_line['OrderLineID'], order_line['ItemNum'], order_line['ItemDescription'])
        mycursor.execute(insert_order_line_query, insert_order_line_values)

        insert_order_to_order_lines_query = """INSERT IGNORE INTO orderToOrderLines (OrderID, ItemNum) VALUES (%s, %s)"""
        insert_order_to_order_lines_values = (order_data['OrderID'], order_line['ItemNum'])
        mycursor.execute(insert_order_to_order_lines_query, insert_order_to_order_lines_values)

    # Commit changes to database
    mydb.commit()
    orders_list = await get_data()
    return orders_list 


