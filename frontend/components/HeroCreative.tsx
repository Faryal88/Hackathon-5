import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Play, Mic, FileText, Video, Sparkles, Brain, Fingerprint } from 'lucide-react';
import Link from 'next/link';

const HeroCreative = () => {
    return (
        <div className="relative w-full min-h-screen bg-delphi-cream flex items-center justify-center overflow-hidden px-4 sm:px-6 lg:px-8 pt-20">
            {/* Subtle Grain Texture Overlay */}
            <div className="absolute inset-0 pointer-events-none opacity-[0.4] mix-blend-multiply"
                style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.5'/%3E%3C/svg%3E")` }}
            />

            {/* Abstract Background Shapes */}
            <div className="absolute top-[-20%] left-[-10%] w-[600px] h-[600px] bg-orange-200/20 rounded-full blur-[100px] animate-pulse-slow" />
            <div className="absolute bottom-[-10%] right-[-5%] w-[500px] h-[500px] bg-delphi-blue/5 rounded-full blur-[100px]" />

            <div className="max-w-7xl w-full mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center relative z-10">

                {/* Left Column: Typography */}
                <div className="text-left space-y-8">

                    <motion.h1
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.1 }}
                        className="flex flex-col font-serif text-6xl md:text-8xl text-delphi-brown leading-[0.9]"
                    >
                        <span>Clone</span>
                        <span>Yourself.</span>
                        <span className="italic text-orange-600 relative inline-block w-fit">
                            Digitally.
                            <svg className="absolute w-full h-3 -bottom-1 left-0 text-orange-200" viewBox="0 0 100 10" preserveAspectRatio="none">
                                <path d="M0 5 Q 50 10 100 5" stroke="currentColor" strokeWidth="3" fill="none" />
                            </svg>
                        </span>
                    </motion.h1>

                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.2 }}
                        className="text-xl md:text-2xl text-delphi-brown/70 font-sans max-w-lg leading-relaxed"
                    >
                        The world's first extensive digital twin engine. Turn your knowledge into an infinite, interactive presence.
                    </motion.p>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8, delay: 0.3 }}
                        className="flex flex-col sm:flex-row gap-4"
                    >
                        <Link href="/dashboard">
                            <button className="group relative px-8 py-4 bg-delphi-brown text-white rounded-xl font-medium text-lg overflow-hidden transition-transform hover:scale-105 active:scale-95 shadow-lg shadow-delphi-brown/20">
                                <span className="relative z-10 flex items-center gap-2">
                                    Launch Dashboard <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                                </span>
                                <div className="absolute inset-0 bg-white/10 translate-y-full group-hover:translate-y-0 transition-transform duration-300" />
                            </button>
                        </Link>
                        <Link href="#demo">
                            <button className="px-8 py-4 bg-transparent border border-delphi-brown/20 text-delphi-brown rounded-xl font-medium text-lg hover:bg-delphi-brown/5 transition-colors flex items-center gap-2">
                                <Play className="w-5 h-5" /> Live Demo
                            </button>
                        </Link>
                    </motion.div>
                </div>

                {/* Right Column: Visual Animation */}
                <div className="relative h-[600px] w-full flex items-center justify-center perspective-1000">
                    {/* Central Brain Card */}
                    <motion.div
                        initial={{ scale: 0.8, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        transition={{ duration: 1, ease: "easeOut" }}
                        className="relative z-20 w-64 h-80 bg-white rounded-[2rem] shadow-2xl border border-delphi-brown/5 p-6 flex flex-col items-center justify-between"
                    >
                        <div className="w-full flex justify-between items-center opacity-50">
                            <Fingerprint className="w-6 h-6 text-delphi-brown" />
                            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                        </div>

                        <div className="relative w-32 h-32">
                            <div className="absolute inset-0 rounded-full bg-gradient-to-tr from-orange-400 to-red-500 blur-xl opacity-20 animate-pulse-slow" />
                            <div className="relative z-10 w-full h-full rounded-full bg-gradient-to-tr from-delphi-brown to-black text-white flex items-center justify-center shadow-inner">
                                <Brain className="w-16 h-16" />
                            </div>
                            {/* Orbit rings inside card */}
                            <div className="absolute inset-[-10px] border border-delphi-brown/10 rounded-full animate-spin-slow" />
                            <div className="absolute inset-[-25px] border border-delphi-brown/5 rounded-full animate-spin-reverse-slow" />
                        </div>

                        <div className="text-center">
                            <div className="font-serif font-bold text-xl text-delphi-brown">Digital You</div>
                            <div className="text-xs text-delphi-brown/40 font-mono mt-1">ID: 8F-2A-9C</div>
                        </div>
                    </motion.div>

                    {/* Floating Input Cards - Feeding the Brain */}
                    {/* 1. Voice Note */}
                    <motion.div
                        initial={{ x: 200, y: -100, opacity: 0, rotate: 10 }}
                        animate={{ x: 120, y: -120, opacity: 1, rotate: 6 }}
                        transition={{ duration: 1, delay: 0.5, type: "spring" }}
                        className="absolute z-10 bg-white p-4 rounded-2xl shadow-xl shadow-delphi-brown/5 border border-delphi-brown/5 flex items-center gap-3 w-48 animate-float"
                    >
                        <div className="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center text-blue-500">
                            <Mic className="w-5 h-5" />
                        </div>
                        <div>
                            <div className="text-xs font-bold text-delphi-brown/60">Voice Note</div>
                            <div className="w-16 h-1 bg-delphi-brown/10 rounded-full mt-1" />
                        </div>
                    </motion.div>

                    {/* 2. Text Input */}
                    <motion.div
                        initial={{ x: -200, y: 50, opacity: 0, rotate: -10 }}
                        animate={{ x: -140, y: 20, opacity: 1, rotate: -6 }}
                        transition={{ duration: 1, delay: 0.7, type: "spring" }}
                        className="absolute z-10 bg-white p-4 rounded-2xl shadow-xl shadow-delphi-brown/5 border border-delphi-brown/5 flex items-center gap-3 w-48 animate-float-delayed"
                    >
                        <div className="w-10 h-10 rounded-full bg-orange-50 flex items-center justify-center text-orange-500">
                            <FileText className="w-5 h-5" />
                        </div>
                        <div>
                            <div className="text-xs font-bold text-delphi-brown/60">Blog Post</div>
                            <div className="w-20 h-1 bg-delphi-brown/10 rounded-full mt-1" />
                        </div>
                    </motion.div>

                    {/* 3. Video Input */}
                    <motion.div
                        initial={{ x: 150, y: 150, opacity: 0, rotate: 5 }}
                        animate={{ x: 100, y: 140, opacity: 1, rotate: 3 }}
                        transition={{ duration: 1, delay: 0.9, type: "spring" }}
                        className="absolute z-10 bg-white p-4 rounded-2xl shadow-xl shadow-delphi-brown/5 border border-delphi-brown/5 flex items-center gap-3 w-48 animate-float-reverse"
                    >
                        <div className="w-10 h-10 rounded-full bg-purple-50 flex items-center justify-center text-purple-500">
                            <Video className="w-5 h-5" />
                        </div>
                        <div>
                            <div className="text-xs font-bold text-delphi-brown/60">Zoom Call</div>
                            <div className="w-12 h-1 bg-delphi-brown/10 rounded-full mt-1" />
                        </div>
                    </motion.div>

                    {/* Connecting Lines (SVG) */}
                    <svg className="absolute inset-0 pointer-events-none z-0 opacity-20">
                        <motion.path
                            d="M 50% 50% L 75% 30%"
                            stroke="#3E2407"
                            strokeWidth="2"
                            strokeDasharray="5,5"
                            initial={{ pathLength: 0 }}
                            animate={{ pathLength: 1 }}
                            transition={{ duration: 1.5, delay: 1 }}
                        />
                        <motion.path
                            d="M 50% 50% L 25% 55%"
                            stroke="#3E2407"
                            strokeWidth="2"
                            strokeDasharray="5,5"
                            initial={{ pathLength: 0 }}
                            animate={{ pathLength: 1 }}
                            transition={{ duration: 1.5, delay: 1.2 }}
                        />
                        <motion.path
                            d="M 50% 50% L 70% 70%"
                            stroke="#3E2407"
                            strokeWidth="2"
                            strokeDasharray="5,5"
                            initial={{ pathLength: 0 }}
                            animate={{ pathLength: 1 }}
                            transition={{ duration: 1.5, delay: 1.4 }}
                        />
                    </svg>

                </div>

            </div>
        </div>
    );
};

export default HeroCreative;
