import React, { useState } from "react";
import Head from "next/head";
import LayoutCreative from "../components/LayoutCreative";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search,
  Ticket,
  Mail,
  User,
  Clock,
  AlertCircle,
  CheckCircle,
  XCircle,
  MessageSquare,
  ChevronRight,
  ChevronDown,
  RefreshCw,
  Sparkles,
  Zap,
  ArrowRight,
  Filter
} from "lucide-react";

interface Customer {
  id: string;
  name: string;
  email: string;
  [key: string]: any;
}

interface Message {
  direction: string;
  content: string;
  timestamp: string;
  [key: string]: any;
}

interface Ticket {
  id: string;
  issue: string;
  status: string;
  priority: string;
  conversation_channel: string;
  created_at: string;
  messages?: Message[];
  [key: string]: any;
}

interface TicketResults {
  customer?: Customer;
  tickets: Ticket[];
  [key: string]: any;
}

export default function CheckTicket() {
  const [email, setEmail] = useState<string>("");
  const [ticketResults, setTicketResults] = useState<TicketResults | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const [expandedTicket, setExpandedTicket] = useState<string | null>(null);

  const handleCheckTickets = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setTicketResults(null);
    setExpandedTicket(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/tickets/user?email=${encodeURIComponent(email)}`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data: TicketResults = await response.json();
      setTicketResults(data);
    } catch (err: any) {
      setError(err.message || "Network error. Please try again.");
      console.error("Error checking tickets:", err);
    } finally {
      setLoading(false);
    }
  };

  const toggleExpandTicket = (ticketId: string) => {
    setExpandedTicket(expandedTicket === ticketId ? null : ticketId);
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "open": return "bg-blue-100 text-blue-700 border-blue-200";
      case "in_progress": return "bg-amber-100 text-amber-700 border-amber-200";
      case "resolved": return "bg-green-100 text-green-700 border-green-200";
      case "closed": return "bg-gray-100 text-gray-600 border-gray-200";
      default: return "bg-gray-100 text-gray-600 border-gray-200";
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case "urgent": return "text-red-500 font-bold";
      case "high": return "text-orange-500 font-bold";
      case "medium": return "text-amber-600";
      default: return "text-gray-400";
    }
  };

  return (
    <LayoutCreative>
      <Head>
        <title>Track Tickets | Abdullah's Digital Twin</title>
        <meta name="description" content="Track your support tickets in real-time" />
      </Head>

      <div className="max-w-6xl mx-auto px-4">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/40 border border-[#3E2407]/5 mb-6 text-sm font-bold uppercase tracking-widest text-[#F97316]">
            <Sparkles className="w-4 h-4" />
            <span>Neural Log Access</span>
          </div>
          <h1 className="text-5xl md:text-7xl font-serif text-[#3E2407] mb-6">
            Ticket <span className="opacity-40">Tracking</span>
          </h1>
          <p className="text-[#3E2407]/60 text-lg max-w-xl mx-auto leading-relaxed">
            Enter your email to retrieve your conversation history and ticket status from the digital twin's memory.
          </p>
        </motion.div>

        {/* Floating Search Capsule */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="max-w-xl mx-auto mb-20 relative z-20"
        >
          <div className="bg-white p-2 pl-6 rounded-[2rem] border border-[#3E2407]/10 shadow-xl shadow-[#3E2407]/5 flex items-center gap-4 transition-all focus-within:ring-4 focus-within:ring-[#F97316]/10 focus-within:border-[#F97316]/30">
            <Search className="w-5 h-5 text-[#3E2407]/40" />
            <form onSubmit={handleCheckTickets} className="flex-1 flex items-center">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email address..."
                className="w-full bg-transparent border-none focus:ring-0 text-[#3E2407] placeholder-[#3E2407]/30 text-lg"
                required
              />
              <button
                type="submit"
                disabled={loading || !email}
                className="px-6 py-3 bg-[#3E2407] text-[#FDF6EE] rounded-[1.5rem] font-bold uppercase tracking-wider text-xs hover:bg-[#F97316] transition-all disabled:opacity-50 disabled:hover:bg-[#3E2407] shadow-lg shadow-[#3E2407]/20 flex items-center gap-2"
              >
                {loading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <span>Search</span>}
              </button>
            </form>
          </div>
        </motion.div>

        {/* Error State */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mb-8 max-w-xl mx-auto"
            >
              <div className="bg-red-50/80 backdrop-blur-md border border-red-100 rounded-2xl p-4 flex items-center gap-3 text-red-600 shadow-lg shadow-red-500/5">
                <AlertCircle className="w-5 h-5 flex-shrink-0" />
                <p className="font-medium">{error}</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Results Stream */}
        <AnimatePresence>
          {ticketResults && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="space-y-12"
            >
              {/* Customer Header */}
              {ticketResults.customer && (
                <div className="flex flex-col md:flex-row items-center justify-between gap-6 bg-white/40 backdrop-blur-xl rounded-[2.5rem] p-8 border border-[#3E2407]/5">
                  <div className="flex items-center gap-6">
                    <div className="relative">
                      <div className="w-20 h-20 rounded-full bg-[#3E2407] flex items-center justify-center text-[#FDF6EE] text-2xl font-serif">
                        {ticketResults.customer.name.charAt(0)}
                      </div>
                      <div className="absolute -bottom-1 -right-1 w-6 h-6 bg-green-500 rounded-full border-4 border-white" />
                    </div>
                    <div>
                      <h2 className="text-3xl font-serif text-[#3E2407]">{ticketResults.customer.name}</h2>
                      <div className="flex items-center gap-2 text-[#3E2407]/60 mt-1">
                        <Mail className="w-4 h-4" />
                        <span className="font-mono text-sm">{ticketResults.customer.email}</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex gap-4">
                    <div className="bg-white/50 px-6 py-4 rounded-2xl border border-[#3E2407]/5 text-center min-w-[120px]">
                      <div className="text-xs font-bold uppercase tracking-widest text-[#3E2407]/40 mb-1">Total</div>
                      <div className="text-3xl font-serif text-[#3E2407]">{ticketResults.tickets.length}</div>
                    </div>
                    <div className="bg-[#F97316]/10 px-6 py-4 rounded-2xl border border-[#F97316]/10 text-center min-w-[120px]">
                      <div className="text-xs font-bold uppercase tracking-widest text-[#F97316] mb-1">Active</div>
                      <div className="text-3xl font-serif text-[#F97316]">
                        {ticketResults.tickets.filter(t => t.status !== 'closed').length}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Masonry Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {ticketResults.tickets.length > 0 ? (
                  ticketResults.tickets.map((ticket, index) => (
                    <motion.div
                      key={ticket.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className={`
                          bg-white/80 backdrop-blur-lg rounded-[2.5rem] p-8 border border-[#3E2407]/5 hover:shadow-2xl hover:shadow-[#3E2407]/10 transition-all duration-300 group
                          ${expandedTicket === ticket.id ? 'md:col-span-2 bg-white' : ''}
                      `}
                    >
                      <div className="flex justify-between items-start mb-6">
                        <div className="flex gap-2">
                          <span className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest border ${getStatusColor(ticket.status)}`}>
                            {ticket.status.replace('_', ' ')}
                          </span>
                          <span className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest border border-transparent bg-[#3E2407]/5 text-[#3E2407]/60 ${getPriorityColor(ticket.priority)}`}>
                            {ticket.priority}
                          </span>
                        </div>
                        <button
                          onClick={() => toggleExpandTicket(ticket.id)}
                          className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${expandedTicket === ticket.id ? 'bg-[#3E2407] text-[#FDF6EE]' : 'bg-[#3E2407]/5 text-[#3E2407]/40 hover:bg-[#F97316] hover:text-white'}`}
                        >
                          {expandedTicket === ticket.id ? <ChevronDown className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
                        </button>
                      </div>

                      <h3 className="text-2xl font-bold text-[#3E2407] mb-4 leading-tight group-hover:text-[#F97316] transition-colors">
                        {ticket.issue}
                      </h3>

                      <div className="flex items-center gap-4 text-xs text-[#3E2407]/40 font-medium uppercase tracking-wider mb-6">
                        <span className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          {new Date(ticket.created_at).toLocaleDateString()}
                        </span>
                        <span className="w-1 h-1 rounded-full bg-[#3E2407]/20" />
                        <span className="flex items-center gap-1">
                          <MessageSquare className="w-4 h-4" />
                          {ticket.conversation_channel}
                        </span>
                      </div>

                      {/* Expanded Content */}
                      <AnimatePresence>
                        {expandedTicket === ticket.id && (
                          <motion.div
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: 'auto', opacity: 1 }}
                            exit={{ height: 0, opacity: 0 }}
                            className="border-t border-[#3E2407]/10 pt-6"
                          >
                            <h4 className="font-serif text-lg text-[#3E2407] mb-4 flex items-center gap-2">
                              <Sparkles className="w-4 h-4 text-[#F97316]" />
                              Neural History
                            </h4>

                            {ticket.messages && ticket.messages.length > 0 ? (
                              <div className="space-y-4 max-h-[400px] overflow-y-auto custom-scrollbar pr-2">
                                {ticket.messages.map((msg, idx) => (
                                  <div
                                    key={idx}
                                    className={`flex ${msg.direction === 'incoming' ? 'justify-end' : 'justify-start'}`}
                                  >
                                    <div className={`
                                        max-w-[85%] p-5 rounded-2xl text-sm leading-relaxed
                                        ${msg.direction === 'incoming'
                                        ? 'bg-[#3E2407] text-[#FDF6EE] rounded-tr-sm shadow-xl shadow-[#3E2407]/10'
                                        : 'bg-white border border-[#3E2407]/10 text-[#3E2407] rounded-tl-sm'}
                                      `}>
                                      <p>{msg.content}</p>
                                      <div className={`text-[10px] mt-2 opacity-50 ${msg.direction === 'incoming' ? 'text-right' : 'text-left'}`}>
                                        {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                      </div>
                                    </div>
                                  </div>
                                ))}
                              </div>
                            ) : (
                              <div className="p-8 text-center bg-[#FDF6EE]/50 rounded-2xl border border-[#3E2407]/5 border-dashed">
                                <p className="text-[#3E2407]/40 italic text-sm">No messages recorded in neural logs.</p>
                              </div>
                            )}
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </motion.div>
                  ))
                ) : (
                  <div className="col-span-full py-20 text-center">
                    <div className="w-24 h-24 bg-white/40 rounded-full flex items-center justify-center mx-auto mb-6 shadow-xl shadow-[#3E2407]/5">
                      <Ticket className="w-10 h-10 text-[#3E2407]/20" />
                    </div>
                    <h3 className="text-2xl font-serif text-[#3E2407] mb-2">No Tickets Found</h3>
                    <p className="text-[#3E2407]/60">We searched the neural network but found no records for this email.</p>
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </LayoutCreative>
  );
}
