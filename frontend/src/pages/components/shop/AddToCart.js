import React, { useState } from 'react';

const API_ADDRESS = process.env.REACT_APP_API_ADDRESS;
function AddToCart({ product }) {
    const [quantity, setQuantity] = useState(1);
    const [unitsInCart, setUnitsInCart] = useState(0);

    const handleAddToCart = async () => {
        try {
            const response = await fetch(`${API_ADDRESS}/cart/add_item`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    product_id: product.result_id,
                    qty: quantity
                })
            });

            const updatedCart = await response.json();
            const productInCart = updatedCart.items.find(item => item.product_id === product.result_id);
            setUnitsInCart(productInCart ? productInCart.qty : 0);
        } catch (error) {
            console.error('Failed to add product to cart:', error);
        }
    };

    return (
        <div>
            <input
                type="number"
                value={quantity}
                onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value)))}
                style={{ width: '50px' }}
            />
            <button onClick={handleAddToCart}>Add to cart</button>

            {unitsInCart > 0 && <p>You already have {unitsInCart} units of this product in your cart.</p>}
        </div>
    );
}

export default AddToCart;
