import styled from 'styled-components';

export default function Switch() {
return (
    <StyledWrapper>
      <div className="toggle-wrapper">
        <input type="checkbox" className="toggle-checkbox" />
        <div className="toggle-container">  
          <div className="toggle-button">
            <div className="toggle-button-circles-container">
              <div className="toggle-button-circle" />
              <div className="toggle-button-circle" />
              <div className="toggle-button-circle" />
              <div className="toggle-button-circle" />
              <div className="toggle-button-circle" />
              <div className="toggle-button-circle" />
              <div className="toggle-button-circle" />
              <div className="toggle-button-circle" />
              <div className="toggle-button-circle" />
              <div className="toggle-button-circle" />
              <div className="toggle-button-circle" />
              <div className="toggle-button-circle" />
            </div>
          </div>
        </div>
      </div>
    </StyledWrapper>
  );
}

const StyledWrapper = styled.div`
  .toggle-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    border-radius: 99px;
    padding: .125em;
    background-image: linear-gradient(to bottom,rgb(255, 255, 255),rgb(53, 52, 52));
    box-shadow: 0 1px 1px rgba(78, 77, 77, 0.6);
    font-size: 2rem;
  }

  .toggle-checkbox {
    appearance: none;
    position: absolute;
    z-index: 1;
    border-radius: inherit;
    width: 100%;
    height: 100%;
    /* fix em sizing */
    font: inherit;
    opacity: 0;
    cursor: pointer;
  }

  .toggle-container {
    display: flex;
    align-items: center;
    position: relative;
    border-radius: 99px;
    width: 3em;
    height: 1.5em;
    background-color:rgb(255, 255, 255);
    box-shadow: inset 0 0 .0625em .125em rgba(5, 5, 5, 0.2), inset 0 .0625em .125em rgba(0, 0, 0, 0.4);
    transition: background-color .4s linear;
  }

  .toggle-checkbox:checked + .toggle-container {
    background-color: rgba(91, 94, 99, 0.57);
  }

  .toggle-button {
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    left: .0625em;
    border-radius: 99px;
    width: 1.375em;
    height: 1.375em;
    background-color: #212121;
    box-shadow: inset 0 -.0625em .0625em .125em rgba(5, 5, 5, 0.2), inset 0 -.125em .0625em rgba(5, 5, 5, 0.2), inset 0 .1875em .0625em rgba(219, 219, 219, 0.3), 0 .125em .125em rgb(0 0 0 / .5);
    transition: left .4s;
  }

  .toggle-checkbox:checked + .toggle-container > .toggle-button {
    left: 1.5625em;
  }

  .toggle-button-circles-container {
    display: grid;
    grid-template-columns: repeat(3, min-content);
    gap: .125em;
    position: absolute;
    margin: 0 auto;
  }

  .toggle-button-circle {
    border-radius: 50%;
    width: .125em;
    height: .125em;
    background-image: radial-gradient(circle at 50% 0, #5e5d5d, #807d7d);
  }`;

