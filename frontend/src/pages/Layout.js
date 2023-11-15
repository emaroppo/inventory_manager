import React from 'react';
import styles from './css/Layout.module.css';
import { Outlet, Link } from 'react-router-dom';

const Layout = ({ children }) => {
  return (
    <div className={styles.layoutContainer}>
      <nav className={styles.navBar}>
        <div className={styles.logo}><Link to="/" className={styles.menuItem}>
            <i className="fas fa-home"></i> SuperStore
            </Link></div>
        <div className={styles.menuItems}>
          
            <Link to="/shop" className={styles.menuItem}>

            <i className="fas fa-shopping-cart"></i> Shop
            </Link>
            <Link to="/locate/store" className={styles.menuItem}>
            <i className="fas fa-map-marker-alt"></i> Find a Store
            </Link>
            <Link to="/cart" className={styles.menuItem}>
            <i className="fas fa-shopping-cart"></i> Cart
            </Link>
            <Link to="/orders" className={styles.menuItem}>
            <i className="fas fa-shopping-cart"></i> Orders
            </Link>
            <Link to="/admin" className={styles.menuItem}>
            <i className="fas fa-user"></i> Admin
            </Link>
            
        </div>
      </nav>
      <div className={styles.content}>
        <Outlet />
      </div>
    </div>
  );
};

export default Layout;
