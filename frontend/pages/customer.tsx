import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowLeft,
  User,
  Mail,
  Phone,
  Calendar,
  Package,
  Shield,
  MessageSquare,
  FileText,
  Clock,
  AlertCircle,
  CheckCircle,
  XCircle,
  MoreVertical,
  Download,
  Printer,
  Edit,
  Star,
  Hash,
  Globe,
  Send,
  Paperclip,
  Smile,
  TrendingUp,
  Activity,
  Zap,
  Sparkles,
} from "lucide-react";

interface Customer {
  id: number;
  name: string;
  email: string;
  phone: string;
  joinDate: string;
  plan: string;
  status: string;
}

interface Message {
  role: "customer" | "agent";
  content: string;
  timestamp: string;
  direction?: "incoming" | "outgoing";
}

interface Conversation {
  id: number;
  subject: string;
  channel: string;
  status: string;
  priority: string;
  createdAt: string;
  updatedAt: string;
  messages: Message[];
}

interface Ticket {
  id: number;
  issue: string;
  status: string;
  priority: string;
  created_at: string;
  updated_at: string;
  conversation_channel: string;
  conversation_status: string;
  messages: Message[];
}

interface ApiResponse {
  customer: {
    id: number;
    email: string;
    name: string;
    phone?: string;
    created_at?: string;
  };
  tickets: Ticket[];
  count: number;
}

