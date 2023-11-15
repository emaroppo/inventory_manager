import React from 'react';
import { useNavigate } from 'react-router-dom';

function ShowOrderDetails({ orderId }) {
    const navigate = useNavigate(); 

    const handleClick = () => {
        navigate(`/order-details/${orderId}`); 
    };

    return (
        <button onClick={handleClick}>Show Order Details</button>
    );
}

export default ShowOrderDetails;
