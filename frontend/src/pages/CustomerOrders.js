import React, { useState, useEffect } from 'react';
import ResultsList from './components/ResultsList';
import ShowOrderDetails from './components/ShowOrderDetails';
import styles from './css/CustomerOrders.module.css';

const API_ADDRESS = process.env.REACT_APP_API_ADDRESS;

function CustomerOrders() {
    const userId = 1;
    const [orders, setOrders] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);

    useEffect(() => {
        const fetchOrders = async () => {
            try {
                const response = await fetch(`${API_ADDRESS}/user/orders`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ user_id: userId }),
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                setOrders(data);
            } catch (error) {
                console.error('Error fetching orders:', error);
            }
        };

        fetchOrders();
    }, [userId]);

    const results = orders.map(order => ({
        result_id: order.order_id,
        result_image: order.order_image,
        leftLines: [order.order_id],
        rightLines: [order.status_id],
    }));

    return (
        <div className={styles.ordersContainer}>
            <ResultsList 
                results={results} 
                currentPage={currentPage} 
                ActionButtonComponent={ShowOrderDetails}
                actionButtonProps={(order) => ({
                    orderId: order.result_id
                })}
            />
        </div>
    );
}

export default CustomerOrders;
