import React, { useState, useEffect } from 'react';
import { useQuery } from 'react-query';
import CategoryList from '../components/shop/CategoryList';
import ResultsGrid from '../components/common/ResultsGrid';
import Pagination from '../components/common/Pagination';
import { fetchCategoryData } from '../utils/fetchCategoryItems'; // Adjust the path as needed
import styles from '../css/Shop.module.css'; 
import { useParams } from 'react-router-dom';

const API_ADDRESS = process.env.REACT_APP_API_ADDRESS;

function Shop() {
    const [products, setProducts] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const { category_name } = useParams();
    const { data: categories } = useQuery('categories', fetchCategoryData);

    useEffect(() => {
        async function fetchProducts() {
            const productsData = await (await fetch(`${API_ADDRESS}/products`)).json();
            setProducts(productsData);
            setCurrentPage(1);
        }
        fetchProducts();
    }, [category_name]);

    let filteredProducts = [];

    if (category_name) {
        // Filter products based on the selected category
        const category = categories?.find(cat => cat.category_name === category_name);
        const categoryId = category ? category.category_id : null;
        filteredProducts = products.filter(product => product.category_id === categoryId);
    } else {
        // If no category is selected, display all products
        filteredProducts = products;
    }

    const hasNextPage = filteredProducts.length > currentPage * 16;
    filteredProducts = filteredProducts.map(product => ({ 'result_id': product.product_id, 'result_image': product.product_image, 'result_name': product.product_name, 'result_price': product.product_price }))


    return (
        <div className={styles.shopContainer}>
            <div className={styles.CategoryList}>
                <CategoryList />
            </div>
            <div className={styles.resultsSection}>
                <ResultsGrid key={0} results={filteredProducts} currentPage={currentPage} />
                <Pagination key={1} currentPage={currentPage} setCurrentPage={setCurrentPage} hasNextPage={hasNextPage} />
            </div>
        </div>
    );
}

export default Shop;