"use client"

import { ACCESS_TOKEN } from "@/lib/constant";
import { useRouter } from "next/navigation";
import { useEffect } from "react";


const Logout = () => {
  const router = useRouter();

  useEffect(() => {
    if (localStorage.getItem(ACCESS_TOKEN)) {
      console.log("Logging out...");
      localStorage.clear();
      router.push("/auth/login");
    }
  }, [router])

  return null;
}

export default Logout
