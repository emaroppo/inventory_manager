function Shop(username, user_id, categories, products) {
    <>
        <div className="Shop">
            <h1>Shop</h1>
            <span>Hello, {username}</span>
            <a href="{user-id}/cart"><img alt="Cart Icon"></img></a>
        </div>
        <div className="Categories">
            <h2>Categories</h2>
            <ul>
                {categories.map((category) => (
                    <li>
                        <a href="{category}">{category}</a>
                    </li>
                ))}
            </ul>
        </div>
        <div className="Products">
            <h2>Products</h2>
            <ul>
                {products.map((product) => (
                    <li>
                        <a href="{product}">{product}</a>
                    </li>
                ))}
            </ul>
            <span>Page 1</span>
        </div>
    </>
}
export default Shop;