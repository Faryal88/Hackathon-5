import React, { useState } from 'react';
import Head from 'next/head';
import Layout from '../components/Layout';
import { motion, AnimatePresence } from 'framer-motion';
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
  Download,
  Printer,
  Filter,
  RefreshCw,
  Sparkles,
  Zap,
  Shield,
  TrendingUp,
  Eye,
  Copy
} from 'lucide-react';

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
  const [email, setEmail] = useState<string>('');
  const [ticketResults, setTicketResults] = useState<TicketResults | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [expandedTicket, setExpandedTicket] = useState<string | null>(null);
  const [copied, setCopied] = useState<boolean>(false);

  const handleCheckTickets = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setTicketResults(null);
    setExpandedTicket(null);

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/tickets/user?email=${encodeURIComponent(email)}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data: TicketResults = await response.json();
      setTicketResults(data);
    } catch (err: any) {
      setError(err.message || 'Network error. Please try again.');
      console.error('Error checking tickets:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleExpandTicket = (ticketId: string) => {
    setExpandedTicket(expandedTicket === ticketId ? null : ticketId);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'open': return <AlertCircle className="w-4 h-4" />;
      case 'in_progress': return <Clock className="w-4 h-4" />;
      case 'resolved': return <CheckCircle className="w-4 h-4" />;
      case 'closed': return <XCircle className="w-4 h-4" />;
      default: return <Ticket className="w-4 h-4" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'open': return 'text-blue-400 bg-blue-500/10 border-blue-500/20';
      case 'in_progress': return 'text-amber-400 bg-amber-500/10 border-amber-500/20';
      case 'resolved': return 'text-green-400 bg-green-500/10 border-green-500/20';
      case 'closed': return 'text-purple-400 bg-purple-500/10 border-purple-500/20';
      default: return 'text-gray-400 bg-gray-500/10 border-gray-500/20';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'urgent': return 'text-red-400 bg-red-500/10 border-red-500/20';
      case 'high': return 'text-orange-400 bg-orange-500/10 border-orange-500/20';
      case 'medium': return 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20';
      case 'low': return 'text-gray-400 bg-gray-500/10 border-gray-500/20';
      default: return 'text-gray-400 bg-gray-500/10 border-gray-500/20';
    }
  };

  return (
    <Layout>
      <Head>
        <title>Track Tickets | TechCorp AI Support</title>
        <meta name="description" content="Track your support tickets in real-time" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-12"
          >
            <div className="inline-block mb-4">
              <motion.div
                whileHover={{ scale: 1.1 }}
                className="p-3 rounded-2xl bg-gradient-to-br from-blue-500/10 to-cyan-500/10 border border-blue-500/20"
              >
                <Ticket className="w-8 h-8 text-blue-400" />
              </motion.div>
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent mb-3">
              Track Your Tickets
            </h1>
            <p className="text-lg text-gray-400 max-w-2xl mx-auto">
              Enter your email to check real-time status of all your support requests
            </p>
          </motion.div>

          {/* Search Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-gradient-to-br from-gray-800/50 to-gray-900/50 rounded-2xl p-8 border border-blue-500/30 backdrop-blur-sm mb-8"
          >
            <div className="max-w-xl mx-auto">
              <form onSubmit={handleCheckTickets}>
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-300 mb-3">
                    <div className="flex items-center space-x-2">
                      <Mail className="w-4 h-4" />
                      <span>Enter your registered email address</span>
                    </div>
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <Mail className="h-5 w-5 text-gray-500" />
                    </div>
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="john@example.com"
                      className="w-full pl-10 pr-4 py-3 rounded-xl bg-gray-800/30 border border-blue-500/30 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent"
                      required
                    />
                    <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                      <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => copyToClipboard(email)}
                        className="p-1 hover:text-blue-400 transition-colors"
                      >
                        <Copy className="w-4 h-4" />
                      </motion.button>
                    </div>
                  </div>
                  {copied && (
                    <motion.p
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="text-xs text-green-400 mt-2"
                    >
                      Email copied to clipboard!
                    </motion.p>
                  )}
                </div>
                <div className="flex items-center justify-between">
                  <motion.button
                    type="button"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setEmail('')}
                    className="px-4 py-2 rounded-xl bg-gray-800/50 text-gray-400 hover:text-white transition-colors"
                  >
                    Clear
                  </motion.button>
                  <motion.button
                    type="submit"
                    disabled={loading || !email}
                    whileHover={{ scale: loading || !email ? 1 : 1.05 }}
                    whileTap={{ scale: loading || !email ? 1 : 0.95 }}
                    className={`flex items-center space-x-2 px-6 py-3 rounded-xl transition-all ${
                      loading || !email
                        ? 'bg-gray-700/50 cursor-not-allowed'
                        : 'bg-gradient-to-r from-blue-500 to-cyan-500 hover:shadow-lg'
                    }`}
                  >
                    {loading ? (
                      <>
                        <RefreshCw className="w-5 h-5 animate-spin" />
                        <span>Searching...</span>
                      </>
                    ) : (
                      <>
                        <Search className="w-5 h-5" />
                        <span>Track Tickets</span>
                        <Sparkles className="w-4 h-4" />
                      </>
                    )}
                  </motion.button>
                </div>
              </form>
            </div>
          </motion.div>

          {/* Error State */}
          <AnimatePresence>
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="mb-8"
              >
                <div className="bg-gradient-to-br from-red-900/20 to-red-800/20 rounded-2xl p-6 border border-red-500/30 backdrop-blur-sm">
                  <div className="flex items-center space-x-3">
                    <AlertCircle className="w-6 h-6 text-red-400" />
                    <div>
                      <h3 className="font-medium text-white">Error occurred</h3>
                      <p className="text-red-300 text-sm">{error}</p>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Results */}
          <AnimatePresence>
            {ticketResults && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 20 }}
                className="space-y-6"
              >
                {/* Customer Info */}
                {ticketResults.customer && (
                  <motion.div
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="bg-gradient-to-br from-gray-800/50 to-gray-900/50 rounded-2xl p-6 border border-blue-500/30 backdrop-blur-sm"
                  >
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-4">
                        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500/20 to-cyan-500/20 flex items-center justify-center">
                          <User className="w-6 h-6 text-blue-400" />
                        </div>
                        <div>
                          <h2 className="text-xl font-bold text-white">{ticketResults.customer.name}</h2>
                          <p className="text-gray-400">{ticketResults.customer.email}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm text-gray-400">Total Tickets</div>
                        <div className="text-2xl font-bold text-blue-400">
                          {ticketResults.tickets.length}
                        </div>
                      </div>
                    </div>
                  </motion.div>
                )}

                {/* Tickets Grid */}
                {ticketResults.tickets.length > 0 ? (
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {ticketResults.tickets.map((ticket, index) => (
                      <motion.div
                        key={ticket.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                        whileHover={{ y: -2 }}
                        className={`bg-gradient-to-br from-gray-800/50 to-gray-900/50 rounded-2xl border border-blue-500/30 backdrop-blur-sm overflow-hidden ${
                          expandedTicket === ticket.id ? 'lg:col-span-2' : ''
                        }`}
                      >
                        {/* Ticket Header */}
                        <div className="p-6">
                          <div className="flex items-start justify-between mb-4">
                            <div>
                              <div className="flex items-center space-x-3 mb-2">
                                <div className="p-2 rounded-lg bg-blue-500/10">
                                  <Ticket className="w-5 h-5 text-blue-400" />
                                </div>
                                <div>
                                  <h3 className="font-bold text-white">Ticket #{ticket.id}</h3>
                                  <p className="text-sm text-gray-400">
                                    Created {new Date(ticket.created_at).toLocaleDateString()}
                                  </p>
                                </div>
                              </div>
                              <p className="text-gray-300">{ticket.issue}</p>
                            </div>
                            <div className="flex items-center space-x-2">
                              <span className={`inline-flex items-center space-x-1 px-3 py-1.5 text-sm rounded-full border ${getStatusColor(ticket.status)}`}>
                                {getStatusIcon(ticket.status)}
                                <span className="capitalize">{ticket.status.replace('_', ' ')}</span>
                              </span>
                              <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={() => toggleExpandTicket(ticket.id)}
                                className="p-2 rounded-lg hover:bg-gray-700/50 transition-colors"
                              >
                                <ChevronRight className={`w-4 h-4 text-gray-400 transition-transform ${
                                  expandedTicket === ticket.id ? 'rotate-90' : ''
                                }`} />
                              </motion.button>
                            </div>
                          </div>

                          {/* Quick Info */}
                          <div className="flex items-center space-x-4 text-sm">
                            <div className="flex items-center space-x-2">
                              <div className={`px-2 py-1 rounded-lg ${getPriorityColor(ticket.priority)}`}>
                                {ticket.priority.toUpperCase()}
                              </div>
                            </div>
                            <div className="flex items-center space-x-2 text-gray-400">
                              <MessageSquare className="w-4 h-4" />
                              <span>{ticket.conversation_channel}</span>
                            </div>
                            <div className="flex items-center space-x-2 text-gray-400">
                              <Clock className="w-4 h-4" />
                              <span>
                                {new Date(ticket.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                              </span>
                            </div>
                          </div>
                        </div>

                        {/* Expanded Messages */}
                        <AnimatePresence>
                          {expandedTicket === ticket.id && ticket.messages && ticket.messages.length > 0 && (
                            <motion.div
                              initial={{ opacity: 0, height: 0 }}
                              animate={{ opacity: 1, height: 'auto' }}
                              exit={{ opacity: 0, height: 0 }}
                              className="border-t border-blue-500/30"
                            >
                              <div className="p-6">
                                <div className="flex items-center justify-between mb-4">
                                  <h4 className="font-semibold text-white">Recent Updates</h4>
                                  <div className="flex items-center space-x-2">
                                    <motion.button
                                      whileHover={{ scale: 1.05 }}
                                      whileTap={{ scale: 0.95 }}
                                      className="p-2 rounded-lg hover:bg-gray-700/50 transition-colors"
                                    >
                                      <Printer className="w-4 h-4 text-gray-400" />
                                    </motion.button>
                                    <motion.button
                                      whileHover={{ scale: 1.05 }}
                                      whileTap={{ scale: 0.95 }}
                                      className="p-2 rounded-lg hover:bg-gray-700/50 transition-colors"
                                    >
                                      <Download className="w-4 h-4 text-gray-400" />
                                    </motion.button>
                                  </div>
                                </div>

                                <div className="space-y-3">
                                  {ticket.messages.slice(-5).map((msg, idx) => (
                                    <motion.div
                                      key={idx}
                                      initial={{ opacity: 0, x: -20 }}
                                      animate={{ opacity: 1, x: 0 }}
                                      transition={{ delay: idx * 0.05 }}
                                      className={`p-4 rounded-xl ${
                                        msg.direction === 'incoming'
                                          ? 'bg-gray-800/50 border border-blue-500/30'
                                          : 'bg-gradient-to-r from-blue-500/20 to-cyan-500/20 border border-blue-500/50'
                                      }`}
                                    >
                                      <div className="flex items-center justify-between mb-2">
                                        <div className="flex items-center space-x-2">
                                          <span className="text-sm font-medium text-gray-300 capitalize">
                                            {msg.direction === 'incoming' ? 'You' : 'Support Agent'}
                                          </span>
                                          <div className="w-1 h-1 rounded-full bg-gray-500" />
                                          <span className="text-xs text-gray-500">
                                            {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                          </span>
                                        </div>
                                      </div>
                                      <p className="text-gray-300">{msg.content}</p>
                                    </motion.div>
                                  ))}
                                </div>
                              </div>
                            </motion.div>
                          )}
                        </AnimatePresence>
                      </motion.div>
                    ))}
                  </div>
                ) : (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="text-center py-16"
                  >
                    <div className="w-20 h-20 mx-auto mb-6 rounded-2xl bg-gradient-to-br from-blue-500/20 to-cyan-500/20 border border-blue-500/30 flex items-center justify-center">
                      <Ticket className="w-10 h-10 text-blue-400" />
                    </div>
                    <h3 className="text-2xl font-bold text-white mb-3">No Tickets Found</h3>
                    <p className="text-gray-400 max-w-md mx-auto mb-8">
                      We couldn't find any support tickets associated with this email address.
                      Submit a new ticket to get started with our support.
                    </p>
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={() => window.location.href = '/'}
                      className="inline-flex items-center space-x-2 px-6 py-3 rounded-xl bg-gradient-to-r from-blue-500 to-cyan-500 text-white hover:shadow-lg transition-all"
                    >
                      <Zap className="w-5 h-5" />
                      <span>Submit New Ticket</span>
                    </motion.button>
                  </motion.div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </Layout>
  );
}