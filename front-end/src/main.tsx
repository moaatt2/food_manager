import { StrictMode, useEffect, useState } from 'react'
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
// console.log(await getMeal(1)); // Working


function getMeals(): Promise<Meal[]> {
  return fetch('http://localhost:3000/v1/search/meals', {
    method: 'Get',
  })
  .then(res => res.json())
  .then(res => {return res.meals as Meal[]})
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

// A list of meal cards
function MealCardList() {
  const [meals, setMeals] = useState<Meal[]>([])

  useEffect(() => {
    fetch('http://localhost:3000/v1/search/meals', {
        method: 'Get',
      })
      .then(res => res.json())
      .then(res => setMeals(res.meals))
      .catch((err) => {console.log(err.message)})
  }, []);

  return (
    <div>
      {meals.map((meal) => <div key={`parent_${meal.id}`}><MealCard meal={meal}/></div>)}
    </div>
  )
}


function MealSearchForm() {
  return (
    <form className="mealSearchForm">
      <table>
        <tbody>
          {/* Ingredients Include */}
          <tr>
            <td className='label'><label htmlFor="ingredients_include">Ingredients Include: </label></td>
            <td className='input'><input type="text" name="ingredients_include" /></td>
          </tr>

          {/* Ingredients Exclude */}
          <tr>
            <td className='label'><label htmlFor="ingredients_exclude">Ingredients Exclude: </label></td>
            <td className='input'><input type="text" name="ingredients_exclude" /></td>
          </tr>

          {/* Types */}
          <tr>
            <td className='label'><label htmlFor="types">Type(s): </label></td>
            <td className='input'>
              <select name="types" id="types" multiple>
                <option value="Breakfast">Breakfast</option>
                <option value="Lunch">Lunch</option>
                <option value="Dinner">Dinner</option>
                <option value="Dessert">Dessert</option>
              </select>
            </td>
          </tr>

          {/* Minimum Average Review */}
          <tr>
            <td className='label'><label htmlFor="min_avg_review">Minium Average Review: </label></td>
            <td className='input'><input type="number" name="min_avg_review" id="min_avg_review" min={0} max={5} step={0.1} defaultValue={4} /></td>
          </tr>
          <tr>
            <td colSpan={2}><button type="submit">Update Filters</button></td>
          </tr>
        </tbody>
      </table>
    </form>
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
      <MealCardList />
      <hr />
      <MealSearchForm />
    </div>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <TestApp />
  </StrictMode>,
)


