
# Project Name
This project is a simple web application that allows users to manage orders and customers using a MySQL database. The application is built using FastAPI on the backend and React on the frontend.
## Screenshots

Data retrived from XML :
![Screenshot (13)](https://user-images.githubusercontent.com/104048277/224835780-120dac72-c052-4be5-9560-fbfd9278c6d5.png)

User can amend/update  orders :
![image](https://user-images.githubusercontent.com/104048277/225148293-91f382d7-dbf6-48b8-a82a-4d286b768edd.png)
![image](https://user-images.githubusercontent.com/104048277/225148334-b0d2a4c8-e17e-4327-b8e4-6013223ed8f4.png)

 DB design :
 
![image](https://user-images.githubusercontent.com/104048277/225148363-5c088589-6bb6-4383-abfa-2bbd2803a808.png)


### Installation
- Install Node.js, Python 
- To run this project, you will need to install its dependencies.
```
pip install -r requirements.txt
```
- Command will install all the required packages listed in the `requirements.txt` file.

- Clone the repository to your local machine.
- Install the necessary dependencies.
- Set up a MySQL database and configure the connection details in mysql_config.py.
- Run the backend using :
```uvicorn main:app --reload```
- Run the frontend using :
``` npm start ```
### Usage
Once the application is running, you can access it in your browser by navigating to http://localhost:3000. The home page displays a list of orders. You can also add a new order or edit an existing one by clicking the corresponding buttons.

### API Endpoints
The following API endpoints are available:

- GET /get_order_data: Returns a list of all orders in the database.
- PUT /order_update/: Updates an existing order with the specified ID.

### Youtube Link
https://youtu.be/jFfzTLQBv9w
