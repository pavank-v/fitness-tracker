"use client";

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function RootPage() {
  const router = useRouter();

  useEffect(() => {
    router.replace('/home');
  }, [router]);

  return (
    <div className="flex items-center justify-center h-screen bg-gray-900">
      <div className="text-center">
        <div className="flex items-center justify-center space-x-2 mb-4">
          <svg className="w-10 h-10" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="2" y="10" width="4" height="12" rx="1" fill="#0e7490" />
            <rect x="6" y="8" width="4" height="16" rx="1" fill="#06b6d4" />
            <rect x="10" y="13" width="12" height="6" rx="1" fill="#0e7490" />
            <rect x="22" y="8" width="4" height="16" rx="1" fill="#06b6d4" />
            <rect x="26" y="10" width="4" height="12" rx="1" fill="#0e7490" />
          </svg>
        </div>
        <div className="bg-gradient-to-r from-cyan-400 to-cyan-600 inline-block text-transparent bg-clip-text font-bold text-2xl mb-6">
          MetaFit
        </div>
        <div className="animate-pulse flex justify-center">
          <div className="h-2 w-16 bg-gradient-to-r from-cyan-500 to-cyan-700 rounded"></div>
        </div>
      </div>
    </div>
  );
}