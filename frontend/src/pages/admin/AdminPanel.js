import OuterComponent from "./AddEntries";

function AdminPanel() {

    const schema = {
        'categories': {
            'fields': ['category_name'],
            'url': 'http://192.168.2.169:8000/categories/add_category'
        },
        'products': {
            'fields': ['product_name',
                'product_price',
                'product_image',
                'category_id'],
            'url': 'http://192.168.2.169:8000/products/add_product'
        },
        'stores': {
            'fields': ['street_n',
                'street_name',
                'city',
                'ZIP',
                'store_image'],
            'url': 'http://192.168.2.169:8000/stores/add_store'
        }
    }


    return (
        <div>
            <h1>Admin Panel</h1>
            {schema && <OuterComponent schema={schema} />}
        </div >
    );
}

export default AdminPanel;