"use client"

import Link from "next/link"
import dynamic from "next/dynamic"
import api from "@/lib/api"
import { useEffect, useState } from "react"
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar'
import 'react-circular-progressbar/dist/styles.css'

const DynamicProtectedRoute = dynamic(() => import("@/components/ProtectedRoute"), {
  loading: () => <div>Loading...</div>
})

const Home = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<null | string>(null);
  
  const [userData, setUserData] = useState({
    id: 0,
    username: ' ',
    email: ' ',
    first_name: ' ',
    last_name: ' ',
    profile: {
        age: 0,
        gender: ' ',
        weight: ' ',
        height: ' ',
        current_level: ' ',
        body_fat_percentage: ' ',
        goal: ' ',
        id: 0,
        user: 0
    }
  })

  const [fitnessStats, setFitnessStats] = useState([{
        calorie_budget: 0,
        protein: 0,
        carbs: 0,
        fats: 0,
        start_date: ' ',
        end_date: ' '
  }]);

  const [foodData, setFoodData] = useState({
    food_log: [],
    daily_summary: {
        total_calories: 0,
        remaining_calories: 0,
        total_protein: 0,
        remaining_protein: 0,
        total_carbs: 0,
        remaining_carbs: 0,
        total_fats: 0,
        remaining_fats: 0
    },
  })

  const [waterConsumed, _setWaterConsumed] = useState({
    consumed: 4,
    target: 5
  })

  const [activity, _setActivity] = useState({
    takenSteps: 7191,
    targetSteps: 10000,
    minutes: 20,
    targetMinutes: 60,
    calBurnt: 233
  })

  const [foodLogForm, setFoodLogForm] = useState(false)
  const showFoodForm = () => setFoodLogForm(true)
  const hideFoodForm = () => setFoodLogForm(false)

  const handleFoodLogSubmit = async (e: any) => {
    e.preventDefault();

    const response = await api.post("/api/food-log/", );

  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        const userResponse = await api.get("/auth/user");
        setUserData(userResponse.data);
        const fitnessResponse = await api.get("/api/personal-diet-plan")
        setFitnessStats(fitnessResponse.data)
        const foodResponse = await api.get("/api/food-log")
        setFoodData(foodResponse.data)
        console.log("Successfully got the response");
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-900">
        <div className="text-center">
          <div className="animate-pulse flex justify-center">
            <div className="h-2 w-16 bg-gradient-to-r from-cyan-500 to-cyan-700 rounded"></div>
          </div>
        </div>
      </div>
    )
  };

  if (error) {
    return <h1 className="flex justify-center text-center">Error occurred: {error}</h1>
  }

  const caloriePercentage = Math.min(Math.round((foodData.daily_summary.total_calories / fitnessStats[0].calorie_budget) * 100), 100);
  const waterPercentage = Math.min(Math.round((waterConsumed.consumed / waterConsumed.target) * 100), 100);
  const stepsPercentage = Math.min(Math.round((activity.takenSteps / activity.targetSteps) * 100), 100);
  const activeMinutesPercentage = Math.min(Math.round((activity.minutes / activity.targetMinutes) * 100), 100);
  
  return (
    <DynamicProtectedRoute>
      <div className="text-white font-sans">
        <div className="min-h-screen px-4 py-24 md:px-8 lg:px-12">
          <div className="max-w-6xl mx-auto">
            <div className="mb-12">
              <h1 className="text-4xl font-bold mb-3 text-white">
                Hi {userData?.first_name} <span className="text-cyan-400">👋</span>
              </h1>
              <p className="text-lg text-gray-300">Let's crush your fitness goals today</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2 space-y-8">
                <div className="bg-gray-800/40 backdrop-blur-lg rounded-2xl p-8 border border-gray-700/30 shadow-xl">
                  <h2 className="text-2xl font-semibold mb-6">Today's Summary</h2>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                    <div className="bg-gradient-to-br from-blue-900/30 to-cyan-900/30 rounded-xl p-5 border border-cyan-800/20 shadow-lg transition-transform hover:scale-105">
                      <div className="mb-3 text-cyan-400 flex justify-center">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                      </div>
                      <div className="text-3xl font-bold text-center">{foodData.daily_summary.total_calories}</div>
                      <div className="text-sm text-gray-300 text-center mt-1">CALORIES</div>
                      <div className="text-sm text-cyan-400 mt-2 text-center">
                        {fitnessStats[0].calorie_budget - foodData.daily_summary.total_calories} remaining
                      </div>
                    </div>
                    
                    <div className="bg-gradient-to-br from-blue-900/30 to-cyan-900/30 rounded-xl p-5 border border-cyan-800/20 shadow-lg transition-transform hover:scale-105">
                      <div className="mb-3 text-cyan-400 flex justify-center">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                      </div>
                      <div className="text-3xl font-bold text-center">{activity.calBurnt}</div>
                      <div className="text-sm text-gray-300 text-center mt-1">CALORIES BURNT</div>
                      <div className="text-sm text-cyan-400 mt-2 text-center">
                        +120 from yesterday
                      </div>
                    </div>
                    
                    <div className="bg-gradient-to-br from-blue-900/30 to-cyan-900/30 rounded-xl p-5 border border-cyan-800/20 shadow-lg transition-transform hover:scale-105">
                      <div className="mb-3 text-cyan-400 flex justify-center">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                        </svg>
                      </div>
                      <div className="text-3xl font-bold text-center">{waterConsumed.consumed}L</div>
                      <div className="text-sm text-gray-300 text-center mt-1">WATER INTAKE</div>
                      <div className="text-sm text-cyan-400 mt-2 text-center">
                        {waterConsumed.target - waterConsumed.consumed}L to go
                      </div>
                    </div>
                    
                    <div className="bg-gradient-to-br from-blue-900/30 to-cyan-900/30 rounded-xl p-5 border border-cyan-800/20 shadow-lg transition-transform hover:scale-105">
                      <div className="mb-3 text-cyan-400 flex justify-center">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                      <div className="text-3xl font-bold text-center">{activity.minutes}</div>
                      <div className="text-sm text-gray-300 text-center mt-1">ACTIVE MINUTES</div>
                      <div className="text-sm text-cyan-400 mt-2 text-center">
                        {activity.targetMinutes - activity.minutes} min to target
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="bg-gray-800/40 backdrop-blur-lg rounded-2xl p-8 border border-gray-700/30 shadow-xl">
                  <div className="flex justify-between items-center mb-6">
                    <h2 className="text-2xl font-semibold">Calorie Budget</h2>
                    <button onClick={showFoodForm} className="px-4 py-2 bg-cyan-600/30 rounded-full text-sm text-cyan-300 hover:bg-cyan-600/40 transition-colors shadow-lg">Log meal</button>
                  </div>

                  {foodLogForm && (
                    <div className="fixed inset-0 backdrop-blur-2xl flex justify-center items-center z-50">
                      <div className="bg-white/10 w-[60vw] max-w-md p-6 rounded-3xl relative">
                        <h2 className="text-2xl font-semibold mb-4 text-gray-800">Log your Meal</h2>
                        <form onSubmit={handleFoodLogSubmit} className="space-y-4">
                          <input
                            type="text"
                            name="food_name"
                            placeholder="Enter the Food Name"
                            className="w-full border border-gray-500 rounded-lg"
                          />
                          <input
                            type="text"
                            name="quantity"
                            placeholder="Enter the Quantity in Grams"
                            className="w-full border border-gray-500 rounded-lg"
                          />
                          <div className="flex justify-end spacex-2">
                            <button
                              type="button"
                              onClick={hideFoodForm}
                              className="px-4 py-2"
                            >
                              cancel
                            </button>
                            <button
                              type="submit"
                              className="px-4 py-2"
                            >
                              Submit
                            </button>
                          </div>
                        </form>
                        <button
                          onClick={hideFoodForm}
                          className="absolute top-3 right-3 text-gray-400">
                            x
                          </button>
                      </div>
                    </div>
                  )}
                  
                  <div className="flex flex-col md:flex-row md:items-center mb-8 gap-8">
                    <div className="w-full md:w-2/3">
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-gray-300">Consumed: {foodData.daily_summary.total_calories} cal</span>
                        <span className="text-gray-300">Target: {fitnessStats[0].calorie_budget} cal</span>
                      </div>
                      <div className="w-full bg-gray-700/40 rounded-full h-4 mb-6 overflow-hidden shadow-inner">
                        <div 
                          className="bg-gradient-to-r from-cyan-500 to-cyan-400 h-4 rounded-full transition-all duration-500 ease-out" 
                          style={{ width: `${caloriePercentage}%` }}
                        ></div>
                      </div>
                      
                      <div className="grid grid-cols-3 gap-6 text-sm">
                        <div>
                          <div className="flex justify-between mb-2">
                            <span className="text-gray-300">Protein</span>
                            <span className="text-gray-300">{foodData.daily_summary.total_protein}g/{fitnessStats[0].protein}g</span>
                          </div>
                          <div className="w-full bg-gray-700/40 rounded-full h-2 overflow-hidden shadow-inner">
                            <div 
                              className="bg-blue-500 h-2 rounded-full transition-all duration-500 ease-out" 
                              style={{ width: `${(foodData.daily_summary.total_protein / fitnessStats[0].protein) * 100}%` }}
                            ></div>
                          </div>
                        </div>
                        
                        <div>
                          <div className="flex justify-between mb-2">
                            <span className="text-gray-300">Carbs</span>
                            <span className="text-gray-300">{foodData.daily_summary.total_carbs}g/{fitnessStats[0].carbs}g</span>
                          </div>
                          <div className="w-full bg-gray-700/40 rounded-full h-2 overflow-hidden shadow-inner">
                            <div 
                              className="bg-green-500 h-2 rounded-full transition-all duration-500 ease-out" 
                              style={{ width: `${(foodData.daily_summary.total_carbs / fitnessStats[0].carbs) * 100}%` }}
                            ></div>
                          </div>
                        </div>
                        
                        <div>
                          <div className="flex justify-between mb-2">
                            <span className="text-gray-300">Fat</span>
                            <span className="text-gray-300">{foodData.daily_summary.total_fats}g/{fitnessStats[0].fats}g</span>
                          </div>
                          <div className="w-full bg-gray-700/40 rounded-full h-2 overflow-hidden shadow-inner">
                            <div 
                              className="bg-yellow-500 h-2 rounded-full transition-all duration-500 ease-out" 
                              style={{ width: `${(foodData.daily_summary.total_fats / fitnessStats[0].fats) * 100}%` }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="w-full md:w-1/3 mt-4 md:mt-0 flex justify-center">
                      <div className="w-36 h-36">
                        <CircularProgressbar
                          value={caloriePercentage}
                          text={`${caloriePercentage}%`}
                          styles={buildStyles({
                            textSize: '1rem',
                            pathColor: '#06b6d4',
                            textColor: '#ffffff',
                            trailColor: '#4A5568',
                            backgroundColor: '#3e98c7',
                          })}
                        />
                        <div className="text-sm text-gray-400 text-center mt-2">of daily goal</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="space-y-8">                
                <div className="bg-gray-800/40 backdrop-blur-lg rounded-2xl p-8 border border-gray-700/30 shadow-xl">
                  <h2 className="text-2xl font-semibold mb-6">Activity Stats</h2>
                  <div className="space-y-6">
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="flex items-center text-gray-300">
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                          </svg>
                          Steps
                        </span>
                        <span className="text-gray-300">{activity.takenSteps.toLocaleString()} / {activity.targetSteps.toLocaleString()}</span>
                      </div>
                      <div className="w-full bg-gray-700/40 rounded-full h-3 overflow-hidden shadow-inner">
                        <div 
                          className="bg-gradient-to-r from-cyan-500 to-cyan-400 h-3 rounded-full transition-all duration-500 ease-out" 
                          style={{ width: `${stepsPercentage}%` }}
                        ></div>
                      </div>
                    </div>
                    
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="flex items-center text-gray-300">
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                          </svg>
                          Water
                        </span>
                        <span className="text-gray-300">{waterConsumed.consumed}L / {waterConsumed.target}L</span>
                      </div>
                      <div className="w-full bg-gray-700/40 rounded-full h-3 overflow-hidden shadow-inner">
                        <div 
                          className="bg-gradient-to-r from-blue-500 to-blue-400 h-3 rounded-full transition-all duration-500 ease-out" 
                          style={{ width: `${waterPercentage}%` }}
                        ></div>
                      </div>
                    </div>
                    
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="flex items-center text-gray-300">
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          Active Time
                        </span>
                        <span className="text-gray-300">{activity.minutes} / {activity.targetMinutes} min</span>
                      </div>
                      <div className="w-full bg-gray-700/40 rounded-full h-3 overflow-hidden shadow-inner">
                        <div 
                          className="bg-gradient-to-r from-green-500 to-green-400 h-3 rounded-full transition-all duration-500 ease-out" 
                          style={{ width: `${activeMinutesPercentage}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="bg-gray-800/40 backdrop-blur-lg rounded-2xl p-8 border border-gray-700/30 shadow-xl">
                  <div className="flex justify-between items-center mb-6">
                    <h2 className="text-2xl font-semibold">Workouts</h2>
                    <button className="px-4 py-2 bg-cyan-600 rounded-full text-sm hover:bg-cyan-700 transition-colors shadow-md">New</button>
                  </div>
                  {/* <div className="space-y-4">
                    {fitnessStats.workouts.map((workout, index) => (
                      <div key={index} className="p-4 rounded-xl bg-gray-800/50 shadow-md flex items-center hover:bg-gray-800/60 transition-colors">
                        <div className={`w-12 h-12 rounded-full mr-4 flex items-center justify-center shadow-md ${
                          workout.status === 'Completed' 
                            ? 'bg-green-900/40 text-green-400' 
                            : workout.status === 'Scheduled' 
                              ? 'bg-cyan-900/40 text-cyan-400'
                              : 'bg-blue-900/40 text-blue-400'
                        }`}>
                          {workout.type === 'Resistance' && '🏋️'}
                          {workout.type === 'Cardio' && '🏃'}
                          {workout.type === 'CrossFit' && '⚡'}
                        </div>
                        <div>
                          <div className="font-medium text-lg">{workout.type}</div>
                          <div className="text-sm text-gray-400">{workout.time}</div>
                        </div>
                        <div className="ml-auto">
                          <span className={`text-sm px-3 py-1 rounded-full shadow-md ${
                            workout.status === 'Completed' 
                              ? 'bg-green-900/30 text-green-400' 
                              : workout.status === 'Scheduled' 
                                ? 'bg-cyan-900/30 text-cyan-400'
                                : 'bg-blue-900/30 text-blue-400'
                          }`}>
                            {workout.status}
                          </span>
                        </div>
                      </div>
                    ))}
                    <Link href="/workouts" className="block w-full p-4 mt-3 bg-gradient-to-r from-cyan-900/30 to-blue-900/30 rounded-xl text-center text-cyan-300 hover:from-cyan-900/40 hover:to-blue-900/40 transition-colors shadow-lg">
                      View all workouts →
                    </Link>
                  </div> */}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DynamicProtectedRoute>
  );
}

export default Home;