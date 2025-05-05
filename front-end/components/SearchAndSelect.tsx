"use client"

import { ChevronDown } from 'lucide-react'
import React, { useState } from 'react'

const SearchAndSelect = () => {
  const [dropdown, setDropdown] = useState(false)
  const [selectedOption, setSelectedOption] = useState('Select')

  const handleSelect = (option: any) => {
    setSelectedOption(option);
    setDropdown(false);
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (selectedOption !== 'Select') {
      console.log('Submitted:', selectedOption);
      // Add your submission logic here
    }
  };

  return (
    <form className="flex items-center gap-1 w-full">
      <div className="relative flex-1 min-w-0">
        <input
          type="search"
          className="w-full p-2.5 text-sm text-gray-200 bg-gray-900/50 border border-gray-700 
          rounded-full focus:ring-2 focus:ring-cyan-500/60 text-center 
          autofill:bg-transparent autofill:text-gray-200 autofill:shadow-none"
          placeholder="Search Info..."
          required
        />
      </div>
      <div className="relative group">
        <button
          type="submit"
          className="flex items-center px-3 sm:px-6 py-2.5 text-sm font-medium text-gray-200 bg-gradient-to-r
            hover:from-cyan-500/90 hover:to-cyan-700/90 rounded-full from-cyan-400/60 to-cyan-600/60 focus:ring-2
            focus:ring-cyan-600/60 focus:ring-offset-2 focus:ring-offset-gray-800 transition-all duration-300 shadow-lg
            hover:shadow-cyan-900/30 whitespace-nowrap"
        >
          <span className="truncate max-w-24">{selectedOption}</span>
          <ChevronDown
            className="w-4 h-4 ml-1 sm:ml-2 transform transition-transform duration-300 group-hover:scale-125"
            onClick={(e) => {
              e.preventDefault();
              setDropdown(!dropdown);
            }}
          />
        </button>
        {dropdown && (
          <div className="absolute right-0 mt-2 w-48 bg-gray-800/50 bg-opacity-40 backdrop-blur-sm border border-gray-700/50 
            rounded-xl shadow-xl z-50 overflow-hidden transform transition-all duration-300 ease-out animate-fadeIn">
            <ul className="py-1">
              <li>
                <button
                  type="button"
                  onClick={() => handleSelect('Nutritional Info')}
                  className="w-full text-left px-6 py-2.5 text-sm text-gray-200 hover:bg-gradient-to-r
                    hover:from-cyan-400/60 hover:to-cyan-600/60"
                >
                  Nutritional Info
                </button>
              </li>
              <li>
                <button
                  type="button"
                  onClick={() => handleSelect('Recipes')}
                  className="w-full text-left px-6 py-2.5 text-sm text-gray-200 hover:bg-gradient-to-r
                    hover:from-cyan-400/60 hover:to-cyan-600/60"
                >
                  Recipes
                </button>
              </li>
            </ul>
          </div>
        )}
      </div>
    </form>
  )
}

export default SearchAndSelect