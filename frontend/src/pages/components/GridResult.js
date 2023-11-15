import React from 'react';
import AddToCart from './AddToCart'; // Adjust the path based on your file structure
import styles from './css/GridResult.module.css'; // Import CSS module

function GridResult({ result }) {
    return (
        <div className={styles.gridResultCard}>
            <img 
                src={process.env.PUBLIC_URL + '/' + result.result_image} 
                alt={result.result_name} 
                className={styles.productImage} 
            />
            <div className={styles.productName}>{result.result_name}</div>
            <div className={styles.productPrice}>Price: {result.result_price}$</div>
            <AddToCart product={result} />
        </div>
    );
}

export default GridResult;
