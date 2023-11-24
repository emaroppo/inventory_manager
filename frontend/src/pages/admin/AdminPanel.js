import React from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import AddEntries from "./AddEntries";
import NavigationList from "../components/common/NavigationList";
import adminMenu from './adminMenu.json';
import dataSchema from './dataSchema.json';
import styles from './AdminPanel.module.css';
import StoreLocator from '../StoreLocator';

function AdminPanel() {
    const location = useLocation();

    return (
        <div className={styles.adminContainer}>
            <div className={styles.adminNavigation}>
                <NavigationList
                    items={adminMenu}
                    determineActive={(item) => location.pathname.includes(item.path)}
                    renderLabel={(item) => item.name}
                    basePath="/admin"
                />
            </div>
            <div className={styles.settingsSection}>
                <Routes>
                    <Route 
                        path="inventory/store/select" 
                        element={<StoreLocator />}
                    />
                    <Route 
                        path="db_manager/add_entry" 
                        element={<AddEntries schema={dataSchema} />} 
                    />
                    {/* Additional routes for other menu items can be added here */}
                </Routes>
            </div>
        </div>
    );
}

export default AdminPanel;
