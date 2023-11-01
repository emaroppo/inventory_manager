import React, { useState, useEffect } from 'react';
import CategoryList from './components/CategoryList';
import ProductGrid from './components/ProductGrid';
import Pagination from './components/Pagination';

import { useParams } from 'react-router-dom';

function Shop() {
    const [categories, setCategories] = useState([]);
    const [products, setProducts] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const { category_name } = useParams();

    useEffect(() => {
        async function fetchData() {
            const categoriesData = await (await fetch('http://localhost:8000/categories')).json();
            const productsData = await (await fetch('http://localhost:8000/products')).json();
            setCategories(categoriesData);
            setProducts(productsData);
            setCurrentPage(1);
        }
        fetchData();
    }, [category_name]);

    let filteredProducts = [];
    let hasNextPage;
    if (typeof category_name === 'undefined' || category_name === null) {
        filteredProducts = products;
        hasNextPage = filteredProducts.length > currentPage * 16;
    } else {
        const category = categories.find(cat => cat[1] === category_name);
        const categoryId = category ? category[0] : null;
        filteredProducts = products.filter(product => product.category_id === categoryId);
        hasNextPage = filteredProducts.length > currentPage * 16;
    }
    return (
        <div style={{ display: 'flex' }}>
            <div style={{ flex: 1, marginRight: '20px' }}>
                <CategoryList categories={categories} />
            </div>
            <div style={{ flex: 3 }}>
                <ProductGrid key={0} products={filteredProducts} currentPage={currentPage} />
                <Pagination key={1} currentPage={currentPage} setCurrentPage={setCurrentPage} hasNextPage={hasNextPage} />
            </div>
        </div>
    );
}

export default Shop;