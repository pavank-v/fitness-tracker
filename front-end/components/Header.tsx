"use client";

import { useState } from "react";
import SearchAndSelect from "./SearchAndSelect";
import { User, Menu, X } from "lucide-react";

const Header = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  return (
    <>
      <div className="sticky top-5 z-10 bg-gradient-to-br from-blue-900/30 to-cyan-900/3 backdrop-blur-3xl border border-gray-600 py-2 rounded-full max-w-7xl mx-2 md:mx-3 lg:mx-auto">
        <div className="flex items-center justify-between px-5">
          <div className="flex items-center gap-2">
            <p className="bg-gradient-to-t from-cyan-500 to-cyan-700 inline-block 
              text-transparent bg-clip-text font-bold text-xl font-sans">MetaFit</p>
            <svg className="w-8 h-8" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="2" y="10" width="4" height="12" rx="1" fill="#0e7490" />
              <rect x="6" y="8" width="4" height="16" rx="1" fill="#06b6d4" />
              <rect x="10" y="13" width="12" height="6" rx="1" fill="#0e7490" />
              <rect x="22" y="8" width="4" height="16" rx="1" fill="#06b6d4" />
              <rect x="26" y="10" width="4" height="12" rx="1" fill="#0e7490" />
            </svg>
          </div>

          <div className="hidden lg:flex space-x-10 text-white font-medium">
            <a href="#" className="text-gray-300/85 hover:bg-gradient-to-r hover:from-cyan-500 
              hover:to-cyan-700 hover:text-transparent hover:bg-clip-text">Explore</a>
            <a href="#" className="text-gray-300/85 hover:bg-gradient-to-r hover:from-cyan-500 
              hover:to-cyan-700 hover:text-transparent hover:bg-clip-text">Workouts</a>
            <a href="#" className="text-gray-300/85 hover:bg-gradient-to-r hover:from-cyan-500 
              hover:to-cyan-700 hover:text-transparent hover:bg-clip-text">Diet</a>
            <a href="#" className="text-gray-300/85 hover:bg-gradient-to-r hover:from-cyan-500 
              hover:to-cyan-700 hover:text-transparent hover:bg-clip-text">My Plan</a>
          </div>

          <div className="flex items-center gap-4">
            <div className="hidden sm:block">
              <SearchAndSelect />
            </div>
            <User className="hidden sm:block w-8 h-8 stroke-[url(#gradient)]" />
            <button
              className="lg:hidden text-white focus:outline-none"
              onClick={toggleMobileMenu}
              aria-label={mobileMenuOpen ? "Close menu" : "Open menu"}
            >
              {mobileMenuOpen ?
                <X className="w-6 h-6 stroke-cyan-400" /> :
                <Menu className="w-6 h-6 stroke-cyan-400" />
              }
            </button>
            <div ><svg width="0" height="0">
              <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#06b6d4" />
                  <stop offset="100%" stopColor="#0e7490" />
                </linearGradient>
              </defs>
            </svg>
            </div>
          </div>
        </div>
      </div>

      {mobileMenuOpen && (
        <div className="lg:hidden fixed inset-0 z-50 bg-gray-900/95 pt-20">
          <button
            className="absolute top-6 right-5 text-white focus:outline-none"
            onClick={toggleMobileMenu}
            aria-label="Close menu"
          >
            <X className="w-6 h-6 stroke-cyan-400" />
          </button>

          <div className="flex flex-col items-center px-4 py-6 space-y-6">
            <div className="w-full max-w-sm mb-4">
              <SearchAndSelect />
            </div>
            <a href="#" className="text-white text-lg font-medium py-2 hover:text-cyan-400 transition">Explore</a>
            <a href="#" className="text-white text-lg font-medium py-2 hover:text-cyan-400 transition">Workouts</a>
            <a href="#" className="text-white text-lg font-medium py-2 hover:text-cyan-400 transition">Diet</a>
            <a href="#" className="text-white text-lg font-medium py-2 hover:text-cyan-400 transition">My Plan</a>
            <div className="flex items-center justify-center mt-6">
              <div className="p-3 rounded-full bg-gray-800/50">
                <User className="w-8 h-8 stroke-[url(#gradient)]" />
              </div>
            </div>
          </div>
        </div>
      )}

    </>
  );
};

export default Header;