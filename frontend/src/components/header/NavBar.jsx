import "../../styles/header/navbar.css"
import { links } from '../../Data'

export default function NavBar() {
    return (
        <div className="header--navbar d-flex justify-content-between">
            <div className="navbar--left d-flex">
                <a href="/" className="menu d-flex align-items-center">
                    <i className="bx bx-menu-alt-left"></i>
                    <div className="nav--text">Menu</div>
                    <i className="bx bxs-chevrons-down"></i>
                </a>
                <div className="menu--separator">|</div>
                <div className="others d-flex justify-content-center align-items-center">
                    {links.map(({link, url, navclass}, index) => (
                        <ul className="d-flex justify-content-center">
                            <li key={index}>
                                <a href={url} className={navclass}>{link}</a>
                            </li>
                        </ul>
                    ))}
                </div>
            </div>
            <div className="navbar--right d-flex justify-content-center align-items-center">
                <a href="/" className="feedback d-flex">
                    <i className='bx bx-chat'></i>                    
                    <div className="navright--text">Feedback</div>
                </a>
                <div className="menu--separator">|</div>
                <a href="/" className="help--center d-flex">
                    <i className='bx bx-help-circle'></i>
                    <div className="navright--text">Help Center</div>
                </a>
            </div>
        </div>
    )
}