import { Outlet, Link } from "react-router-dom";
import "../index.css";

function Layout() {
    return (
        <div className="Layout">
            <Outlet />
        </div>
    );
}

export default Layout;