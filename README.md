
# Project Name
This project is a simple web application that allows users to manage orders and customers using a MySQL database. The application is built using FastAPI on the backend and React on the frontend.
## Screenshots

Data retrived from XML :
![Screenshot (13)](https://user-images.githubusercontent.com/104048277/224835780-120dac72-c052-4be5-9560-fbfd9278c6d5.png)

User can amend/update  orders :
![image](https://user-images.githubusercontent.com/104048277/224835765-3e4ea4c5-f099-4aef-a4c1-018de5960298.png)
 DB design :
 
![image](https://user-images.githubusercontent.com/104048277/224835441-aa74d2a5-c9aa-4a77-ae9d-ff050f50d8a0.png)


### Installation
- Install Node.js, Python 
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
