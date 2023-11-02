import { Link, useNavigate, useParams } from 'react-router-dom';

function CategoryList({ categories }) {
    const navigate = useNavigate();
    const { category_name } = useParams();

    return (
        <div>
            <h2>Categories</h2>
            <Link to="/shop" style={{ display: 'block', marginBottom: '10px', fontWeight: !category_name ? 'bold' : 'normal' }} onClick={() => navigate('/shop')}>
                All products
            </Link>
            {categories.map(category => (
                <Link
                    key={category.category_id}
                    to={`/shop/${category.category_name}`}
                    style={{
                        display: 'block',
                        marginBottom: '10px',
                        fontWeight: category.category_name === category_name ? 'bold' : 'normal'
                    }}
                    onClick={() => navigate(`/shop/${category.category_name}`)}
                >
                    {category.category_name}
                </Link>
            ))}
        </div>
    );
}

export default CategoryList;