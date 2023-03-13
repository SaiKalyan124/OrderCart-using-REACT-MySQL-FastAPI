import React, { useState } from 'react';
import Modal from 'react-modal';
import "./../Styling Files/order_page.css"
import EditForm from './editForm';

Modal.setAppElement('#root');
function OrderCard(props) {
    const { order } = props;
    const [showModal, setShowModal] = useState(false);

    // Handle Edit button click
    const handleEdit = () => {
      setShowModal(true);
    }
    // Handle Modal close
    function handleCloseModal() {
        setShowModal(false);
    }


    // console.log("Line ID",order.OrderLineID)
    function handleSubmit(event) {
      event.preventDefault();
      const formData=new FormData(event.target);
      const updatedOrderLines = orderLines.map((item, index) => ({
        ItemDescription: formData.get(`itemDescription${index}`),
        // Get other updated item properties here
      }));
      const updatedOrderData = {
        OrderID:order.OrderID,
        CountryCode: formData.get('countryCode'), // Updated value
        FullName: formData.get('fullName'),
        AddresType: formData.get('addressType'),
        AddressLine1: formData.get('addressLine1'),
        AddressLine2: formData.get('addressLine2'),
        OrderLines: updatedOrderLines
      };
      console.log("from displayORder",updatedOrderData)
      

      

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
    }
  
    return (
      <div className="card mb-3">
        <div className="card-header">
          <div className="left-column">
            <h3>Order #{order.OrderID}</h3>
            <h3>Ref # {order.ReferenceNumber}</h3>
          </div>
          <div className="right-column">
              <h3>Ship To:</h3>
            <h3 className="card-text" title={`
                Ship To:
                ${order.CountryCode}
                ${order.FullName}, ${order.AddresType}
                ${order.AddressLine1}, ${order.AddressLine2}`}>
              {order.FirstName} {order.LastName} 
            </h3>
            <h3 className="card-text">{order.Phone}</h3>
            <h3 className="card-text">{order.Email}</h3>
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
                <EditForm order={order} onCancel={handleCloseModal} onSubmit={ handleSubmit}/>
            </Modal></div>
        </div>
      </div>
    );
  }
         

function OrderList(props) {
  const { orders } = props;

  return (
    <div className="order-container">
      {orders.map((order) => (
        <div key={order.OrderID}>
          <OrderCard order={order} />
        </div>
      ))}
    </div>
  );
}

export default OrderList;


import React, { useState } from 'react';
import "./../Styling Files/editForm.css"

function EditForm(props) {
  const { order } = props;
  const [orderLines, setOrderLines] = useState(order.OrderLines);

  const handleItemChange = (index, item) => {
    const newOrderLines = [...orderLines];
    newOrderLines[index] = item;
    setOrderLines(newOrderLines);
  };

































      {orderLines.map((item, index) => (
        <div key={index}>
          <label>
            Item Description:
            <input type="text" name="itemDescription" value={item.ItemDescription} onChange={(e) => 
              handleItemChange(index, { ItemDescription: e.target.value })} />
          </label>
          <button type="button" onClick={() => handleDeleteItem(index)}>Delete</button>
        </div>
      ))}























      import React, { useState } from 'react';
import "./../Styling Files/editForm.css"

function EditForm(props) {
  const { order ,items} = props;
  const [orderLines, setOrderLines] = useState(order.OrderLines);

  const handleItemChange = (index, item) => {
    const newOrderLines = [...orderLines];
    newOrderLines[index] = item;
    setOrderLines(newOrderLines);
  };

  const handleAddItem = () => {
    const newOrderLines = [...orderLines, { ItemDescription: '' }];
    setOrderLines(newOrderLines);
  };

  const handleDeleteItem = (index) => {
    const newOrderLines = [...orderLines];
    newOrderLines.splice(index, 1);
    setOrderLines(newOrderLines);
  };
    console.log("orderlines",orderLines)
    console.log("In EditForm",items)
    

  return (
    <form className='edit-form' onSubmit={(event) => props.onSubmit(event, orderLines)}>
      <h3>Order #:{order.OrderID}</h3>

      <br />
      <label>
        Country Code:<br />
        <input type="text" name="countryCode" placeholder={order.CountryCode} defaultValue={order.CountryCode} />
      </label><br />
      <label>
        FullName:<br />
        <input type="text" name="fullName" placeholder={order.FullName} defaultValue={order.FullName} />
      </label><br />
      <label>
        AddressType:<br />
        <input type="text" name="addressType" placeholder={order.AddresType} defaultValue={order.AddresType} />
      </label><br />
      <label>
        AddressLine1:<br />
        <input type="text" name="addressLine1" placeholder={order.AddressLine1} defaultValue={order.AddressLine1} />
      </label><br />
      <label>
        AddressLine2:<br />
        <input type="text" name="addressLine2" placeholder={order.AddressLine2} defaultValue={order.AddressLine2} />
      </label>
      


      <h4>Order Lines:</h4>
          {orderLines.map((item, index) => (
          <div key={index}>
          <label>
          Item Description: 
          <br/>{item.ItemNum}
          <br/>
          <input type="text" name={`itemDescription${index}`} value={item.ItemDescription} 
                onChange={(e) =>
          handleItemChange(index, { ItemDescription: e.target.value })} />
          </label>
          <button type="button" onClick={() => handleDeleteItem(index)}>Delete</button>
          </div>
          ))}
      <select multiple>
        {items.map((item, index) => (
          <option key={index} value={item.ItemNum} selected={orderLines.some((line) => line.ItemNum === item.ItemNum)}>
            {item.ItemDescription}
          </option>
        ))}
      </select>






      
      <button type="button" onClick={handleAddItem}>Add Item</button>
      <br />
      <button type="submit">Save</button>
      <button onClick={props.onCancel}>Cancel</button>
    </form>
  );
}

export default EditForm;