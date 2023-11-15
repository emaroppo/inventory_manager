import React, { useState, useEffect } from 'react';
import CategoryList from './components/CategoryList';
import ResultsGrid from './components/ResultsGrid';
import Pagination from './components/Pagination';
import styles from './css/Shop.module.css'; 
import { useParams } from 'react-router-dom';

const API_ADDRESS = process.env.REACT_APP_API_ADDRESS;
console.log(API_ADDRESS);

function Shop() {
    const [categories, setCategories] = useState([]);
    const [products, setProducts] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const { category_name } = useParams();

    useEffect(() => {
        async function fetchData() {
            const categoriesData = await (await fetch(`${API_ADDRESS}/categories`)).json();
            const productsData = await (await fetch(`${API_ADDRESS}/products`)).json();
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
        const category = categories.find(cat => cat.category_name === category_name);
        const categoryId = category ? category.category_id : null;
        filteredProducts = products.filter(product => product.category_id === categoryId);
        hasNextPage = filteredProducts.length > currentPage * 16;

        console.log(filteredProducts);
    }

    filteredProducts = filteredProducts.map(product => ({ 'result_id': product.product_id, 'result_image': product.product_image, 'result_name': product.product_name, 'result_price': product.product_price }))


    return (
        <div className={styles.shopContainer}>
            <div className={styles.categoryList}>
                <CategoryList categories={categories} />
            </div>
            <div className={styles.resultsSection}>
                <ResultsGrid key={0} results={filteredProducts} currentPage={currentPage} />
                <Pagination key={1} currentPage={currentPage} setCurrentPage={setCurrentPage} hasNextPage={hasNextPage} />
            </div>
        </div>
    );
}

export default Shop;