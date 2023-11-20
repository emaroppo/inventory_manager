import React from 'react';

function Pagination({ currentPage, setCurrentPage, hasNextPage }) {
    return (
        <div style={{ marginTop: '20px' }}>
            {currentPage > 1 &&
                <button onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}>Previous</button>
            }

            {hasNextPage &&
                <span> Page {currentPage} <button onClick={() => setCurrentPage(prev => prev + 1)}>Next</button></span>
            }
        </div>
    );
}

export default Pagination;
