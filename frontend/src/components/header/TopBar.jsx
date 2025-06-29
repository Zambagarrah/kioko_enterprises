import { Link } from 'react-router-dom';
import { searchResults } from '../../Data';
import { useState, useEffect } from 'react';
import Cart from './headerCart/Headercart';
import Switch from '../../UIVerse/switch/Switch';
import '../../styles/header/topbar.css';

export default function TopBar() {
    // Input Section
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [hasSearched, setHasSearched] = useState(false); // Track if a search has been performed

    const handleInputChange = (e) => {
        setQuery(e.target.value);
    };

    // Debounce function to limit the number of searches
    useEffect(() => {
        const handler = setTimeout(() => {
            if (query) {
                const filteredResults = searchResults.filter(item =>
                    item.toLowerCase().includes(query.toLowerCase())
                );
                setResults(filteredResults);
            } else {
                setResults([]);
            }
        }, 300); // Adjust the debounce time as needed

        return () => {
            clearTimeout(handler);
        };
    }, [query]);

    // Function to handle search when Enter key is pressed
    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            setHasSearched(true); // Mark that a search has been performed
            const filteredResults = searchResults.filter(item =>
                item.toLowerCase().includes(query.toLowerCase())
            );
            setResults(filteredResults);
        }
    };

    // Function to handle search button click
    const handleSearchClick = () => {
        setHasSearched(true); // Mark that a search has been performed
        const filteredResults = searchResults.filter(item =>
            item.toLowerCase().includes(query.toLowerCase())
        );
        setResults(filteredResults);
    };

    return (
        <div className="header--topbar d-flex justify-content-between align-items-center">
            <div className="topbar--left d-flex">
                <a href="/" className="logo" aria-label="Home">
                    <span className="logo--initials">DBV</span>
                    <span className="logo--text">Digital Adventures</span>
                </a>
                <a href='/' className="address d-flex align-items-center" aria-label="Select Address">
                    <i className="bx bx-location-plus logo--icon"></i>
                    <div className="address--text">
                        <div className="address--toptext">Hello</div>
                        <div className="address--maintext fw-bold">Select Address</div>
                    </div>
                </a>
            </div>
            <div className="search--bar d-flex">
                <input 
                    className="input--area" 
                    type="text"
                    placeholder="I'm looking for..."
                    value={query}
                    onChange={handleInputChange}
                    onKeyDown={handleKeyDown} // Add onKeyDown event
                    aria-label="Search"
                />
                <div className="search--eg d-flex align-items-center">
                    <a href="/">iphone</a>
                    <a href="/">Projector</a>
                    <a href="/">Smartphone</a>                    
                </div>
                <button 
                    className="bx bx-search-alt"
                    onClick={handleSearchClick} // Use the new search function
                    aria-label="Search"
                ></button>                
                <ul className="search--results">
                    {results.length > 0 ? (
                        results.map((result, index) => (
                            <li key={index}>
                                <a href="/" className="search--result d-flex">{result}</a>
                            </li>
                        ))
                    ) : (
                        hasSearched && <li>No Results Found ! ! !</li> // Show message only after a search
                    )}
                </ul>
            </div>
            <div className="topbar--right d-flex">
                <a href='/' className="notification--bell align-items-center" aria-label="Notifications">
                    <i className="bx bx-bell"></i>
                </a>
                <div className="country"></div>
                <div className="switch align -items-center">
                    <Switch />
                </div>
                <Link to="/login" className="register d-flex align-items-center" aria-label="Sign In/Register">
                    <i className="bx bx-user"></i>
                    <div href="/" className="register--text">
                        <div className="register--toptext">Welcome</div>
                        <div className="register--main text fw-bold">Sign In / Register</div>
                    </div>
                </Link>
                <a href='/' className="cart" aria-label="Cart">
                    <Cart />
                </a>
                <a href='/' className="returns align-items-center justify-content-center" aria-label="Returns & Orders">
                    <div className="returns--toptext">Returns</div>
                    <div className="returns--maintext fw-bold">& Orders</div>
                </a>
            </div>
        </div>
    );
}