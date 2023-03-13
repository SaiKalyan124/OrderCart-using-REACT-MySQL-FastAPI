import React, { useState } from 'react';
import Modal from 'react-modal';
import "./../StylingFiles/order_page.css"
import EditForm from './editForm';

Modal.setAppElement('#root');
function OrderCard(props) {
    const { order ,items} = props;
    const [showModal, setShowModal] = useState(false);

    // Handle Edit button click
    const handleEdit = () => {
      setShowModal(true);
    }
    // Handle Modal close
    function handleCloseModal() {
        setShowModal(false);
    }
    console.log("ALL the ITEMS",items)

    // console.log("Line ID",order.OrderLineID)
    function handleSubmit(event,orderLines) {
      event.preventDefault();
      const formData=new FormData(event.target);
      const updatedOrderLines = orderLines.map((item, index) => ({
        OrderLineID:item.OrderLineID,
        ItemNum: item.ItemNum,
        ItemDescription: formData.get(`itemDescription${index}`),
        // Get other updated item properties here
      }));
      const updatedOrderData = {
        OrderID:order.OrderID,
         
        FullName: formData.get('fullName'),
        AddresType: formData.get('addressType'),
        AddressLine1: formData.get('addressLine1'),
        AddressLine2: formData.get('addressLine2'),
        CountryCode: formData.get('countryCode'),
        OrderLines: updatedOrderLines, 
      };
      


      // Send the updated order data to the server
      fetch('http://localhost:8000/order_update/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedOrderData)
          })
            .then(response => {
              if (!response.ok) {
                throw new Error('Failed to save order data');
              }
              return response.json();
            })
            .then(data => {
              console.log('Order data saved successfully', updatedOrderData);
              // Close the modal
              setShowModal(false);
            })
            .catch(error => {
              console.error('Error saving order data', error);
            });
            window.location.reload();
    }
  
    return (
      <div className="card mb-3">
        <div className="card-header">
          
          <div class="right-column">
            <h3>Ship To:</h3>
            <h3 class="card-text">{order.FirstName} {order.LastName}</h3>
            <h3>{order.Phone}</h3>
              <h3>{order.Email}</h3>
            <div class="popup-card">
              <h4>Address:</h4>
              
              <p>{order.FullName}, {order.AddresType}</p>
              <p>{order.AddressLine1}, {order.AddressLine2} -- {order.CountryCode}</p>
              
            </div>
          </div>
          <div className="left-column">
            <h3>Order #{order.OrderID}</h3>
            <h3>Ref # {order.ReferenceNumber}</h3>
          </div>
        </div>
        <div className="card-body">
          <h6 className="card-subtitle mb-2 text-muted"></h6>
          <div className="list-group">
            {order.OrderLines.map((line) => (
              <p key={line.OrderLineID} className="list-group-item">
                {line.ItemDescription}
                <></>
              </p>
            ))}
          </div>
          
            <button className="button-88" onClick={handleEdit}>Edit</button>
  
            {/* Modal form */}
            <div >
            <Modal  className='Modal' isOpen={showModal} onRequestClose={handleCloseModal}>
                <EditForm order={order} onCancel={handleCloseModal} onSubmit={ handleSubmit} items={items}/>
            </Modal></div>
        </div>
      </div>
    );
  }
         

function OrderList(props) {
  const { orders,items } = props;

  return (
    <div className="order-container">
      {orders.map((order) => (
        <div key={order.OrderID}>
          <OrderCard order={order} items={items} />
        </div>
      ))}
    </div>
  );
}

export default OrderList;


