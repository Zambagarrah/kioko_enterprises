import { Routes, Route, useLocation } from 'react-router-dom';
import Header from './components/header/Header';
import Home from './components/home/Home';
import Logins from './components/logins/Logins';
import NotFound from './components/error/NotFound';
import './App.css';

export default function App() {
  const location = useLocation(); // Get the current location

  // Define an array of paths where the Header should not be displayed
  const noNavbarPaths = ['/login']; // Add more paths as needed

  return (
    <>
      {/* Conditionally render Header based on the current path */}
      {!noNavbarPaths.includes(location.pathname) && <Header />}
      
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Logins />} /> {/* Login page without Header */}
        <Route path="*" element={<NotFound />} /> {/* Optional: Catch-all route */}
      </Routes>
    </>
  );
}