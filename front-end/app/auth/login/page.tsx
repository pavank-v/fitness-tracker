"use client"

import type React from "react"
import { LogIn } from "lucide-react"
import { useState } from "react"
import { useRouter } from "next/navigation"
import api from "@/lib/api"
import { ACCESS_TOKEN, REFRESH_TOKEN } from "@/lib/constant"
import axios from "axios"

const Login = () => {
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  })

  const [error, setError] = useState("")
  const router = useRouter()

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }))
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError("")

    try {
      console.log("Submitting login request:", formData)
      const res = await api.post("/auth/token/", formData)
      console.log("Login Response:", res)

      if (res.status === 200) {
        console.log("Login successful! Redirecting...");
        localStorage.setItem(ACCESS_TOKEN, res.data.access);
        localStorage.setItem(REFRESH_TOKEN, res.data.refresh);

        if (!res.data.access || !res.data.refresh) {
          console.log("Tokens not received, stopping redirect.");
          return;
        }

        router.push("/home");
      }
    } catch (err) {
      console.log("Login Error", err);

      if (axios.isAxiosError(err)) {
        const errorMessage = err.response?.data?.detail || "Invalid credentials";
        setError(errorMessage);
        return;
      } else {
        setError("An unknown error occurred");
      }
    }
  }


  return (
    <>
      <div className="relative min-h-screen text-white font-sans z-10">
        <div className="relative flex justify-center items-center min-h-screen py-12 px-4 sm:px-6 lg:px-8">
          <div className="bg-black bg-opacity-30 backdrop-blur-xl p-8 rounded-2xl shadow-2xl w-full max-w-md border border-gray-700/50">
            <div className="flex items-center justify-center mb-8">
              <LogIn className="w-8 h-8 text-cyan-500 mr-3" />
              <h2 className="text-3xl font-extrabold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
                Welcome Back
              </h2>
            </div>

            {error && (
              <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-lg">
                <p className="text-red-400 text-center text-sm">{error}</p>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
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
                  className="peer mt-1 block w-full px-4 py-3 bg-gray-900/50 border border-gray-600/50 text-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-transparent transition-all duration-200 placeholder-gray-900"
                  placeholder="Enter your username"
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
                  className="peer mt-1 block w-full px-4 py-3 bg-gray-900/50 border border-gray-600/50 text-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-transparent transition-all duration-200 placeholder-gray-900"
                  placeholder="Enter your password"
                />
              </div>

              <button
                type="submit"
                className="w-full py-3 px-4 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-xl hover:from-cyan-600 hover:to-blue-600 focus:outline-none focus:ring-4 focus:ring-cyan-500/50 transform hover:scale-[1.02] transition-all duration-200 font-medium text-lg shadow-lg shadow-cyan-500/25"
              >
                Sign In
              </button>
            </form>
          </div>
        </div>
      </div>
    </>
  )
}

export default Login

