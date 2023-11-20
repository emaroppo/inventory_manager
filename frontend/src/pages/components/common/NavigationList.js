import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import PropTypes from 'prop-types';
import styles from '../css/NavigationList.module.css';

function NavigationList({ items, determineActive, renderLabel = item => item.name, basePath = "" }) {
    const [activeSubMenu, setActiveSubMenu] = useState(null);

    const toggleSubMenu = (id) => {
        setActiveSubMenu(activeSubMenu === id ? null : id);
    };

    return (
        <div className={styles.navigationContainer}>
            <h2 className={styles.navigationTitle}> {/* Title here */} </h2>
            {items.map(item => (
                <React.Fragment key={item.id}>
                    <Link
                        to={item.submenu ? '#' : `${basePath}/${item.path}`}
                        className={determineActive(item) ? styles.navigationItemActive : styles.navigationItem}
                        onClick={() => item.submenu && toggleSubMenu(item.id)}
                    >
                        {renderLabel(item)}
                    </Link>
                    {item.submenu && activeSubMenu === item.id && (
                        <div className={styles.subMenu}>
                            {item.submenu.map(subItem => (
                                <Link
                                    key={subItem.id}
                                    to={`${basePath}/${item.path}/${subItem.path}`}
                                    className={styles.navigationItem}
                                >
                                    <i>{renderLabel(subItem)}</i>
                                </Link>
                            ))}
                        </div>
                    )}
                </React.Fragment>
            ))}
        </div>
    );
}

NavigationList.propTypes = {
    items: PropTypes.array.isRequired,
    determineActive: PropTypes.func.isRequired,
    renderLabel: PropTypes.func,
    basePath: PropTypes.string,
};

export default NavigationList;
