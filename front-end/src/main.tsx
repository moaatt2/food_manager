import { StrictMode, useState } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import './main.css'


/**
 * Interfaces
 */

interface ButtonProps {
  title: string;
  disabled:boolean;
}


interface ClickerProps {
  count: number;
  onClick: ()=>void;
}


interface Meal {
  id:         number
  name:       string
  source:     string | null
  type:       Array<string>
  num_meals:  number
  keeps_days: number
  created_at: string
  updated_at: string
  deleted_at: string | null
}


/**
 * API Functions
 */

function getMeal(meal_id: number): Promise<Meal> {
  return fetch(`http://localhost:3000/v1/meal/${meal_id}`, {
    method: 'Get',
  })
  .then(res => res.json())
  .then(res => {return res.meal as Meal})
}
const meal = await getMeal(1);
// console.log(await getMeal(1)); // Working


function getMeals(): Promise<Meal[]> {
  return fetch('http://localhost:3000/v1/search/meals', {
    method: 'Get',
  })
  .then(res => res.json())
  .then(res => {return res as Meal[]})
}
// console.log(await getMeals()); // Working


/**
 * UI Functions
 */

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

// Button Clicker taking state from app to share state across multiple instances
function ButtonClicker3({count, onClick}: ClickerProps) {
  return (
    <div>
    <h2>{count} Clicks</h2>
    <button onClick={onClick}>Click Me</button>
    </div>
  )
}


// Card for a meal
function MealCard({meal}: {meal: Meal}) {

  // Simplify Date Line
  let updated: boolean = meal.created_at != meal.updated_at;
  let createdDate: string = (new Date(meal.created_at)).toLocaleDateString();
  let updatedDate: string = (new Date(meal.updated_at)).toLocaleDateString();

  // Make Source Easier
  let sourceSection: string = `Source: ${meal.source} | `;

  // Sort out types
  let typeSection: React.JSX.Element;
  if (meal.type.length == 1) {
    typeSection = (<p>Type: {meal.type[0]}</p>);
  } else {
    typeSection = (<p>Types: {meal.type.join(', ')}</p>);
  }

  return (
    <div className="mealCard" key={meal.id}>
        <h3 className="mealTitle">{meal.name}</h3>
        {typeSection}
        <p>{meal.source && sourceSection} Makes {meal.num_meals * 2} Portions | Keeps for {meal.keeps_days + 1} Days</p>
        <p className="dateText">Created: {createdDate} {updated && (` | Updated: ${updatedDate}`)}</p>
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
      <hr />
      <MealCard meal={meal} />
    </div>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <TestApp />
  </StrictMode>,
)


