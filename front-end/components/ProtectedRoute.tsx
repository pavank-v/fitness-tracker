"use client"

import type React from "react"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { ACCESS_TOKEN, REFRESH_TOKEN } from "@/lib/constant"
import { jwtDecode } from "jwt-decode"
import api from "@/lib/api"

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const [isAuthorized, setIsAuthorized] = useState<boolean | null>(null);
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    if (typeof window === "undefined") {
      return
    }
    
    const checkAuth = async () => {
      try {
        await auth()
      } catch (error) {
        setIsAuthorized(false)
        setIsLoading(false)
      }
    }
    checkAuth()
  }, [])

  const refresh = async () => {
    const refreshToken = localStorage.getItem(REFRESH_TOKEN)

    try {
      const res = await api.post("auth/token/refresh", { refresh: refreshToken })

      if (res.status === 200) {
        setIsAuthorized(true)
        localStorage.setItem(ACCESS_TOKEN, res.data.access)
      } else {
        setIsAuthorized(false)
      }
    } catch (error) {
      console.log("Error in Refreshing Token", error)
      setIsAuthorized(false)
    }
    setIsLoading(false)
  }

  const auth = async () => {
    const token = localStorage.getItem(ACCESS_TOKEN)

    if (!token) {
      setIsAuthorized(false)
      setIsLoading(false)
      return
    }

    try {
      const decode = jwtDecode(token)
      const tokenExpiration: number = (decode as any).exp
      const now = Date.now() / 1000

      if (tokenExpiration < now) {
        await refresh()
      } else {
        setIsAuthorized(true)
        setIsLoading(false)
      }
    } catch (error) {
      console.log("Error in Decoding", error)
      setIsAuthorized(false)
      setIsLoading(false)
    }
  }

  useEffect(() => {
    if (!isLoading && !isAuthorized) {
      router.replace("/auth/login")
    }
  }, [isLoading, isAuthorized, router])

  if (isLoading) {
    return <div className="flex justify-center items-center min-h-screen">Loading...</div>
  }


  if (!isAuthorized) {
    return null
  }

  return children
}

export default ProtectedRoute