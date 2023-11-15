import React from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import styles from './css/CategoryList.module.css';

function CategoryList({ categories }) {
    const navigate = useNavigate();
    const { category_name } = useParams();

    return (
        <div className={styles.categoryListContainer}>
            <h2 className={styles.categoryListTitle}>Categories</h2>
            <Link 
                to="/shop" 
                className={category_name ? styles.categoryItem : styles.categoryItemActive}
                onClick={() => navigate('/shop')}
            >
                All products
            </Link>
            {categories.map(category => (
                <Link
                    key={category.category_id}
                    to={`/shop/${category.category_name}`}
                    className={category.category_name === category_name ? styles.categoryItemActive : styles.categoryItem}
                    onClick={() => navigate(`/shop/${category.category_name}`)}
                >
                    {category.category_name}
                </Link>
            ))}
        </div>
    );
}

export default CategoryList;
