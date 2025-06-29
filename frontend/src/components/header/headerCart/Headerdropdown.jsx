import homeImg from '../../../assets/home-img-1.png'
import '../../../styles/header/cart/cartDropdown.css'
import PropTypes from 'prop-types'

export default function Dropdown({ items }) {
    return (
        <div className="dropdown">
            <button className="dropdown--btn align-items-center">
                <i className="bx bx-cart-alt"></i>
                <span className="badge">{items.length}</span>
            </button>
            <div className="dropdown--content">
                {items.length === 0 ? (
                    <p>No Items in Cart</p>
                ) : (
                    items.map((items, index) => (
                        <a 
                            href="/!"
                            key={index}
                            className='d-flex cart--preview'
                        >
                            <img 
                                src={homeImg} 
                                alt="Item" 
                            />
                            <p>Mobile Phone</p>
                        </a>
                    ))
                )}
                <a href="/" className="link--btn">View More</a>
            </div>
        </div>
    )
}

// Define PropTypes for validation
Dropdown.propTypes = {
  items: PropTypes.arrayOf(PropTypes.string).isRequired,
};

// Set default props (optional, but useful)
Dropdown.defaultProps = {
  items: [],
};