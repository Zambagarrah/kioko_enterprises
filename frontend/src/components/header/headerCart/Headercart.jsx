import { useState } from "react";
import Dropdown from "./Headerdropdown";
import '../../../styles/header/cart/cartIcon.css'

export default function Cart() {
    const [cartItems, setCartItems] = useState(['iytem 1', 'item 2', 'item 3']);
    
    return (
        <div className="text-center mt-3">
            <Dropdown items={cartItems} />
            <button
                className="add--btn"
                onClick={() => setCartItems([...cartItems, `Item ${cartItems.length + 1}`])}
            >
                Add Item to Cart
            </button>
        </div>
    )
}