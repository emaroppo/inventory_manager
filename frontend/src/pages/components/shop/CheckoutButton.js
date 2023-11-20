import React from 'react';

const API_ADDRESS = process.env.REACT_APP_API_ADDRESS;

function CheckoutButton({ onCheckoutSuccess }) {
    const handleCheckout = async () => {
        try {
            const response = await fetch(`${API_ADDRESS}/cart/checkout`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                console.log('Checkout Successful');
                onCheckoutSuccess(); // Callback to inform the Cart component
            } else {
                console.error('Checkout Failed:', await response.json());
            }
        } catch (error) {
            console.error('Error during checkout:', error);
        }
    };

    return (
        <button onClick={handleCheckout}>
            Checkout
        </button>
    );
}

export default CheckoutButton;
