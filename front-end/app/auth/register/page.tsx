"use client";

import type React from 'react';
import { UserPlus } from 'lucide-react';
import api from '@/lib/api';
import { ACCESS_TOKEN, REFRESH_TOKEN } from '@/lib/constant';
import { useState } from 'react'
import { useRouter } from 'next/navigation';
import axios from 'axios';

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

  const [error, setError] = useState('');
  const router = useRouter();

  const registrationData = {
    username: formData.username,
    password: formData.password,
    email: formData.email,
    first_name: formData.first_name || undefined,
    last_name: formData.last_name || undefined,
    profile: {
      age: formData.age ? Number(formData.age) : undefined,
      gender: formData.gender,
      weight: formData.weight ? Number(formData.weight) : undefined,
      height: formData.height ? Number(formData.height) : undefined,
      current_level: formData.current_level,
      body_fat_percentage: formData.body_fat_percentage ? Number(formData.body_fat_percentage) : undefined,
      goal: formData.goal,
    },
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target as HTMLInputElement | HTMLSelectElement;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    console.log("Submitting form with data:", registrationData);

    try {
      const response = await api.post("/auth/user/", registrationData);
      console.log("Registration Response:", response);

      if (response.status === 200 || response.status === 201) {
        console.log("User registered successfully! Redirecting...");

        localStorage.setItem(ACCESS_TOKEN, response.data.access);
        localStorage.setItem(REFRESH_TOKEN, response.data.refresh);

        window.location.href = "/auth/login";
      } else {
        console.log("Unexpected response:", response);
        setError("Unexpected response from the server.");
      }
    } catch (err: unknown) {
      console.log("Registration Error:", err);

      if (axios.isAxiosError(err)) {
        console.log("Backend Response:", err.response?.data);
        setError(err.response?.data?.detail || "Registration Failed");
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unknown error occurred");
      }
    }
  };



  return (
    <>
      <div className="relative min-h-screen text-white font-sans z-10">
        <div className="relative flex justify-center items-center min-h-screen py-12 px-4 sm:px-6 lg:px-8">
          <div className="bg-black bg-opacity-30 backdrop-blur-xl p-8 rounded-2xl shadow-2xl w-full max-w-2xl border border-gray-700/50">
            <div className="flex items-center justify-center mb-8">
              <UserPlus className="w-8 h-8 text-cyan-500 mr-3" />
              <h2 className="text-3xl font-extrabold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
                Create Your Account
              </h2>
            </div>

            {error && (
              <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-lg">
                <p className="text-red-400 text-center text-sm">{error}</p>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-300">
                      Username
                    </label>
                    <input
                      type="text"
                      name="username"
                      value={formData.username}
                      onChange={handleChange}
                      required
                      maxLength={150}
                      className="mt-1 block w-full px-4 py-3 bg-gray-800/50 border border-gray-600/50 text-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-transparent transition-all duration-200 placeholder-gray-500"
                      placeholder="Choose a username"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-300">
                      Email Address
                    </label>
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      required
                      className="mt-1 block w-full px-4 py-3 bg-gray-800/50 border border-gray-600/50 text-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-transparent transition-all duration-200 placeholder-gray-500"
                      placeholder="your@email.com"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-300">
                      Password
                    </label>
                    <input
                      type="password"
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      required
                      className="mt-1 block w-full px-4 py-3 bg-gray-800/50 border border-gray-600/50 text-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-transparent transition-all duration-200"
                    />
                  </div>

                  <div className="grid grid-rows-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-300">
                        First Name
                      </label>
                      <input
                        type="text"
                        name="first_name"
                        value={formData.first_name}
                        onChange={handleChange}
                        className="mt-1 block w-full px-4 py-3 bg-gray-800/50 border border-gray-600/50 text-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-transparent transition-all duration-200"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-300">
                        Last Name
                      </label>
                      <input
                        type="text"
                        name="last_name"
                        value={formData.last_name}
                        onChange={handleChange}
                        className="mt-1 block w-full px-4 py-3 bg-gray-800/50 border border-gray-600/50 text-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-transparent transition-all duration-200"
                      />
                    </div>
                  </div>
                </div>

                <div className="space-y-6">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-300">
                        Age
                      </label>
                      <input
                        type="number"
                        name="age"
                        value={formData.age}
                        onChange={handleChange}
                        className="mt-1 block w-full px-4 py-3 bg-gray-800/50 border border-gray-600/50 text-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-transparent transition-all duration-200"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-300">
                        Gender
                      </label>
                      <select
                        name="gender"
                        value={formData.gender}
                        onChange={handleChange}
                        className="mt-1 block w-full px-4 py-3 bg-gray-800/50 border border-gray-600/50 text-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-transparent transition-all duration-200"
                      >
                        <option className="bg-gray-900 text-gray-100 py-2" value="M">Male</option>
                        <option className="bg-gray-900 text-gray-100 py-2" value="F">Female</option>
                      </select>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-300">
                        Weight (kg)
                      </label>
                      <input
                        type="number"
                        name="weight"
                        value={formData.weight}
                        onChange={handleChange}
                        required
                        className="mt-1 block w-full px-4 py-3 bg-gray-800/50 border border-gray-600/50 text-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-transparent transition-all duration-200"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-300">
                        Height (cm)
                      </label>
                      <input
                        type="number"
                        name="height"
                        value={formData.height}
                        onChange={handleChange}
                        className="mt-1 block w-full px-4 py-3 bg-gray-800/50 border border-gray-600/50 text-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-transparent transition-all duration-200"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-300">
                      Current Level
                    </label>
                    <select
                      name="current_level"
                      value={formData.current_level}
                      onChange={handleChange}
                      required
                      className="mt-1 block w-full px-4 py-3 bg-gray-800/50 border border-gray-600/50 text-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-transparent transition-all duration-200"
                    >
                      <option className="bg-gray-900 text-gray-100 py-2" value="Beginner">Beginner</option>
                      <option className="bg-gray-900 text-gray-100 py-2" value="Intermediate">Intermediate</option>
                      <option className="bg-gray-900 text-gray-100 py-2" value="Advance">Advanced</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-300">
                      Body Fat Percentage
                    </label>
                    <input
                      type="number"
                      name="body_fat_percentage"
                      value={formData.body_fat_percentage}
                      onChange={handleChange}
                      className="mt-1 block w-full px-4 py-3 bg-gray-800/50 border border-gray-600/50 text-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-transparent transition-all duration-200"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-300">
                      Goal
                    </label>
                    <select
                      name="goal"
                      value={formData.goal}
                      onChange={handleChange}
                      required
                      className="mt-1 block w-full px-4 py-3 bg-gray-800/50 border border-gray-600/50 text-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-transparent transition-all duration-200"
                    >
                      <option className="bg-gray-900 text-gray-100 py-2" value="Lose">Lose Weight</option>
                      <option className="bg-gray-900 text-gray-100 py-2" value="Gain">Build Muscle</option>
                      <option className="bg-gray-900 text-gray-100 py-2" value="Maintain">Maintain Weight</option>
                    </select>
                  </div>
                </div>
              </div>

              <button
                type="submit"
                className="w-full py-3 px-4 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-xl hover:from-cyan-600 hover:to-blue-600 focus:outline-none focus:ring-4 focus:ring-cyan-500/50 transform hover:scale-[1.02] transition-all duration-200 font-medium text-lg shadow-lg shadow-cyan-500/25"
              >
                Create Account
              </button>
            </form>
          </div>
        </div>
      </div>
    </>
  );
};

export default Register;