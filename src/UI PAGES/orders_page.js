import React, { useState, useEffect } from "react";
import "./../Styling Files/order_page.css"
import OrderList from "../Components/displayOrder";

function Home() {
  const [orders, setOrders] = useState([]);
  const [items, setItems] = useState({});

  useEffect(() => {
    fetch('http://localhost:8000/get_data/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
    })
      .then((response) => response.json())
      .then((data) => {
        setOrders(data.Orders);
        setItems(data.Items);
      })
      .catch((error) => {
        console.error('Error fetching order data:', error);
      });
  }, []);

  console.log('Orders:', items);
  // const orderArray=Object.values(orders)
  return (
    <div className="order-container">
      
      <OrderList orders={orders} items={items}/>
    </div>
  );
  
  
}

export default Home;
