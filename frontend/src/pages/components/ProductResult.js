function ProductResult(product) {
    product = product.product;
    return (
        <div key={product.product_id} style={{ border: '1px solid #ccc', padding: '10px' }}>
            <img src={process.env.PUBLIC_URL + '/placeholder.jpg'} alt={product.product_name} style={{ width: '75%' }} /> <br />
            {product.product_name} <br />
            Price: 0.00$ <br />
            Add to cart

        </div>
    );
}

export default ProductResult;