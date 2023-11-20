const API_ADDRESS = process.env.REACT_APP_API_ADDRESS;


function RemoveFromCart({ productId, onItemRemoved }) {
    const removeFromCart = async () => {
        try {
            const response = await fetch(`${API_ADDRESS}/cart/remove_item`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    product_id: productId,
                    qty: 'all',
                }),
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Item removed from cart:', data);
                onItemRemoved(); // Call the callback function
            } else {
                console.error('Failed to remove item from cart');
            }
        } catch (error) {
            console.error('Error removing item from cart:', error);
        }
    };

    return (
        <button onClick={removeFromCart}>
            Remove from Cart
        </button>
    );
}


export default RemoveFromCart;