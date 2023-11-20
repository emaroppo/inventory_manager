const API_ADDRESS = process.env.REACT_APP_API_ADDRESS;

export const fetchCategoryData = async (category_name) => {
    try {
        const response = await fetch(`${API_ADDRESS}/categories/`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
        throw error;
    }
};
