import React, { useState, useEffect } from 'react';
import ResultsList from './components/ResultsList';
import PlaceholderButton from './components/PlaceholderButton'; // Assuming you have a placeholder button component
import { useParams } from 'react-router-dom';

const API_ADDRESS = process.env.REACT_APP_API_ADDRESS;

function CustomerOrderDetails() {
    const orderId = useParams().orderId;
    const [orderDetails, setOrderDetails] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const fetchOrderDetails = async () => {
            setLoading(true);
            try {
                const response = await fetch(`${API_ADDRESS}/user/orders/view_order`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ order_id: orderId }),
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setOrderDetails(data.items); // Assuming the response has an 'items' field
            } catch (error) {
                console.error('Error fetching order details:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchOrderDetails();
    }, [orderId]);

    const results = orderDetails.map(item => ({
        result_id: item.product_id,
        result_image: "placeholder-image-url", // Placeholder image URL
        leftLines: [`Item: ${item.product_name}`, `Quantity: ${item.qty}`],
        rightLines: [item.shipping_status], // Assuming each item has a shipping_status field
    }));

    if (loading) return <div>Loading...</div>;

    return (
        <div>
            <h1>Order Details</h1>
            <ResultsList 
                results={results} 
                currentPage={1}
                ActionButtonComponent={PlaceholderButton}
                actionButtonProps={() => ({})}
            />
        </div>
    );
}

export default CustomerOrderDetails;
