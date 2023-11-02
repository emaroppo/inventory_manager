import React from 'react';
import ListResult from "./ListResult";
import RemoveFromCart from "./RemoveFromCart";

function ResultsList({ results, currentPage, onItemRemoved }) {
    console.log(results);

    return (
        <div>
            {
                results
                    .slice((currentPage - 1) * 16, currentPage * 16)
                    .map(result => (
                        <div key={result.result_id} style={{ display: 'flex', alignItems: 'center' }}>
                            <ListResult result={result} />
                            <RemoveFromCart
                                productId={result.result_id}
                                onItemRemoved={onItemRemoved} // Pass the callback function down
                            />
                        </div>
                    ))
            }
        </div>
    );
}
export default ResultsList;
