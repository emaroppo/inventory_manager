import React from 'react';
import ListResult from './ListResult'; 
import styles from './css/ResultsList.module.css'; 

function ResultsList({ results, ActionButtonComponent, actionButtonProps }) {
    console.log(results);
    return (
        <div className={styles.resultsListContainer}>
            {results.map(result => (
                <ListResult 
                    key={result.result_id} 
                    result={result} 
                    ActionButtonComponent={ActionButtonComponent}
                    actionButtonProps={actionButtonProps(result)}
                />
            ))}
        </div>
    );
}

export default ResultsList;
