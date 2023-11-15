import React from 'react';
import GridResult from './GridResult';
import styles from './css/ResultsGrid.module.css';

function ResultsGrid({ results }) {
    return (
        <div className={styles.resultsGridContainer}>
            {results.map(result => (
                <GridResult key={result.result_id} result={result} />
            ))}
        </div>
    );
}

export default ResultsGrid;
