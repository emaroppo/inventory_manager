import React, { useState, useEffect } from 'react';
import { useQuery } from 'react-query';
import ResultsList from '../components/common/ResultsList';
import RemoveFromCart from '../components/shop/RemoveFromCart';
import CheckoutButton from '../components/shop/CheckoutButton';
import { fetchCartItems } from '../utils/fetchCartItems'; // Adjust the path as needed

const API_ADDRESS = process.env.REACT_APP_API_ADDRESS;

function Cart() {
    const { data: cartItems, refetch } = useQuery('cartItems', () => fetchCartItems(API_ADDRESS));
    const [resultsList, setResultsList] = useState(null); // Initialized state for the results list

    useEffect(() => {
        if (cartItems?.items) {
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
                        onItemRemoved: refetch
                    })}
                />
            );
        }
    }, [cartItems]);

    const handleCheckoutSuccess = () => {
        console.log('Checkout successful. Refreshing cart...');
        refetch();
    };

    return (
        <>
            {resultsList}
            <CheckoutButton onCheckoutSuccess={handleCheckoutSuccess} />
        </>
    );
}

export default Cart;
