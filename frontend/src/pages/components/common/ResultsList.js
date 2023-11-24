// ResultsList component
import React from 'react';
import ListResult from './ListResult'; 
import styles from '../css/ResultsList.module.css'; 
import StoreDetailsButton from './StoreDetailsButton'; // Import the new button component


function ResultsList({ results }) {
  return (
    <div className={styles.resultsListContainer}>
      {results.map(result => (
        <ListResult 
          key={result.result_id} 
          result={result}
          ActionButtonComponent={StoreDetailsButton}
          actionButtonProps={{ storeId: result.result_id }}
        />
      ))}
    </div>
  );
}

export default ResultsList;