const CustomerPage: React.FC = () => {
  const [customerData, setCustomerData] = useState<Customer | null>(null);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [activeTab, setActiveTab] = useState<string>("conversations");
  const [newMessage, setNewMessage] = useState<string>("");

  useEffect(() => {
    const fetchCustomerData = async () => {
      // Get customer email from URL query parameter or use a default
      // Use window.location.search for browser environments or a default for SSR
      let email = 'salah0shah2@gmail.com'; // default
      if (typeof window !== 'undefined' && window.location && window.location.search) {
        const urlParams = new URLSearchParams(window.location.search);
        const paramEmail = urlParams.get('email');
        if (paramEmail) {
          email = paramEmail;
        }
      }
      try {
        setLoading(true);

        // Fetch customer data from backend API - use relative path to avoid CORS issues
        console.log('Fetching customer data for email:', email); // Debug log
        const response = await fetch(`/api/tickets/user?email=${encodeURIComponent(email)}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
        });
        console.log('Response status:', response.status); // Debug log

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result: ApiResponse = await response.json();
        console.log('API result:', result); // Debug log

        if (result && result.customer) {
          const customer = result.customer;
          console.log('Customer data found:', customer); // Debug log

          // Transform customer data to match expected format
          const transformedCustomer = {
            id: customer.id,
            name: customer.name || customer.email.split('@')[0],
            email: customer.email,
            phone: customer.phone || 'N/A',
            joinDate: customer.created_at || new Date().toISOString(),
            plan: 'Professional', // Could be retrieved from a customer record if available
            status: 'Active', // Could be retrieved from a customer record if available
          };

          console.log('Setting customer data:', transformedCustomer); // Debug log
          setCustomerData(transformedCustomer);

          // Transform conversations and messages
          const transformedConversations = result.tickets?.map((ticket: Ticket) => ({
            id: ticket.id,
            subject: ticket.issue.substring(0, 30) + (ticket.issue.length > 30 ? '...' : ''),
            channel: ticket.conversation_channel || 'web_form',
            status: ticket.status,
            priority: ticket.priority,
            createdAt: ticket.created_at,
            updatedAt: ticket.updated_at,
            messages: ticket.messages?.map((msg: Message) => ({
              role: (msg.direction === 'incoming' ? 'customer' : 'agent') as "customer" | "agent",
              content: msg.content,
              timestamp: msg.timestamp,
            })) || [],
          })) || [];

          console.log('Setting conversations:', transformedConversations); // Debug log
          setConversations(transformedConversations);
        } else {
          console.error('No customer data found in API response');
          console.log('API response:', result); // Debug log
          // Set a default customer if API doesn't return expected data
          setCustomerData({
            id: 1,
            name: "Unknown Customer",
            email: email,
            phone: 'N/A',
            joinDate: new Date().toISOString(),
            plan: "Professional",
            status: "Active",
          });
        }
      } catch (error) {
        console.error('Error fetching customer data:', error);
        console.error('Failed to fetch data for email:', email);
        // Fallback to a default customer if API call fails
        setCustomerData({
          id: 1,
          name: "Default Customer",
          email: email,
          phone: "N/A",
          joinDate: new Date().toISOString(),
          plan: "Professional",
          status: "Active",
        });
        setConversations([]);
      } finally {
        setLoading(false);
      }
    };

    fetchCustomerData();
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case "active":
        return <CheckCircle className="w-4 h-4" />;
      case "pending":
        return <Clock className="w-4 h-4" />;
      case "suspended":
        return <XCircle className="w-4 h-4" />;
      default:
        return <Activity className="w-4 h-4" />;
    }
  };

  const getPriorityIcon = (priority: string) => {
    switch (priority.toLowerCase()) {
      case "high":
        return <AlertCircle className="w-4 h-4 text-red-400" />;
      case "medium":
        return <Clock className="w-4 h-4 text-amber-400" />;
      case "low":
        return <Shield className="w-4 h-4 text-green-400" />;
      default:
        return <Activity className="w-4 h-4" />;
    }
  };

  const tabs = [
    {
      id: "conversations",
      label: "Conversations",
      icon: <MessageSquare className="w-5 h-5" />,
    },
    { id: "tickets", label: "Tickets", icon: <FileText className="w-5 h-5" /> },
    {
      id: "activity",
      label: "Activity",
      icon: <Activity className="w-5 h-5" />,
    },
    {
      id: "documents",
      label: "Documents",
      icon: <Paperclip className="w-5 h-5" />,
    },
  ];

  const sendMessage = () => {
    if (newMessage.trim()) {
      const newMsg: Message = {
        role: "agent",
        content: newMessage,
        timestamp: new Date().toISOString(),
      };

      const updatedConversations = [...conversations];
      if (updatedConversations.length > 0) {
        updatedConversations[0].messages.push(newMsg);
        setConversations(updatedConversations);
      }
      setNewMessage("");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center">
        <div className="relative">
          <div className="absolute inset-0 bg-gradient-to-r from-green-500/20 to-emerald-500/20 blur-3xl animate-pulse" />
          <div className="relative flex flex-col items-center">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
              className="w-20 h-20 border-4 border-transparent border-t-green-400 border-r-emerald-400 rounded-full"
            />
            <div className="mt-8">
              <div className="h-2 w-48 bg-gradient-to-r from-gray-700 to-gray-600 rounded-full animate-pulse" />
              <div className="h-2 w-32 bg-gradient-to-r from-gray-700 to-gray-600 rounded-full animate-pulse mt-2" />
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      {/* Glass Header */}
      <motion.header
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="sticky top-0 z-50 backdrop-blur-xl bg-gray-900/80 border-b border-green-500/30"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => window.history.back()}
                className="p-2 rounded-xl bg-gradient-to-br from-green-500/10 to-emerald-500/10 border border-green-500/20 hover:border-green-400/30 transition-all"
              >
                <ArrowLeft className="w-5 h-5 text-green-400" />
              </motion.button>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent">
                  Customer Profile
                </h1>
                <p className="text-sm text-gray-400">
                  Premium support management
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 rounded-xl bg-gray-800/50 hover:bg-gray-700/50 border border-green-500/20 transition-all"
              >
                <Printer className="w-5 h-5 text-gray-400" />
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="p-2 rounded-xl bg-gray-800/50 hover:bg-gray-700/50 border border-green-500/20 transition-all"
              >
                <Download className="w-5 h-5 text-gray-400" />
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-gradient-to-r from-green-500 to-emerald-500 text-white hover:shadow-lg transition-all"
              >
                <Edit className="w-4 h-4" />
                <span>Edit Profile</span>
              </motion.button>
            </div>
          </div>
        </div>
      </motion.header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Customer Profile */}
          <div className="lg:col-span-1 space-y-6">
            {/* Customer Card */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-gradient-to-br from-gray-800/50 to-gray-900/50 rounded-2xl p-6 border border-green-500/30 backdrop-blur-sm"
            >
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-4">
                  <motion.div whileHover={{ scale: 1.1 }} className="relative">
                    <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-green-500 to-emerald-500 p-0.5">
                      <div className="w-full h-full rounded-2xl bg-gray-900 flex items-center justify-center">
                        <User className="w-10 h-10 text-green-400" />
                      </div>
                    </div>
                    <div className="absolute -bottom-2 -right-2 w-8 h-8 rounded-full bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center">
                      <Sparkles className="w-4 h-4 text-white" />
                    </div>
                  </motion.div>
                  <div>
                    <h2 className="text-xl font-bold text-white">
                      {customerData?.name || 'Loading...'}
                    </h2>
                    <p className="text-sm text-gray-400">
                      {customerData?.email || 'Loading...'}
                    </p>
                  </div>
                </div>
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  className="p-2 rounded-xl bg-gray-800/50 hover:bg-gray-700/50 cursor-pointer"
                >
                  <MoreVertical className="w-5 h-5 text-gray-400" />
                </motion.div>
              </div>

              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 rounded-xl bg-gray-800/30 border border-green-500/20">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 rounded-lg bg-green-500/10">
                      <Hash className="w-4 h-4 text-green-400" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-400">Customer ID</p>
                      <p className="font-medium text-white">
                        {customerData ? `CUST-${customerData.id.toString().padStart(5, "0")}` : 'Loading...'}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-between p-3 rounded-xl bg-gray-800/30 border border-green-500/20">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 rounded-lg bg-green-500/10">
                      <Package className="w-4 h-4 text-green-400" />
                    </div>
                    <div>
                      <p className="text-sm text-gray-400">Plan</p>
                      <p className="font-medium text-white">
                        {customerData?.plan || 'Loading...'}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    {customerData ? getStatusIcon(customerData.status) : <Activity className="w-4 h-4" />}
                    <span className="text-sm text-green-400">
                      {customerData?.status || 'Loading...'}
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="p-3 rounded-xl bg-gray-800/30 border border-green-500/20">
                    <div className="flex items-center space-x-3">
                      <div className="p-2 rounded-lg bg-green-500/10">
                        <Phone className="w-4 h-4 text-green-400" />
                      </div>
                      <div>
                        <p className="text-sm text-gray-400">Phone</p>
                        <p className="font-medium text-white">
                          {customerData?.phone || 'N/A'}
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="p-3 rounded-xl bg-gray-800/30 border border-green-500/20">
                    <div className="flex items-center space-x-3">
                      <div className="p-2 rounded-lg bg-green-500/10">
                        <Calendar className="w-4 h-4 text-green-400" />
                      </div>
                      <div>
                        <p className="text-sm text-gray-400">Member Since</p>
                        <p className="font-medium text-white">
                          {customerData ? new Date(customerData.joinDate).toLocaleDateString(
                            "en-US",
                            {
                              month: "short",
                              year: "numeric",
                            }
                          ) : 'Loading...'}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-6 pt-6 border-t border-green-500/30">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-400">Customer Rating</p>
                    <div className="flex items-center space-x-1 mt-1">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <Star
                          key={star}
                          className="w-4 h-4 text-yellow-400 fill-current"
                        />
                      ))}
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-400">Support Score</p>
                    <p className="text-2xl font-bold text-green-400">94%</p>
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Quick Stats */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-gradient-to-br from-green-900/20 to-emerald-900/20 rounded-2xl p-6 border border-green-500/30 backdrop-blur-sm"
            >
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-bold text-white">Customer Stats</h3>
                <TrendingUp className="w-5 h-5 text-green-400" />
              </div>

              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-400">Tickets</span>
                    <span className="text-green-400">{conversations.length}</span>
                  </div>
                  <div className="h-2 w-full bg-gray-700 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${Math.min(100, (conversations.length / 30) * 100)}%` }}
                      className="h-full bg-gradient-to-r from-green-500 to-emerald-400"
                    />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-400">Avg Response Time</span>
                    <span className="text-green-400">{conversations.length > 0 ? '2.4m' : 'N/A'}</span>
                  </div>
                  <div className="h-2 w-full bg-gray-700 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${conversations.length > 0 ? "65%" : "30%"}` }}
                      className="h-full bg-gradient-to-r from-blue-500 to-cyan-400"
                    />
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-400">Satisfaction</span>
                    <span className="text-green-400">{conversations.length > 0 ? '96%' : 'N/A'}</span>
                  </div>
                  <div className="h-2 w-full bg-gray-700 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${conversations.length > 0 ? "96%" : "50%"}` }}
                      className="h-full bg-gradient-to-r from-purple-500 to-pink-400"
                    />
                  </div>
                </div>
              </div>
            </motion.div>
          </div>

          {/* Right Column - Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Tabs */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex space-x-2 bg-gray-800/30 rounded-2xl p-2 border border-green-500/20"
            >
              {tabs.map((tab) => (
                <motion.button
                  key={tab.id}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 px-4 py-3 rounded-xl text-sm font-medium transition-all ${activeTab === tab.id
                    ? "bg-gradient-to-r from-green-500 to-emerald-500 text-white shadow-lg"
                    : "text-gray-400 hover:text-white hover:bg-gray-700/50"
                    }`}
                >
                  {tab.icon}
                  <span>{tab.label}</span>
                </motion.button>
              ))}
            </motion.div>

            {/* Conversations */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="space-y-6"
            >
              <AnimatePresence>
                {conversations.map((conversation, index) => (
                  <motion.div
                    key={conversation.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    whileHover={{ y: -2 }}
                    className="bg-gradient-to-br from-gray-800/50 to-gray-900/50 rounded-2xl p-6 border border-green-500/30 backdrop-blur-sm"
                  >
                    <div className="flex items-center justify-between mb-6">
                      <div>
                        <div className="flex items-center space-x-3 mb-2">
                          <h3 className="text-lg font-bold text-white">
                            {conversation.subject}
                          </h3>
                          <div className="flex items-center space-x-2">
                            <span className="px-3 py-1 text-xs rounded-full bg-gray-700/50 text-green-400 border border-green-500/30">
                              {conversation.channel}
                            </span>
                            <span className="flex items-center space-x-1 px-3 py-1 text-xs rounded-full bg-gray-700/50 text-white border border-green-500/30">
                              {getPriorityIcon(conversation.priority)}
                              <span>{conversation.priority}</span>
                            </span>
                          </div>
                        </div>
                        <p className="text-sm text-gray-400">
                          {new Date(conversation.createdAt).toLocaleString()}
                        </p>
                      </div>
                      <span className="px-3 py-1 text-sm rounded-full bg-green-500/10 text-green-400 border border-green-500/30">
                        {conversation.status}
                      </span>
                    </div>

                    {/* Messages */}
                    <div className="space-y-4">
                      <AnimatePresence>
                        {conversation.messages.map((message, msgIndex) => (
                          <motion.div
                            key={msgIndex}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: msgIndex * 0.05 }}
                            className={`flex ${message.role === "customer"
                              ? "justify-start"
                              : "justify-end"
                              }`}
                          >
                            <div
                              className={`max-w-2xl rounded-2xl p-4 ${message.role === "customer"
                                ? "bg-gray-800/50 border border-green-500/30"
                                : "bg-gradient-to-r from-green-500/20 to-emerald-500/20 border border-green-500/50"
                                }`}
                            >
                              <div className="flex items-center space-x-2 mb-2">
                                <div
                                  className={`w-6 h-6 rounded-full flex items-center justify-center ${message.role === "customer"
                                    ? "bg-green-500/20 text-green-400"
                                    : "bg-emerald-500/20 text-emerald-400"
                                    }`}
                                >
                                  {message.role === "customer" ? (
                                    <User className="w-3 h-3" />
                                  ) : (
                                    <Shield className="w-3 h-3" />
                                  )}
                                </div>
                                <span className="text-xs text-gray-400">
                                  {message.role === "customer"
                                    ? "Customer"
                                    : "Support Agent"}
                                </span>
                                <span className="text-xs text-gray-500">
                                  {new Date(
                                    message.timestamp
                                  ).toLocaleTimeString([], {
                                    hour: "2-digit",
                                    minute: "2-digit",
                                  })}
                                </span>
                              </div>
                              <p className="text-gray-300">{message.content}</p>
                            </div>
                          </motion.div>
                        ))}
                      </AnimatePresence>
                    </div>

                    {/* Reply Input */}
                    <div className="mt-6 pt-6 border-t border-green-500/30">
                      <div className="flex items-center space-x-3">
                        <div className="flex-1 relative">
                          <input
                            type="text"
                            value={newMessage}
                            onChange={(e) => setNewMessage(e.target.value)}
                            placeholder="Type your reply..."
                            className="w-full px-4 py-3 rounded-xl bg-gray-800/50 border border-green-500/30 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-green-500/50 focus:border-transparent"
                            onKeyPress={(e) =>
                              e.key === "Enter" && sendMessage()
                            }
                          />
                          <div className="absolute right-3 top-3 flex items-center space-x-2">
                            <button className="p-1 hover:text-green-400 transition-colors">
                              <Paperclip className="w-4 h-4" />
                            </button>
                            <button className="p-1 hover:text-green-400 transition-colors">
                              <Smile className="w-4 h-4" />
                            </button>
                          </div>
                        </div>
                        <motion.button
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                          onClick={sendMessage}
                          className="p-3 rounded-xl bg-gradient-to-r from-green-500 to-emerald-500 hover:shadow-lg transition-all"
                        >
                          <Send className="w-5 h-5 text-white" />
                        </motion.button>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CustomerPage;
