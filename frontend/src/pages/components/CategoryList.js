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
                    key={category[0]}
                    to={`/shop/${category[1]}`}
                    style={{
                        display: 'block',
                        marginBottom: '10px',
                        fontWeight: category[1] === category_name ? 'bold' : 'normal'
                    }}
                    onClick={() => navigate(`/shop/${category[1]}`)}
                >
                    {category[1]}
                </Link>
            ))}
        </div>
    );
}

export default CategoryList;