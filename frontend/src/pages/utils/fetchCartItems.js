const API_ADDRESS = process.env.REACT_APP_API_ADDRESS;

export const fetchCartItems = async (API_ADDRESS) => {
    const response = await fetch(`${API_ADDRESS}/cart`);
    return response.json();
};
