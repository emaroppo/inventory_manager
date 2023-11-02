import React, { useState, useEffect } from 'react';
import ResultsList from './components/ResultsList';

const API_ADDRESS = process.env.API_ADDRESS;

function StoreLocator() {
    const [zipQuery, setZipQuery] = useState('');
    const [stores, setStores] = useState([]);

    function handleChange(event) {
        setZipQuery(event.target.value);
    }

    useEffect(() => {
        async function fetchStores() {
            if (zipQuery.length > 3) {
                const response = await fetch(`${API_ADDRESS}/stores/find?zip_query=` + zipQuery);
                const data = await response.json();

                // Transform the data to match the format expected by ResultsList and ListResult
                const transformedData = data.map(store => ({
                    result_id: store.store_id,
                    result_name: store.street_name,
                    result_image: "path_to_default_store_image.jpg", // Default image or use a relevant one
                    result_price: `${store.street_n}, ${store.city} - ${store.ZIP}`
                }));

                setStores(transformedData);
            } else {
                setStores([]); // Clear stores if zipQuery length is less than or equal to 3
            }
        }

        fetchStores();
    }, [zipQuery]);

    return (
        <div>
            <h1>Store Locator</h1>
            <div>
                <input
                    type="text"
                    value={zipQuery}
                    onChange={handleChange}
                    placeholder="Enter zip code"

                />
                <ResultsList results={stores} currentPage={1} />
            </div>
        </div>
    );
}

export default StoreLocator;
