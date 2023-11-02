import { Link } from "react-router-dom";

function Home() {
    return (
        <>
            <div className="Home" style={{ backgroundImage: `url(${process.env.PUBLIC_URL}/cover.jpg)`, position: 'relative', height: '95vh', color: 'white' }}>
                <h1>Home</h1>
                <div className="Cover">
                </div>
                <div className="Quick-links" style={{ position: 'absolute', bottom: 0, width: '100%', display: 'flex', justifyContent: 'space-evenly', alignItems: 'center' }}>
                    <Link to="shop">Shop</Link>
                    <Link to="locate/store">Store Locator</Link>
                </div>
            </div>
        </>
    );
}

export default Home;