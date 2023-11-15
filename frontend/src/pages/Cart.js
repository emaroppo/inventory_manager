import React, { useState, useEffect } from 'react';
import ResultsList from './components/ResultsList';
import RemoveFromCart from './components/RemoveFromCart'; // Import RemoveFromCart
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
        console.log(data);
        setCartItems(data);
    };

    useEffect(() => {
        if (cartItems.hasOwnProperty('items')) {
            const results = cartItems.items.map(item => ({
                result_id: item.item.product_id,
                result_image: item.item.product_image,
                leftLines: [item.item.product_name],
                rightLines: [item.item.product_price, item.qty]
            }));
            

            setResultsList(
                <ResultsList 
                    key={1000} 
                    results={results} 
                    currentPage={1}
                    ActionButtonComponent={RemoveFromCart}
                    actionButtonProps={(result) => ({
                        productId: result.result_id,
                        onItemRemoved: fetchData
                    })}
                />
            );
        }
    }, [cartItems]);

    const handleCheckoutSuccess = () => {
        console.log('Checkout successful. Refreshing cart...');
        fetchData();
    };

    return (
        <>
            {resultsList}
            <CheckoutButton onCheckoutSuccess={handleCheckoutSuccess} />
        </>
    );
}

export default Cart;
