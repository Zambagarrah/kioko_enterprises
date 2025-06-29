import '../../styles/header/header.css'
import TopBar from './TopBar'
import NavBar from './NavBar'

export default function Header() {
    return (
        <header id="header" className="header">
            <TopBar />
            <NavBar />
        </header>
    )
}