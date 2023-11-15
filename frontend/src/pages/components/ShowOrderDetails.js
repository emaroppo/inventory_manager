import React from 'react';
import { useNavigate } from 'react-router-dom'; // Updated import

function ShowOrderDetails({ orderId }) {
    const navigate = useNavigate(); // Updated hook

    const handleClick = () => {
        navigate(`/order-details/${orderId}`); // Updated navigation method
    };

    return (
        <button onClick={handleClick}>Show Order Details</button>
    );
}

export default ShowOrderDetails;
