import React from 'react';
import { motion } from 'framer-motion';
import WebSupportFormDelphi from './WebSupportFormDelphi';
import { Sparkles, Users, Activity, Lock, Cpu, Globe } from 'lucide-react';

const DemoCreative = () => {
    return (
        <section id="demo" className="relative py-32 bg-delphi-cream overflow-hidden">
            {/* Background Elements */}
            <div className="absolute inset-0 pointer-events-none">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-orange-200/20 rounded-full blur-[120px] animate-pulse-slow" />
                {/* Tech Grid Overlay */}
                <div className="absolute inset-0 opacity-[0.03]"
                    style={{ backgroundImage: `linear-gradient(#3E2407 1px, transparent 1px), linear-gradient(90deg, #3E2407 1px, transparent 1px)`, backgroundSize: '40px 40px' }}
                />
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 flex flex-col items-center">

                {/* Header */}
                <div className="text-center mb-20 max-w-3xl">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="inline-flex items-center gap-2 px-3 py-1 bg-white/60 backdrop-blur-sm border border-delphi-brown/10 rounded-full mb-6"
                    >
                        <Sparkles className="w-3 h-3 text-orange-500" />
                        <span className="text-xs font-bold text-delphi-brown/60 tracking-wider uppercase">Live Neural Interface</span>
                    </motion.div>

                    <motion.h2
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.1 }}
                        className="text-5xl md:text-7xl font-serif text-delphi-brown mb-6"
                    >
                        Experience the <span className="italic text-orange-500 relative inline-block">
                            Mind.
                            <svg className="absolute w-full h-3 -bottom-1 left-0 text-orange-200" viewBox="0 0 100 10" preserveAspectRatio="none">
                                <path d="M0 5 Q 50 10 100 5" stroke="currentColor" strokeWidth="3" fill="none" />
                            </svg>
                        </span>
                    </motion.h2>
                    <motion.p
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.2 }}
                        className="text-xl text-delphi-brown/70 font-sans leading-relaxed"
                    >
                        Interact with a digital twin trained on thousands of data points. It understands context, tone, and specific knowledge bases instantly.
                    </motion.p>
                </div>

                {/* Main Console Container */}
                <div className="relative w-full max-w-5xl">

                    {/* Floating Stats - Left */}
                    <motion.div
                        initial={{ x: -50, opacity: 0 }}
                        whileInView={{ x: 0, opacity: 1 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.4 }}
                        className="absolute -left-12 top-20 hidden md:flex items-center gap-3 bg-white/80 backdrop-blur-md p-4 rounded-xl shadow-lg border border-delphi-brown/5 animate-float"
                    >
                        <div className="w-10 h-10 rounded-full bg-green-50 flex items-center justify-center text-green-600">
                            <Users className="w-5 h-5" />
                        </div>
                        <div>
                            <div className="text-xs font-bold text-delphi-brown/40 uppercase">Active Users</div>
                            <div className="text-lg font-bold text-delphi-brown">2,841</div>
                        </div>
                    </motion.div>

                    {/* Floating Stats - Right */}
                    <motion.div
                        initial={{ x: 50, opacity: 0 }}
                        whileInView={{ x: 0, opacity: 1 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.6 }}
                        className="absolute -right-12 bottom-40 hidden md:flex items-center gap-3 bg-white/80 backdrop-blur-md p-4 rounded-xl shadow-lg border border-delphi-brown/5 animate-float-delayed"
                    >
                        <div className="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center text-blue-600">
                            <Activity className="w-5 h-5" />
                        </div>
                        <div>
                            <div className="text-xs font-bold text-delphi-brown/40 uppercase">System Status</div>
                            <div className="text-lg font-bold text-delphi-brown flex items-center gap-2">
                                Online <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                            </div>
                        </div>
                    </motion.div>

                    {/* Floating Stats - Bottom Left */}
                    <motion.div
                        initial={{ x: -20, y: 20, opacity: 0 }}
                        whileInView={{ x: 0, y: 0, opacity: 1 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.5 }}
                        className="absolute -left-4 bottom-20 hidden lg:flex items-center gap-3 bg-white/80 backdrop-blur-md p-3 rounded-xl shadow-lg border border-delphi-brown/5 animate-float-reverse"
                    >
                        <Globe className="w-4 h-4 text-delphi-brown/40" />
                        <span className="text-sm font-medium text-delphi-brown/70">Global Latency: 24ms</span>
                    </motion.div>


                    {/* The Console */}
                    <motion.div
                        initial={{ scale: 0.95, opacity: 0, y: 40 }}
                        whileInView={{ scale: 1, opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.8 }}
                        className="relative z-10"
                    >
                        {/* Glass Border Glow */}
                        <div className="absolute inset-0 rounded-[2.5rem] bg-gradient-to-b from-white/80 to-transparent blur-xl opacity-50 -z-10" />

                        <div className="bg-white/40 backdrop-blur-2xl rounded-[2.5rem] p-2 md:p-4 shadow-2xl border border-white/50 ring-1 ring-delphi-brown/5">
                            <div className="bg-white rounded-[2rem] overflow-hidden shadow-inner md:p-6 lg:p-8">
                                <WebSupportFormDelphi />
                            </div>
                        </div>

                        {/* Decorative 'Connectors' */}
                        <div className="absolute top-1/2 -left-20 w-20 h-[1px] bg-gradient-to-r from-transparent to-delphi-brown/20 hidden md:block" />
                        <div className="absolute top-1/2 -right-20 w-20 h-[1px] bg-gradient-to-l from-transparent to-delphi-brown/20 hidden md:block" />
                    </motion.div>

                </div>
            </div>
        </section>
    );
};

export default DemoCreative;
