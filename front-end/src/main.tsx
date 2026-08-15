import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'

interface ButtonProps {
  title: string;
  disabled:boolean;
}

function TestButton({title, disabled}: ButtonProps) {
  return (
    <button disabled={disabled}>{title}</button>
  )
}

export default function TestApp() {
  return (
    <div>
      <h1>Hello</h1>
      <TestButton title="Test" disabled={false}/>
    </div>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <TestApp />
  </StrictMode>,
)
