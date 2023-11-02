import React from 'react';
import AddToCart from './AddToCart';  // Adjust the path based on your file structure.

function GridResult(result) {
    result = result.result;

    return (
        <div key={result.result_id} style={{ border: '1px solid #ccc', padding: '10px' }}>
            <img src={process.env.PUBLIC_URL + '/' + result.result_image} alt={result.result_name} style={{ width: '75%' }} /> <br />
            {result.result_name} <br />
            Price: {result.result_price}$ <br />

            <AddToCart product={result} />
        </div>
    );
}

export default GridResult;
