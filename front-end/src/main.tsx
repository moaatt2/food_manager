import { StrictMode } from 'react'
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

export default function TestApp() {
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
    </div>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <TestApp />
  </StrictMode>,
)
