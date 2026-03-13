import React from 'react';
import { motion } from 'framer-motion';
import { MessageCircle, Zap, Globe, MessageSquare, ArrowRight, User, Heart, Mic, Video, FileText } from 'lucide-react';
import Image from 'next/image';

const BentoGridDelphi = () => {
    return (
        <section className="py-24 bg-delphi-cream relative overflow-hidden">
            {/* Header */}
            <div className="text-center max-w-3xl mx-auto px-4 mb-20">
                <h2 className="text-5xl md:text-6xl font-serif text-delphi-brown mb-6">
                    Never miss a question.<br />
                    <span className="text-delphi-brown/60">Never miss a connection.</span>
                </h2>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                    {/* Card 1: Never Repeat Yourself */}
                    <div className="bg-[#FAF7F2] rounded-[2.5rem] p-10 md:p-12 flex flex-col items-center text-center relative overflow-hidden group border border-delphi-brown/5 hover:shadow-xl hover:shadow-delphi-brown/5 transition-all duration-500">
                        <div className="relative z-10">
                            <h3 className="text-2xl font-serif font-bold text-delphi-brown mb-4">Scale Your Expertise</h3>
                            <p className="text-delphi-brown/70 leading-relaxed">
                                Your Digital Twin learns from your past answers to handle repetitive questions instantly. Clone your best self for every interaction.
                            </p>
                        </div>
                        {/* Subtle pulsing animation behind */}
                        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-orange-500/5 rounded-full blur-3xl group-hover:bg-orange-500/10 transition-colors duration-500 animate-pulse-slow" />
                    </div>

                    {/* Card 2: Keep Relationships Alive */}
                    <div className="bg-[#FAF7F2] rounded-[2.5rem] p-10 md:p-12 flex flex-col items-center text-center relative overflow-hidden border border-delphi-brown/5 hover:shadow-xl hover:shadow-delphi-brown/5 transition-all duration-500">
                        <h3 className="text-2xl font-serif font-bold text-delphi-brown mb-4">Deepen Audience Connections</h3>
                        <p className="text-delphi-brown/70 mb-8 leading-relaxed max-w-md">
                            Engage with every follower personally. Your AI remembers context, ensuring no meaningful interaction gets lost in the noise.
                        </p>

                        {/* Floating Chat UI */}
                        <div className="w-full max-w-sm bg-white rounded-2xl p-4 shadow-sm border border-delphi-brown/5 relative mt-auto">
                            <div className="flex flex-col gap-3">
                                <motion.div
                                    initial={{ opacity: 0, x: -10 }}
                                    whileInView={{ opacity: 1, x: 0 }}
                                    transition={{ delay: 0.2 }}
                                    className="flex items-center gap-3 p-2 rounded-lg bg-delphi-cream/50"
                                >
                                    <div className="w-8 h-8 rounded-full bg-delphi-brown/10 flex items-center justify-center">
                                        <User className="w-4 h-4 text-delphi-brown/60" />
                                    </div>
                                    <div className="flex-1">
                                        <div className="h-2 w-24 bg-delphi-brown/10 rounded-full mb-1" />
                                        <div className="h-2 w-16 bg-delphi-brown/5 rounded-full" />
                                    </div>
                                    <span className="text-xs text-orange-500 font-bold bg-orange-50 px-2 py-1 rounded-full">{'>'}50 chats</span>
                                </motion.div>
                                <motion.div
                                    initial={{ opacity: 0, y: 10 }}
                                    whileInView={{ opacity: 1, y: 0 }}
                                    transition={{ delay: 0.4 }}
                                    className="flex items-center gap-2 text-xs font-bold text-delphi-brown/40 pl-2"
                                >
                                    <div className="w-4 h-4 rounded-full border border-delphi-brown/20 flex items-center justify-center">+</div>
                                    Add Action
                                </motion.div>
                            </div>
                        </div>
                    </div>

                    {/* Card 3: Future-Proof (Full Width Orbit) */}
                    <div className="md:col-span-2 bg-[#FAF7F2] rounded-[2.5rem] p-10 md:p-16 relative overflow-hidden border border-delphi-brown/5 hover:shadow-xl hover:shadow-delphi-brown/5 transition-all duration-500 min-h-[500px] flex flex-col items-center justify-center text-center">
                        <div className="relative z-10 max-w-2xl mb-12">
                            <h3 className="text-3xl font-serif font-bold text-delphi-brown mb-4">Future-Proof Your Knowledge Base</h3>
                            <p className="text-delphi-brown/70 leading-relaxed">
                                Connect your entire digital footprint. From Slack discussions to Substack newsletters, turn scattered data into a cohesive, interactive mind.
                            </p>
                        </div>

                        {/* Orbit Animation Container - Horizon Style */}
                        <div className="absolute bottom-[-450px] left-1/2 -translate-x-1/2 w-[900px] h-[900px] pointer-events-none">
                            {/* Orbits */}
                            <div className="absolute inset-0 rounded-full border border-delphi-brown/5 opacity-50" />
                            <div className="absolute inset-[180px] rounded-full border border-delphi-brown/5 opacity-50" />
                            <div className="absolute inset-[360px] rounded-full border border-delphi-brown/5 opacity-50" />

                            {/* Central Avatar - Large & Bottom Centered */}
                            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 rounded-full bg-gradient-to-br from-orange-400 to-red-600 p-1.5 shadow-2xl shadow-orange-500/30 z-20">
                                <div className="w-full h-full rounded-full overflow-hidden relative bg-delphi-brown">
                                    <img
                                        src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?fit=crop&w=400&h=400"
                                        alt="Digital Mind"
                                        className="w-full h-full object-cover opacity-90 hover:scale-110 transition-transform duration-700"
                                    />
                                </div>
                            </div>

                            {/* Orbiting Items - Outer Ring (Radius ~450px) */}
                            <div className="absolute inset-0 animate-spin-slow">
                                {/* Top Center (relative to ring) */}
                                <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-5">
                                    <div className="flex items-center gap-2 bg-white px-5 py-2.5 rounded-full shadow-lg border border-delphi-brown/5 -rotate-90 md:rotate-0 transition-all">
                                        <div className="w-5 h-5 bg-[#5865F2] rounded-full flex items-center justify-center p-1">
                                            <svg viewBox="0 0 24 24" fill="white" className="w-3 h-3"><path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037 3.934 3.934 0 0 0-.338.719 18.29 18.29 0 0 0-4.893 0 3.93 3.93 0 0 0-.338-.719.074.074 0 0 0-.079-.037 19.736 19.736 0 0 0-4.885 1.515.069.069 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.08.08 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028 14.09 14.09 0 0 0 1.226-1.994.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.118.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.086 2.176 2.419 0 1.334-.966 2.419-2.176 2.419zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.086 2.176 2.419 0 1.334-.966 2.419-2.176 2.419z" /></svg>
                                        </div>
                                        <span className="text-sm font-medium text-delphi-brown/80">Discord</span>
                                    </div>
                                </div>
                            </div>

                            {/* Orbiting Items - Middle Ring (Radius ~270px) */}
                            <div className="absolute inset-[180px] animate-spin-reverse-slow">
                                {/* Left Side */}
                                <div className="absolute top-[40%] left-0 -translate-x-1/2">
                                    <div className="flex items-center gap-2 bg-white px-5 py-2.5 rounded-full shadow-lg border border-delphi-brown/5 rotate-90 md:rotate-0 transition-all">
                                        <div className="w-5 h-5 bg-[#4A154B] rounded-full flex items-center justify-center p-1">
                                            <svg viewBox="0 0 24 24" fill="white" className="w-3 h-3"><path d="M5.042 15.165a2.528 2.528 0 0 1-2.52 2.523A2.528 2.528 0 0 1 0 15.165a2.527 2.527 0 0 1 2.522-2.52h2.52v2.52zM6.313 15.165a2.527 2.527 0 0 1 2.521-2.52 2.527 2.527 0 0 1 2.521 2.52v6.316a2.528 2.528 0 0 1-2.521 2.521 2.528 2.528 0 0 1-2.521-2.521v-6.316zm8.852 1.255a2.528 2.528 0 0 1 2.521-2.521h6.313a2.528 2.528 0 0 1 2.521 2.521 2.528 2.528 0 0 1-2.521 2.521h-6.313a2.528 2.528 0 0 1-2.521-2.521zm0-1.275a2.528 2.528 0 0 1 2.521-2.521 2.527 2.527 0 0 1 2.521 2.52h2.52v6.316a2.527 2.527 0 0 1-2.52 2.52 2.528 2.528 0 0 1-2.522-2.52V15.145zm-5.697 0a2.528 2.528 0 0 1 2.521 2.521v6.316a2.528 2.528 0 0 1-2.521 2.521 2.527 2.527 0 0 1-2.521-2.521v-6.316a2.527 2.527 0 0 1 2.521-2.52zm0-8.85a2.528 2.528 0 0 1 2.521-2.522h6.316a2.527 2.527 0 0 1 2.521 2.522 2.528 2.528 0 0 1-2.521 2.521h-6.316a2.528 2.528 0 0 1-2.521-2.521zm0 1.272a2.528 2.528 0 0 1-2.521 2.521 2.527 2.527 0 0 1-2.52-2.521V1.27A2.528 2.528 0 0 1 6.311-1.252a2.527 2.527 0 0 1 2.521 2.52v6.316h2.636z" /></svg>
                                        </div>
                                        <span className="text-sm font-medium text-delphi-brown/80">Slack</span>
                                    </div>
                                </div>
                                {/* Right Side */}
                                <div className="absolute top-[40%] right-0 translate-x-1/2">
                                    <div className="flex items-center gap-2 bg-white px-5 py-2.5 rounded-full shadow-lg border border-delphi-brown/5 -rotate-90 md:rotate-0 transition-all">
                                        <div className="w-5 h-5 bg-[#FF6719] rounded-full flex items-center justify-center p-1">
                                            <FileText className="w-3 h-3 text-white" />
                                        </div>
                                        <span className="text-sm font-medium text-delphi-brown/80">Substack</span>
                                    </div>
                                </div>
                            </div>

                            {/* Orbiting Items - Inner Ring (Radius ~90px) */}
                            <div className="absolute inset-[360px] animate-spin-slow">
                                <div className="absolute bottom-[20%] left-[15%]">
                                    <div className="flex items-center gap-2 bg-white px-5 py-2.5 rounded-full shadow-lg border border-delphi-brown/5 rotate-45 md:rotate-0 transition-all">
                                        <MessageSquare className="w-4 h-4 text-delphi-brown/40" />
                                        <span className="text-sm font-medium text-delphi-brown/80">Messages</span>
                                    </div>
                                </div>
                                <div className="absolute bottom-[20%] right-[15%]">
                                    <div className="flex items-center gap-2 bg-white px-5 py-2.5 rounded-full shadow-lg border border-delphi-brown/5 -rotate-45 md:rotate-0 transition-all">
                                        <Mic className="w-4 h-4 text-delphi-brown/40" />
                                        <span className="text-sm font-medium text-delphi-brown/80">Notes</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        {/* Gradient Fade at bottom to blend orbit */}
                        <div className="absolute bottom-0 left-0 right-0 h-40 bg-gradient-to-t from-[#FAF7F2] via-[#FAF7F2]/80 to-transparent z-10" />
                    </div>

                    {/* Card 4: Catch Signals */}
                    <div className="bg-[#FAF7F2] rounded-[2.5rem] p-10 md:p-12 flex flex-col items-center text-center relative overflow-hidden border border-delphi-brown/5 hover:shadow-xl hover:shadow-delphi-brown/5 transition-all duration-500">
                        <h3 className="text-2xl font-serif font-bold text-delphi-brown mb-4">Actionable Audience Insights</h3>
                        <p className="text-delphi-brown/70 leading-relaxed max-w-xs mx-auto mb-8">
                            Understand what your audience truly wants. Detect emerging topics and sentiment trends from thousands of conversations.
                        </p>

                        <div className="mt-auto relative w-full flex flex-col items-center gap-6">
                            <div className="flex -space-x-4">
                                {[1, 2, 3].map((i) => (
                                    <div key={i} className={`w-14 h-14 rounded-full border-4 border-[#FAF7F2] bg-delphi-brown/10 flex items-center justify-center relative z-${i}0 shadow-lg`}>
                                        <User className="w-6 h-6 text-delphi-brown/40" />
                                    </div>
                                ))}
                            </div>
                            {/* Floating Insight Card - Relative positioning to avoid overlap */}
                            <motion.div
                                animate={{ y: [0, -5, 0] }}
                                transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                                className="bg-white p-4 rounded-xl shadow-lg border border-delphi-brown/5 text-left w-64 relative z-10"
                            >
                                <div className="flex items-center gap-2 mb-2 text-xs font-bold text-delphi-brown/40 uppercase">
                                    <Zap className="w-3 h-3" /> Insight
                                </div>
                                <p className="text-xs text-delphi-brown/80 leading-snug">
                                    Increased interest around your <span className="text-orange-500 font-bold">relationship advice</span> from paid subscribers.
                                </p>
                            </motion.div>
                        </div>
                    </div>

                    {/* Card 5: Link in Bio */}
                    <div className="bg-[#FAF7F2] rounded-[2.5rem] p-10 md:p-12 flex flex-col items-center text-center relative overflow-hidden border border-delphi-brown/5 hover:shadow-xl hover:shadow-delphi-brown/5 transition-all duration-500">
                        <h3 className="text-2xl font-serif font-bold text-delphi-brown mb-4">Monetize Your Mind. 24/7.</h3>
                        <p className="text-delphi-brown/70 leading-relaxed max-w-sm mx-auto mb-auto">
                            Turn passive traffic into active revenue. Offer exclusive AI-gated content, paid consultations, or premium knowledge access directly.
                        </p>

                        <div className="mt-8 relative w-full flex justify-center">
                            <div className="w-64 bg-white/50 backdrop-blur-sm rounded-2xl p-4 border border-delphi-brown/5 relative">
                                {/* Connector Line */}
                                <div className="absolute -top-8 left-1/2 -translate-x-1/2 w-px h-8 bg-delphi-brown/10 border-l border-dashed border-delphi-brown/30" />
                                <div className="absolute -top-2 left-1/2 -translate-x-1/2 w-4 h-4 text-delphi-brown/20">⌘</div>

                                <div className="text-left mb-3">
                                    <div className="text-xs font-bold text-delphi-brown/40">Brian Halligan <span className="font-normal opacity-50">Author</span></div>
                                </div>

                                <div className="flex items-center justify-between bg-white rounded-xl p-3 shadow-sm border border-delphi-brown/5">
                                    <div className="text-xs text-delphi-brown/80 font-medium">
                                        Access exclusive <br /> knowledge
                                    </div>
                                    <button className="bg-[#FAF7F2] text-orange-500 text-xs font-bold px-3 py-1.5 rounded-lg border border-orange-500/10">
                                        $15/m Subscribe
                                    </button>
                                </div>

                                <motion.div
                                    initial={{ opacity: 0, y: 10 }}
                                    whileInView={{ opacity: 1, y: 0 }}
                                    transition={{ delay: 0.5 }}
                                    className="mt-2 text-[10px] text-center text-orange-500 bg-orange-50 py-1 rounded-lg"
                                >
                                    You received $15.00 from John S.
                                </motion.div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </section>
    );
};

export default BentoGridDelphi;
