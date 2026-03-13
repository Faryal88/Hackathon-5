import React, { ReactNode } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

interface NavItem {
  name: string;
  href: string;
  icon: string;
}

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const pathname = usePathname() || '';

  const navItems = [
    { name: 'Dashboard', href: '/dashboard', icon: '📊' },
    { name: 'Tickets', href: '/tickets', icon: '🎫' },
    { name: 'Customers', href: '/customer', icon: '👥' },
    { name: 'Conversations', href: '/conversations', icon: '💬' },
    { name: 'Settings', href: '/settings', icon: '⚙️' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-black to-gray-900">
      {/* Header */}
      <header className="bg-black/80 backdrop-blur-md shadow-sm border-b border-green-500/30 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Link href="/" className="flex items-center space-x-3 group">
                <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg flex items-center justify-center group-hover:scale-105 transition-transform duration-200 animate-pulse-glow">
                  <span className="text-xl">🤖</span>
                </div>
                <span className="text-xl font-bold bg-gradient-to-r from-green-400 to-emerald-300 bg-clip-text text-transparent">
                  TechCorp AI Support
                </span>
              </Link>
            </div>

            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <span className="text-sm text-green-400">Agent:</span>
                <span className="text-sm font-medium text-green-300">Support Team</span>
              </div>
              <div className="w-9 h-9 bg-gradient-to-r from-green-500 to-emerald-600 rounded-full flex items-center justify-center text-black text-sm font-bold shadow-lg animate-glow">
                S
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className="w-64 bg-black/50 backdrop-blur-md shadow-sm border-r border-green-500/30 min-h-screen sticky top-16">
          <nav className="p-4">
            <ul className="space-y-1">
              {navItems.map((item) => (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className={`flex items-center space-x-3 px-3 py-3 rounded-xl transition-all duration-200 group ${
                      pathname === item.href
                        ? 'bg-gradient-to-r from-green-600 to-emerald-700 text-black shadow-lg animate-glow'
                        : 'text-green-300 hover:bg-green-900/50 hover:shadow-sm hover:text-green-100'
                    }`}
                  >
                    <span className={`text-lg transition-transform duration-200 group-hover:scale-110 ${
                      pathname === item.href ? 'text-black' : 'text-green-400'
                    }`}>{item.icon}</span>
                    <span className="font-medium transition-colors duration-200">{item.name}</span>
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6 bg-gradient-to-br from-black/50 to-gray-900/50 min-h-screen">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;