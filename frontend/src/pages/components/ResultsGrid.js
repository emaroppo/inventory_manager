import React from 'react';
import GridResult from "./GridResult";

function ResultsGrid({ results, currentPage }) {
    return (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px' }}>
            {
                results
                    .slice((currentPage - 1) * 16, currentPage * 16)
                    .map(result => (<GridResult key={result.result_id} result={result} />))
            }
        </div>
    );
}

export default ResultsGrid;
