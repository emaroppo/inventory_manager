import React from 'react';
import ListResult from "./ListResult";

function ResultsList({ results, currentPage, ActionButtonComponent, actionButtonProps }) {
    console.log(results);

    return (
        <div>
            {results.slice((currentPage - 1) * 16, currentPage * 16).map(result => (
                <div key={result.result_id} style={{ display: 'flex', alignItems: 'center' }}>
                    <ListResult result={result} />
                    <ActionButtonComponent {...actionButtonProps(result)} />
                </div>
            ))}
        </div>
    );
}

export default ResultsList;
