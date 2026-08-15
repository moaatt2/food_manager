import { StrictMode, useState } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'

interface ButtonProps {
  title: string;
  disabled:boolean;
}

// Single Input
function NamedButton({title}: {title: string}) {
  return (
    <button>{title}</button>
  )
}

// Multiple inputs
function ControllableButton({title, disabled}: ButtonProps) {
  return (
    <button disabled={disabled}>{title}</button>
  )
}

// Test Nesting Components
function TestForm() {
  return (
    <form>
      <NamedButton title="submit" />
    </form>
  )
}

// Button click reaction
function ButtonClicker() {
  function handleClick() {
    alert('You clicked me!');
  }

  return (
    <div>
    <h2>0 Clicks</h2>
    <button onClick={handleClick}>Click Me</button>
    </div>
  )
}

// Button Clicker with state - update count on click
function ButtonClicker2() {
  const [count, setCount] = useState(0)

  function handleClick() {
    setCount(count + 1 );
  }

  return (
    <div>
    <h2>{count} Clicks</h2>
    <button onClick={handleClick}>Click Me</button>
    </div>
  )
}


interface ClickerProps {
  count: number;
  onClick: ()=>void;
}

// Button Clicker taking state from app to share state across multiple instances
function ButtonClicker3({count, onClick}: ClickerProps) {
  return (
    <div>
    <h2>{count} Clicks</h2>
    <button onClick={onClick}>Click Me</button>
    </div>
  )
}


export default function TestApp() {
  const[count, setCount] = useState(0)

  function handleClick() {
    setCount(count + 1 );
  }

  return (
    <div>
      <h1>Hello Vite</h1>
      <NamedButton title="Named Button"/>
      <br />
      <ControllableButton title="Controllable button" disabled={false}/>
      <br />
      <TestForm/>
      <br />
      <ButtonClicker />
      <br />
      <ButtonClicker2 />
      <br />
      <ButtonClicker2 />
      <br />
      <ButtonClicker3 count={count} onClick={handleClick}/>
      <br />
      <ButtonClicker3 count={count} onClick={handleClick}/>
    </div>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <TestApp />
  </StrictMode>,
)
