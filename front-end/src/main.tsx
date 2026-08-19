import React, { StrictMode, useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import './main.css'

// Load varianbles from .env file
const API_ADDRESS: string = import.meta.env.VITE_API_ADDRESS;
const API_PORT:    string = import.meta.env.VITE_API_PORT;

/**
 * Interfaces
 */
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

interface Ingredient {
  id:   number
  name: string
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


// Component allowing the user to search for a meal
function MealSearchComponent() {
  const [meals, setMeals] = useState<Meal[]>([])
  const [ingredients, setIngredients] = useState<Ingredient[]>([])


  const [minAvgReview, setMinAvgReview] = useState<number>(4);
  function minAvgReviewChange(e: React.ChangeEvent<HTMLInputElement>) {
    setMinAvgReview(e.target.valueAsNumber);
  }

  const [types, setTypes] = useState<string[]>([]);
  function typesChange(e: React.ChangeEvent<HTMLSelectElement>) {
    setTypes([...e.target.options].filter(option => option.selected).map(option => option.value));
  }

  const [includeIngredients, setIncludeIngredients] = useState<string[]>([]);
  function includeIngredientsChange(e: React.ChangeEvent<HTMLSelectElement>) {
    setIncludeIngredients([...e.target.options].filter(option => option.selected).map(option => option.value))
  }

  const [excludeIngredients, setExcludeIngredients] = useState<string[]>([]);
  function excludeIngredientsChange(e: React.ChangeEvent<HTMLSelectElement>) {
    setExcludeIngredients([...e.target.options].filter(option => option.selected).map(option => option.value))
  }

  useEffect(() => {
    // Construct params with 
    let params = new URLSearchParams({
      min_avg_review: minAvgReview.toString(),
    });

    // Add types to filter
    for (let type of types) {
      params.append("types", type);
    }

    // Add Include Ingredients
    for (let includeIngredient of includeIngredients) {
      params.append("ingredients_include", includeIngredient);
    }

    // Add Exclude Ingredients
    for (let excludeIngredient of excludeIngredients) {
      params.append("ingredients_exclude", excludeIngredient);
    }


    // Request Meals
    fetch(`http://${API_ADDRESS}:${API_PORT}/v1/search/meals?` + params.toString(), {
      method: 'Get',
    })
    .then(res => res.json())
    .then(res => setMeals(res.meals))
    .catch((err) => {console.log(err.message)})


    // Get ingredients list a single time
    if (ingredients.length == 0) {
      fetch(`http://${API_ADDRESS}:${API_PORT}/v1/search/ingredients`, {
        method: 'Get',
      })
      .then(res => res.json())
      .then(res => setIngredients(res.ingredients))
      .catch((err) => {console.log(err.message)})
    }
  }, [minAvgReview, types, includeIngredients, excludeIngredients]);

  return (
    <div>
      <form className="mealSearchForm">
        <table>
          <tbody>
            {/* Ingredients Include */}
            <tr>
              <td className='label'><label htmlFor="ingredients_include">Ingredients Include: </label></td>
              <td className='input'>
                <select name="ingredients_include" onChange={includeIngredientsChange} value={includeIngredients} multiple={true} size={4}>
                  {ingredients.map(ingredient => <option key={ingredient.id} value={ingredient.id}>{ingredient.name}</option>)}
                </select>
              </td>
            </tr>

            {/* Ingredients Exclude */}
            <tr>
              <td className='label'><label htmlFor="ingredients_exclude">Ingredients Exclude: </label></td>
              <td className='input'>
                <select name="ingredients_exclude" onChange={excludeIngredientsChange} value={excludeIngredients} multiple={true} size={4}>
                  {ingredients.map(ingredient => <option key={ingredient.id} value={ingredient.id}>{ingredient.name}</option>)}
                </select>
              </td>
            </tr>

            {/* Types */}
            <tr>
              <td className='label'><label htmlFor="types">Type(s): </label></td>
              <td className='input'>
                <select name="types" onChange={typesChange} value={types} multiple={true}>
                  <option value="Breakfast">Breakfast</option>
                  <option value="Lunch">Lunch</option>
                  <option value="Dinner">Dinner</option>
                  <option value="Desert">Dessert</option>
                </select>
              </td>
            </tr>

            {/* Minimum Average Review */}
            <tr>
              <td className='label'><label htmlFor="min_avg_review">Minium Average Review: </label></td>
              <td className='input'><input type="number" onChange={minAvgReviewChange} min={1} max={5} step={0.1} value={minAvgReview} /></td>
            </tr>
          </tbody>
        </table>
      </form>
      <hr />
      <div>
        {meals.map((meal) => <div key={`parent_${meal.id}`}><MealCard meal={meal}/></div>)}
      </div>
    </div>
  )
}


export default function TestApp() {
  return (
    <div>
      <MealSearchComponent />
    </div>
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <TestApp />
  </StrictMode>,
)


