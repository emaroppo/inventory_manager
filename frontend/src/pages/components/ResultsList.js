import React from 'react';
import ListResult from "./ListResult";

function ResultsList({ results, currentPage }) {
    console.log(results);

    return (
        <div>
            {
                results
                    .slice((currentPage - 1) * 16, currentPage * 16)
                    .map(result => (<ListResult key={result.result_id} result={result} />))
            }
        </div>
    );
}
export default ResultsList;
