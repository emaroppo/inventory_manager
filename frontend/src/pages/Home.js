import React from 'react';
import { Link } from 'react-router-dom';
import styles from './css/Home.module.css';

const Home = () => {
  return (
    <div className={styles.homeContainer}>
      <h1>Welcome to Our Supermarket!</h1>
      <div className={styles.buttonsContainer}>
        <Link to="/shop" className={styles.button}>
          Shop Now
        </Link>
        <Link to="/store-locator" className={styles.button}>
          Find a Store
        </Link>
      </div>
    </div>
  );
};

export default Home;
