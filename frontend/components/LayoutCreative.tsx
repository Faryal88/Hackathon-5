import React, { ReactNode } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
    LayoutDashboard,
    Ticket,
    Users,
    MessageSquare,
    Settings,
    LogOut,
    Menu,
    X
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface LayoutProps {
    children: ReactNode;
}

const LayoutCreative: React.FC<LayoutProps> = ({ children }) => {
    const pathname = usePathname() || '';
    const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

    const navItems = [
        { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
        { name: 'Tickets', href: '/tickets', icon: Ticket },
        { name: 'Conversations', href: '/conversations', icon: MessageSquare },
    ];

    return (
        <div className="min-h-screen bg-[#FDF6EE] text-[#3E2407] font-sans selection:bg-orange-100 flex overflow-hidden">
            {/* Background Gradients */}
            <div className="absolute inset-0 z-0 pointer-events-none overflow-hidden">
                <div className="absolute top-[-20%] left-[-10%] w-[800px] h-[800px] bg-orange-200/20 rounded-full blur-[120px] mix-blend-multiply" />
                <div className="absolute bottom-[-20%] right-[-10%] w-[600px] h-[600px] bg-blue-100/30 rounded-full blur-[100px] mix-blend-multiply" />
            </div>

            {/* Sidebar - Desktop */}
            <aside className="hidden lg:flex flex-col w-64 h-screen sticky top-0 z-20 border-r border-[#3E2407]/5 bg-white/30 backdrop-blur-md">
                <div className="p-8">
                    <Link href="/" className="block">
                        <h1 className="text-3xl font-serif font-bold text-[#3E2407] tracking-tight">
                            Abdullah<span className="text-orange-500">.</span>
                        </h1>
                    </Link>
                    <div className="mt-2 inline-flex items-center px-2 py-1 bg-[#3E2407]/5 rounded-full border border-[#3E2407]/5">
                        <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse mr-2" />
                        <span className="text-[10px] font-bold uppercase tracking-widest text-[#3E2407]/60">System Online</span>
                    </div>
                </div>

                <nav className="flex-1 px-4 space-y-2 overflow-y-auto">
                    {navItems.map((item) => {
                        const isActive = pathname === item.href;
                        return (
                            <Link key={item.href} href={item.href}>
                                <div className={`
                    group flex items-center gap-4 px-4 py-3 rounded-2xl transition-all duration-300
                    ${isActive
                                        ? 'bg-white shadow-lg shadow-[#3E2407]/5 text-[#3E2407]'
                                        : 'text-[#3E2407]/60 hover:bg-white/50 hover:text-[#3E2407]'
                                    }
                `}>
                                    <item.icon className={`w-5 h-5 transition-transform group-hover:scale-110 ${isActive ? 'text-orange-500' : ''}`} />
                                    <span className="font-medium">{item.name}</span>
                                    {isActive && (
                                        <motion.div
                                            layoutId="activeNav"
                                            className="ml-auto w-1 h-1 rounded-full bg-orange-500"
                                        />
                                    )}
                                </div>
                            </Link>
                        );
                    })}
                </nav>

                <div className="p-4 border-t border-[#3E2407]/5">
                    <button className="flex items-center gap-3 w-full px-4 py-3 text-[#3E2407]/60 hover:text-red-500 hover:bg-red-50 rounded-2xl transition-all">
                        <LogOut className="w-5 h-5" />
                        <span className="font-medium">Disconnect</span>
                    </button>
                </div>
            </aside>

            {/* Mobile Header */}
            <div className="lg:hidden fixed top-0 w-full z-40 bg-white/80 backdrop-blur-md border-b border-[#3E2407]/5 p-4 flex justify-between items-center">
                <h1 className="text-xl font-serif font-bold">Abdullah.</h1>
                <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}>
                    {isMobileMenuOpen ? <X /> : <Menu />}
                </button>
            </div>

            {/* Main Content */}
            <main className="flex-1 overflow-y-auto relative z-10 pt-20 lg:pt-0">
                <div className="max-w-7xl mx-auto p-4 lg:p-8">
                    {children}
                </div>
            </main>
        </div>
    );
};

export default LayoutCreative;
