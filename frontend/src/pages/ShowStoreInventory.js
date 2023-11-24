import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Button, Paper, Typography } from '@mui/material';
import DataTable from 'mui-datatables';

const ShowStoreInventory = () => {
  const { store_id } = useParams();
  const [inventory, setInventory] = useState([]);

  useEffect(() => {
    const fetchInventory = async () => {
      try {
        const response = await fetch('/inventory/store', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ store_id }),
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setInventory(data);
      } catch (error) {
        console.error('Error fetching inventory:', error);
      }
    };

    fetchInventory();
  }, [store_id]);

  const columns = [
    { name: 'itemName', label: 'Item Name' },
    { name: 'quantity', label: 'Quantity' },
    // Add more columns as needed
  ];

  const options = {
    filterType: 'checkbox',
    responsive: 'standard',
  };

  return (
    <div>
      <Typography variant="h4">Store ID: {store_id}</Typography>
      <Button variant="contained" color="primary">Restock</Button>
      <Button variant="contained" color="secondary">Assign Order</Button>
      <Paper>
        <DataTable
          title="Store Inventory"
          data={inventory}
          columns={columns}
          options={options}
        />
      </Paper>
    </div>
  );
};

export default ShowStoreInventory;
