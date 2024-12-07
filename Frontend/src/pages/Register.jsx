import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";

const Register = () => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    first_name: "",
    last_name: "",
    age: "",
    gender: "M",
    weight: "",
    height: "",
    current_level: "Beginner",
    body_fat_percentage: "",
    goal: "Lose",
  });

  const registrationData = {
    username: formData.username,
    password: formData.password,
    email: formData.email,
    first_name: formData.first_name || "",  
    last_name: formData.last_name || "",
    profile: {
      age: formData.age || null, 
      gender: formData.gender,
      weight: formData.weight || null, 
      height: formData.height || null, 
      current_level: formData.current_level,
      body_fat_percentage: formData.body_fat_percentage || null, 
      goal: formData.goal,
    },
  };

  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await api.post("/auth/user/", registrationData);

      if (response.status === 201) {
        localStorage.setItem(ACCESS_TOKEN, response.data.access);
        localStorage.setItem(REFRESH_TOKEN, response.data.refresh);
        navigate("/login");
      }
    } catch (err) {
      console.log(err.response, registrationData)
      setError(err.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-gray-100">
      <div className="bg-gray-900 p-8 rounded-xl shadow-xl w-1/2 border border-gray-700">
        <h2 className="text-3xl font-extrabold text-center mb-6 text-gray-400">
          Register
        </h2>
        {error && (
          <p className="text-red-500 text-center mb-4 animate-bounce">
            {error}
          </p>
        )}
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label
              htmlFor="username"
              className="block text-sm font-medium text-gray-400"
            >
              Username
            </label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              maxLength="150"
              className="mt-1 block w-full px-4 py-2 bg-gray-800 border border-gray-600 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-400"
            >
              Email Address
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="mt-1 block w-full px-4 py-2 bg-gray-800 border border-gray-600 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-400"
            >
              Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              className="mt-1 block w-full px-4 py-2 bg-gray-800 border border-gray-600 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="first_name"
              className="block text-sm font-medium text-gray-400"
            >
              First Name
            </label>
            <input
              type="text"
              id="first_name"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
              className="mt-1 block w-full px-4 py-2 bg-gray-800 border border-gray-600 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="last_name"
              className="block text-sm font-medium text-gray-400"
            >
              Last Name
            </label>
            <input
              type="text"
              id="last_name"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
              className="mt-1 block w-full px-4 py-2 bg-gray-800 border border-gray-600 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="age"
              className="block text-sm font-medium text-gray-400"
            >
              Age
            </label>
            <input
              type="number"
              id="age"
              name="age"
              value={formData.age}
              onChange={handleChange}
              className="mt-1 block w-full px-4 py-2 bg-gray-800 border border-gray-600 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="gender"
              className="block text-sm font-medium text-gray-400"
            >
              Gender
            </label>
            <select
              id="gender"
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              className="mt-1 block w-full px-4 py-2 bg-gray-800 border border-gray-600 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            >
              <option value="M">Male</option>
              <option value="F">Female</option>
            </select>
          </div>
          
          <div className="mb-4">
          <label
              htmlFor="weight"
              className="block text-sm font-medium text-gray-400"
            >
              Weight (kg)
            </label>
            <input
              type="number"
              id="weight"
              name="weight"
              value={formData.weight}
              onChange={handleChange}
              required
              className="mt-1 block w-full px-4 py-2 bg-gray-800 border border-gray-600 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="height"
              className="block text-sm font-medium text-gray-400"
            >
              Height (cm)
            </label>
            <input
              type="number"
              id="height"
              name="height"
              value={formData.height}
              onChange={handleChange}
              className="mt-1 block w-full px-4 py-2 bg-gray-800 border border-gray-600 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="current_level"
              className="block text-sm font-medium text-gray-400"
            >
              Current Level
            </label>
            <select
              id="current_level"
              name="current_level"
              value={formData.current_level}
              onChange={handleChange}
              required
              className="mt-1 block w-full px-4 py-2 bg-gray-800 border border-gray-600 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            >
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advance">Advanced</option>
            </select>
          </div>
          <div className="mb-4">
            <label
              htmlFor="body_fat_percentage"
              className="block text-sm font-medium text-gray-400"
            >
              Body Fat Percentage
            </label>
            <input
              type="number"
              id="body_fat_percentage"
              name="body_fat_percentage"
              value={formData.body_fat_percentage}
              onChange={handleChange}
              className="mt-1 block w-full px-4 py-2 bg-gray-800 border border-gray-600 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            />
          </div>
          <div className="mb-6">
            <label
              htmlFor="goal"
              className="block text-sm font-medium text-gray-400"
            >
              Goal
            </label>
            <select
              id="goal"
              name="goal"
              value={formData.goal}
              onChange={handleChange}
              required
              className="mt-1 block w-full px-4 py-2 bg-gray-800 border border-gray-600 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
            >
              <option value="Lose">Lose Weight</option>
              <option value="Gain">Build Muscle</option>
              <option value="Maintain ">Maintain Weight</option>
            </select>
          </div>
          <button
            type="submit"
            className="w-full py-2 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-500 focus:outline-none focus:ring-4 focus:ring-blue-700 shadow-lg transition"
          >
            Register
          </button>
        </form>
      </div>
    </div>
  );
};

export default Register;