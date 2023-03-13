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
    const uniqueItems = [...new Set(items.map(item => item.ItemNum))];
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
              <input 
                type="text" 
                name={`itemDescription${index}`} 
                value={item.ItemDescription} 
                onChange={(e) =>
                  handleItemChange(index, { ItemDescription: e.target.value })
                } 
              />
            </label>
            {/* <button type="button" onClick={() => handleDeleteItem(item)} className="delete-button">Delete</button> */}
            <button type="button" onClick={() => handleDeleteItem(index)} className="delete-button">Delete</button>

          </div>
        ))}
        <br/>
        <select 
          multiple 
          value={orderLines.map((item) => item.ItemNum)} 
          onChange={(e) => {
            const selectedOptions = Array.from(e.target.selectedOptions).map((option) => option.value);
            const newOrderLines = [...orderLines];
            for (const item of items) {
              if (selectedOptions.includes(item.ItemNum) && !newOrderLines.some((line) => line.ItemNum === item.ItemNum)) {
                // Generate a new order line ID by incrementing the highest ID in existing order lines by 1
                const newOrderLineID = newOrderLines.length > 0 ? Math.max(...newOrderLines.map((line) => line.OrderLineID)) + 1 : 1;
                newOrderLines.push({ ...item, OrderLineID: newOrderLineID });
              } else if (!selectedOptions.includes(item.ItemNum) && newOrderLines.some((line) => line.ItemNum === item.ItemNum)) {
                // Find the item in the existing order lines and remove it
                const itemToRemove = newOrderLines.find((line) => line.ItemNum === item.ItemNum);
                if (itemToRemove) {
                  newOrderLines.splice(newOrderLines.indexOf(itemToRemove), 1);
                }
              }
            }
            setOrderLines(newOrderLines);
          }}
        >
          <option value={null}>None</option>
{uniqueItems.map((itemNum) => {
  const item = items.find((i) => i.ItemNum === itemNum);
  return (
    <option 
      key={itemNum} 
      value={itemNum} 
      selected={orderLines.some((line) => line.ItemNum === itemNum)}
    >
      {item.ItemDescription}
    </option>
  );
})}
</select>
      <button type="button" onClick={handleAddItem} className='edit-button'>Add Item</button>
      <br />
      <button type="submit" className='button-88'>Save</button><br/>
      <button onClick={props.onCancel} className='cancel-button-88'>Cancel</button>
    </form>
  );
}

export default EditForm;