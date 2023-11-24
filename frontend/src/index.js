import {QueryClient, QueryClientProvider} from 'react-query';
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./pages/Layout";
import Home from "./pages/Home";
import Shop from "./pages/shop/Shop";
import StoreLocator from './pages/StoreLocator';
import AdminPanel from './pages/admin/AdminPanel';
import CustomerOrders from './pages/CustomerOrders';
import CustomerOrderDetails from './pages/CustomerOrderDetails';
import ShowStoreInventory from './pages/ShowStoreInventory';
import Cart from './pages/shop/Cart';

import "./index.css";


export default function App() {

  return (
    <QueryClientProvider client={new QueryClient()}>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="shop" element={<Shop />} />
          <Route path="shop/:category_name" element={<Shop />} />
          <Route path="/locate/store" element={<StoreLocator />} />
          <Route path="/admin/*" element={<AdminPanel />} />
          <Route path="/admin/inventory/store/select/details/:store_id" element={<ShowStoreInventory />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/orders" element={<CustomerOrders />} />
          <Route path="/order-details/:orderId" element={<CustomerOrderDetails />} />
          
        </Route>
        <Route path="*" element={<h1>Not Found</h1>} />
      </Routes>
    </BrowserRouter>
    </QueryClientProvider>
  );
}

const rootElement = document.getElementById("root");
ReactDOM.createRoot(rootElement).render(<App />);