import React from 'react';
import { useQuery } from 'react-query';
import { useParams } from 'react-router-dom';
import { fetchCategoryData } from '../../utils/fetchCategoryItems'; // Adjust the path as needed
import NavigationList from '../common/NavigationList'; // Adjust the path as needed
import styles from '../css/CategoryList.module.css';

function CategoryList() {
    const { category_name } = useParams();
    const { data: categories, isLoading, error } = useQuery('categories', fetchCategoryData);

    const determineActive = (item) => {
        return item.category_name === category_name;
    };

    if (isLoading) return 'Loading...';
    if (error) return 'An error has occurred: ' + error.message;

    // Prepend 'All Products' to the categories
    const allProductsItem = {
        category_name: 'All Products', 
        path: '', // No additional path for the base page
        id: 'all-products' // Unique identifier for 'All Products'
    };
    const items = [allProductsItem, ...categories.map(category => ({
        ...category, 
        path: category.category_name, 
        id: category.category_id
    }))];

    return (
        <NavigationList
            items={items}
            determineActive={determineActive}
            renderLabel={(item) => item.category_name}
            basePath="/shop"
            containerClassName={styles.categoryListContainer}
            itemClassName={styles.categoryItem}
            activeItemClassName={styles.categoryItemActive}
        />
    );
}

export default CategoryList;
