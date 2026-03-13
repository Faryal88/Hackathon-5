import React from 'react';
import { motion } from 'framer-motion';
import { Twitter, Instagram, Linkedin, Github, Send, ArrowRight } from 'lucide-react';
import Link from 'next/link';

const FooterCreative = () => {
    return (
        <footer className="relative bg-[#2A1705] text-delphi-cream pt-24 pb-12 overflow-hidden">
            {/* Background Texture */}
            <div className="absolute inset-0 opacity-[0.03]"
                style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23F7F0E8' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")` }}
            />

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">

                {/* Pre-Footer CTA */}
                <div className="mb-20 grid md:grid-cols-2 gap-12 items-end border-b border-delphi-cream/10 pb-20">
                    <div>
                        <h2 className="text-5xl md:text-7xl font-serif mb-6 leading-[0.9]">
                            Ready to clone<br />
                            <span className="italic text-orange-400">yourself?</span>
                        </h2>
                        <p className="text-delphi-cream/60 max-w-md text-lg">
                            Join the waitlist for the world's first extensive digital twin engine.
                        </p>
                    </div>
                    <div className="flex flex-col gap-4">
                        <div className="relative group">
                            <input
                                type="email"
                                placeholder="Enter your email"
                                className="w-full bg-white/5 border border-delphi-cream/20 rounded-full py-4 px-6 text-delphi-cream placeholder:text-delphi-cream/30 focus:outline-none focus:border-orange-400/50 transition-colors"
                            />
                            <button className="absolute right-2 top-2 bottom-2 bg-orange-500 hover:bg-orange-600 text-white px-6 rounded-full transition-colors flex items-center justify-center">
                                <ArrowRight className="w-5 h-5" />
                            </button>
                        </div>
                    </div>
                </div>

                {/* Main Footer Content */}
                <div className="grid grid-cols-2 md:grid-cols-12 gap-12 mb-20">

                    {/* Brand Column */}
                    <div className="col-span-2 md:col-span-4 lg:col-span-5">
                        <Link href="/" className="inline-block mb-6 group">
                            <span className="font-serif text-4xl text-delphi-cream tracking-tight group-hover:text-orange-400 transition-colors">Abdullah.</span>
                        </Link>
                        <p className="text-delphi-cream/50 max-w-xs mb-8">
                            The interface to your digital mind. Turn your knowledge into an infinite, interactive presence.
                        </p>
                        <div className="flex gap-4">
                            {[
                                { icon: Twitter, href: "#" },
                                { icon: Github, href: "#" },
                                { icon: Linkedin, href: "#" }
                            ].map((social, i) => (
                                <a key={i} href={social.href} className="w-10 h-10 rounded-full border border-delphi-cream/10 flex items-center justify-center text-delphi-cream/60 hover:bg-delphi-cream hover:text-delphi-brown transition-all">
                                    <social.icon className="w-4 h-4" />
                                </a>
                            ))}
                        </div>
                    </div>

                    {/* Links Columns */}
                    <div className="col-span-1 md:col-span-2 lg:col-span-2">
                        <h4 className="font-serif text-lg mb-6 text-delphi-cream">Product</h4>
                        <ul className="space-y-4 text-delphi-cream/60">
                            {['Features', 'Pricing', 'API', 'Integrations'].map(item => (
                                <li key={item}>
                                    <Link href="#" className="hover:text-orange-400 transition-colors">{item}</Link>
                                </li>
                            ))}
                        </ul>
                    </div>

                    <div className="col-span-1 md:col-span-3 lg:col-span-2">
                        <h4 className="font-serif text-lg mb-6 text-delphi-cream">Company</h4>
                        <ul className="space-y-4 text-delphi-cream/60">
                            {['About Us', 'Careers', 'Blog', 'Contact'].map(item => (
                                <li key={item}>
                                    <Link href="#" className="hover:text-orange-400 transition-colors">{item}</Link>
                                </li>
                            ))}
                        </ul>
                    </div>
                    <div className="col-span-1 md:col-span-3 lg:col-span-3">
                        <h4 className="font-serif text-lg mb-6 text-delphi-cream">Legal</h4>
                        <ul className="space-y-4 text-delphi-cream/60">
                            {['Privacy Policy', 'Terms of Service', 'Cookie Policy'].map(item => (
                                <li key={item}>
                                    <Link href="#" className="hover:text-orange-400 transition-colors">{item}</Link>
                                </li>
                            ))}
                        </ul>
                    </div>

                </div>

            </div>
        </footer>
    );
};

export default FooterCreative;
