import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

function StoreDetailsButton({ storeId }) {
  const navigate = useNavigate();
  const location = useLocation();

  const handleClick = () => {
    // Extract the base URL from the current location
    const baseUrl = location.pathname;
    // Navigate to the store details page, preserving the current path structure
    navigate(`${baseUrl}/details/${storeId}`);
  };

  return (
    <button className={'button'} onClick={handleClick}>
      Show Store Details
    </button>
  );
}

export default StoreDetailsButton;
