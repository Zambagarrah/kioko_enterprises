import React, { useState } from 'react';
import '../../styles/logins/logins.css';

export default function Logins() {
    // State to manage which form is active
    const [isLoginActive, setIsLoginActive] = useState(true);
    const [showPasswordLogin, setShowPasswordLogin] = useState(false);
    const [showPasswordSignup, setShowPasswordSignup] = useState(false);

    const handleRegisterClick = () => {
        setIsLoginActive(false);
    };

    const handleLoginClick = () => {
        setIsLoginActive(true);
    };

    return (
        <section className="login--page d-flex justify-content-center align-items-center">
            <div className={`container ${!isLoginActive ? 'active' : ''}`}>
                {/* Login Form */}
                <div className={`form--box signin d-flex align-items-center text-center text-black ${isLoginActive ? '' : 'hidden'}`}>
                    <form action="">
                        <h1 className='login--header'>Login</h1>
                        <div className="input--box">
                            <input type="text" placeholder="Username" required />
                            <i className="bx bxs-user"></i>
                        </div>
                        <div className="input--box">
                            <input 
                                type={showPasswordLogin ? "text" : "password"} 
                                placeholder="Password" 
                                required 
                            />
                            <i 
                                className={`bx ${showPasswordLogin ? 'bx-low-vision' : 'bx-low-vision'}`} 
                                onClick={() => setShowPasswordLogin(!showPasswordLogin)} 
                                style={{ cursor: 'pointer', position: 'absolute', right: '2rem', top: '50%', transform: 'translateY(-50%)' }}
                            ></i>
                        </div>
                        <div className="forgotpass--link">
                            <a href="/">Forgot password?</a>
                        </div>
                        <button type="submit" className="login--btn">Login</button>
                        <p className='login--text'>or Login with social platforms</p>
                        <div className="login--socials d-flex justify-content-center">
                            <a href="/"><i className="bx bxl-google"></i></a>
                            <a href="/"><i className="bx bxl-apple"></i></a>
                            <a href="/"><i className="bx bx-chat"></i></a>
                            <a href="/"><i className="bx bxl-facebook"></i></a>
                        </div>
                    </form>
                </div>

                {/* Signup Form */}
                <div className={`form--box signup d-flex align-items-center text-center text-black ${isLoginActive ? 'hidden' : ''}`}>
                    <form action="">
                        <h1 className='login--header'>Join Us</h1>
                        <div className="input--box">
                            <input type="text" placeholder="Username" required />
                            <i className="bx bxs-user"></i>
                        </div>
                        <div className="input--box">
                            <input type="email" placeholder="Email" required />
                            <i className="bx bxs-envelope"></i>
                        </div>
                        <div className="input--box">
                            <input 
                                type={showPasswordSignup ? "text" : "password"} 
                                placeholder="Password" 
                                required 
                            />
                            <i 
                                className={`bx ${showPasswordSignup ? 'bx-low-vision' : 'bx-low-vision'}`} 
                                onClick={() => setShowPasswordSignup(!showPasswordSignup)} 
                                style={{ cursor: 'pointer', position: 'absolute', right: '2rem', top: '50%', transform: 'translateY(-50%)' }}
                            ></i>
                        </div>
                        <button type="submit" className="login--btn">Signup</button>
                        <p className='login--text'>or Register with social platforms</p> <div className="login--socials d-flex justify-content-center">
                            <a href="/"><i className="bx bxl-google"></i></a>
                            <a href="/"><i className="bx bxl-apple"></i></a>
                            <a href="/"><i className="bx bx-chat"></i></a>
                            <a href="/"><i className="bx bxl-facebook"></i></a>
                        </div>
                    </form>
                </div>

                {/* Toggle Box */}
                <div className="logintoggle--box">
                    <div className="logintoggle--panel logintoggle--left d-flex justify-content-center align-items-center">
                        <div className="login--header">Hello, Welcome!</div>
                        <p className="login--text logintoggle--text">Don't have an account?</p>
                        <button className='login--btn register-btn' onClick={handleRegisterClick}>Register here</button>
                    </div>
                    <div className="logintoggle--panel logintoggle--right d-flex justify-content-center align-items-center">
                        <div className="login--header">Welcome Back!</div>
                        <p className="login--text logintoggle--text">Already have an account?</p>
                        <button className='login--btn signin-btn' onClick={handleLoginClick}>Login here</button>
                    </div>
                </div>
            </div>
        </section>
    );
}