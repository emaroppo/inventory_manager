import React from 'react';
import styles from '../css/ListResult.module.css'; // Import CSS module

function ListResult({ result, ActionButtonComponent, actionButtonProps }) {
    return (
        <div className={styles.listResultItem}>
            <div className={styles.productDetails}>
                <img src={result.result_image} alt={result.leftLines.join(', ')} className={styles.productImage} />
                <div className={styles.leftLinesContainer}>
                    {result.leftLines.map((line, index) => (
                        <div key={index} className={styles.productInfo}>{line}</div>
                    ))}
                </div>
                <div className={styles.rightLinesContainer}>
                    {result.rightLines.map((line, index) => (
                        <div key={index} className={styles.productPrice}>{line}</div>
                    ))}
                </div>
            </div>
            {ActionButtonComponent && <ActionButtonComponent {...actionButtonProps} />}
        </div>
    );
}

export default ListResult;