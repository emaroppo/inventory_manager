import React from 'react';
import { Link } from "react-router-dom";
import ProductResult from "./ProductResult";

function ProductGrid({ products, categoryFilter, currentPage }) {
    return (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px' }}>
            {
                products
                    .filter(product => !categoryFilter || product.category_id === categoryFilter)
                    .slice((currentPage - 1) * 16, currentPage * 16)
                    .map(product => (<ProductResult key={product.product_id} product={product} />
                    ))
            }
        </div>
    );
}

export default ProductGrid;
