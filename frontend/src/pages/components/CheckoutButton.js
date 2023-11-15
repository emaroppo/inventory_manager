import React from 'react';

const API_ADDRESS = process.env.REACT_APP_API_ADDRESS;

function CheckoutButton({ onCheckout }) {
    const handleCheckout = async () => {
        const response = await fetch(`${API_ADDRESS}/cart/checkout`, {
            method: 'POST',
        });
        const data = await response.json();
        onCheckout(data);
    };

    return (
        <button onClick={handleCheckout}>
            Checkout
        </button>
    );
}

export default CheckoutButton;