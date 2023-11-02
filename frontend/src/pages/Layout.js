import { Outlet, Link } from "react-router-dom";
import "../index.css";

function Layout() {
    return (
        <div className="Layout">
            <nav className="Nav">
                <Link to="/">Home</Link>
                <Link to="shop">Shop</Link>
                <Link to="locate/store">Store Locator</Link>
                <Link to="admin">Admin</Link>
                <Link to="cart">Cart</Link>
            </nav>
            <Outlet />
        </div>
    );
}

export default Layout;