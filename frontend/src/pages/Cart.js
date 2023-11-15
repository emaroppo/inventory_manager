import React, { useState, useEffect } from 'react';
import ResultsList from './components/ResultsList';
import CheckoutButton from './components/CheckoutButton';

const API_ADDRESS = process.env.REACT_APP_API_ADDRESS;

function Cart() {
    const [cartItems, setCartItems] = useState([]);
    const [resultsList, setResultsList] = useState([]);

    // This function will fetch the updated cart data
    const fetchCartData = async () => {
        const response = await fetch(`${API_ADDRESS}/cart`);
        const data = await response.json();
        setCartItems(data);  // schedules an update to cartItems
    };

    useEffect(() => {
        fetchCartData();
    }, []);

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

            const newResultsList = (
                <ResultsList
                    key={1000}
                    results={results}
                    currentPage={1}
                    onItemRemoved={fetchCartData} // Pass the fetch function as a prop
                />
            );
            setResultsList(newResultsList);
        }
    }, [cartItems]);
    const handleCheckout = (order) => {
        console.log(order); // log the order data
        // Here you can handle the order data, for example, by showing a success message
    };

    return (<>
        {resultsList}
        <CheckoutButton onCheckout={handleCheckout} />
    </>);
}

export default Cart;

