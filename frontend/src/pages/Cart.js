import React, { useState, useEffect } from 'react';
import ResultsList from './components/ResultsList';
import CheckoutButton from './components/CheckoutButton'; // Import CheckoutButton

const API_ADDRESS = process.env.REACT_APP_API_ADDRESS;

function Cart() {
    const [cartItems, setCartItems] = useState([]);
    const [resultsList, setResultsList] = useState([]);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        const response = await fetch(`${API_ADDRESS}/cart`);
        const data = await response.json();
        setCartItems(data);
    };

    useEffect(() => {
        if (cartItems.hasOwnProperty('items')) {
            const results = cartItems.items.map(cartItem => ({
                'result_id': cartItem.item.product_id,
                'result_image': cartItem.item.product_image,
                'result_name': cartItem.item.product_name,
                'result_price': cartItem.item.product_price,
                'result_qty': cartItem.qty,
            })).map(result => ({
                'result_id': result.result_id,
                'result_image': result.result_image,
                'leftLines': [result.result_name],
                'rightLines': [result.result_price, result.result_qty],
            }));

            const newResultsList = <ResultsList key={1000} results={results} currentPage={1} />;
            setResultsList(newResultsList);
        }
    }, [cartItems]);

    // Callback function to handle successful checkout
    const handleCheckoutSuccess = () => {
        console.log('Checkout successful. Refreshing cart...');
        fetchData(); // Fetch updated cart data
    };

    return (
        <>
            {resultsList}
            <CheckoutButton onCheckoutSuccess={handleCheckoutSuccess} />
        </>
    );
}

export default Cart;
