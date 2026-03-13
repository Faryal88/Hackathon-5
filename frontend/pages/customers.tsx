import React, { useState, useEffect } from "react";
import Head from "next/head";
import Link from "next/link";
import Layout from "../components/Layout";
import { motion, AnimatePresence } from "framer-motion";
import {
  Users,
  Mail,
  MessageCircle,
  Globe,
  Search,
  ChevronRight,
  Clock,
  TrendingUp,
  AlertCircle,
  Eye,
  Filter,
  MoreVertical,
  Download,
  User,
  Phone,
  Package
} from "lucide-react";

interface Customer {
  id: number;
  email: string;
  name: string;
  phone?: string;
  created_at: string;
  [key: string]: any;
}

interface Conversation {
  id: number;
  customer_id: number;
  channel: string;
  status: string;
  created_at: string;
  updated_at: string;
}

const floatAnimation = {
  y: [0, -10, 0],
  transition: {
    duration: 3,
    repeat: Infinity,
    ease: "easeInOut",
  },
};

export default function Customers() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [filterChannel, setFilterChannel] = useState<string>("all");

  const fetchCustomers = async () => {
    try {
      // First, get all conversations to identify unique customers
      const convResponse = await fetch("http://127.0.0.1:8000/api/conversations");
      if (!convResponse.ok) throw new Error(`HTTP error! status: ${convResponse.status}`);
      const convData: Conversation[] = await convResponse.json();
      setConversations(convData);

      // Group conversations by customer_id to get unique customers
      const uniqueCustomerIds = Array.from(new Set(convData.map((c: Conversation) => c.customer_id)));

      // Fetch customer details for each unique customer
      const customerPromises = uniqueCustomerIds.map(async (customerId) => {
        // Get first conversation for this customer to get email
        const firstConv = convData.find(c => c.customer_id === customerId);

        if (firstConv) {
          // Get messages for this conversation to extract customer info
          try {
            const msgResponse = await fetch(`http://127.0.0.1:8000/api/messages/${firstConv.id}`);
            if (msgResponse.ok) {
              const messages = await msgResponse.json();
              if (messages.length > 0) {
                const firstMessage = messages[0];

                // Try to extract customer info from message content
                const content = firstMessage.content;

                // Extract email from content
                const emailRegex = /[\w\.-]+@[\w\.-]+\.\w+/g;
                const emailMatch = content.match(emailRegex);

                let email = `customer${customerId}@example.com`;
                let name = `Customer #${customerId}`;

                if (emailMatch) {
                  email = emailMatch[0];

                  // Try to get full customer details
                  try {
                    const customerResponse = await fetch(`http://127.0.0.1:8000/api/tickets/user?email=${email}`);
                    if (customerResponse.ok) {
                      const customerData = await customerResponse.json();
                      if (customerData.customer) {
                        name = customerData.customer.name || email.split('@')[0];
                        return {
                          id: customerData.customer.id,
                          email: customerData.customer.email,
                          name: customerData.customer.name,
                          phone: customerData.customer.phone,
                          created_at: customerData.customer.created_at || new Date().toISOString()
                        };
                      }
                    }
                  } catch (e) {
                    console.error("Error fetching customer details:", e);
                  }
                }

                return {
                  id: customerId,
                  email,
                  name,
                  created_at: firstConv.created_at
                };
              }
            }
          } catch (e) {
            console.error("Error fetching messages:", e);
          }
        }

        return {
          id: customerId,
          email: `customer${customerId}@example.com`,
          name: `Customer #${customerId}`,
          created_at: new Date().toISOString()
        };
      });

      const customerResults = await Promise.all(customerPromises);
      setCustomers(customerResults.filter(Boolean));
    } catch (error) {
      console.error("Error fetching customers:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  const getChannelIcon = (channel: string) => {
    switch (channel.toLowerCase()) {
      case "gmail":
      case "email":
        return <Mail className="w-4 h-4" />;
      case "whatsapp":
        return <MessageCircle className="w-4 h-4" />;
      default:
        return <Globe className="w-4 h-4" />;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case "open":
        return <Clock className="w-4 h-4 text-amber-400" />;
      case "resolved":
        return <TrendingUp className="w-4 h-4 text-green-400" />;
      case "escalated":
        return <AlertCircle className="w-4 h-4 text-red-400" />;
      default:
        return <Clock className="w-4 h-4" />;
    }
  };

  // Filter customers based on search term and channel
  const filteredCustomers = customers.filter(customer => {
    const matchesSearch = customer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      customer.email.toLowerCase().includes(searchTerm.toLowerCase());

    if (filterChannel === "all") return matchesSearch;

    // Find conversations for this customer
    const customerConversations = conversations.filter(c => c.customer_id === customer.id);
    const hasChannel = customerConversations.some(c => c.channel === filterChannel);

    return matchesSearch && hasChannel;
  });

  if (loading) {
    return (
      <Layout>
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500/20 to-purple-500/20 blur-3xl animate-pulse" />
            <div className="relative flex flex-col items-center">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                className="w-20 h-20 border-4 border-transparent border-t-blue-400 border-r-purple-400 rounded-full"
              />
              <div className="mt-8">
                <div className="h-2 w-48 bg-gradient-to-r from-gray-700 to-gray-600 rounded-full animate-pulse" />
                <div className="h-2 w-32 bg-gradient-to-r from-gray-700 to-gray-600 rounded-full animate-pulse mt-2" />
              </div>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  const channelFilters = [
    { id: "all", label: "All Channels", count: customers.length },
    { id: "gmail", label: "Email", count: conversations.filter(c => c.channel === "gmail").length },
    { id: "whatsapp", label: "WhatsApp", count: conversations.filter(c => c.channel === "whatsapp").length },
    { id: "web_form", label: "Web Form", count: conversations.filter(c => c.channel === "web_form").length },
  ];

  return (
    <Layout>
      <Head>
        <title>Customers | TechCorp AI Support</title>
        <meta name="description" content="Customer Management Dashboard" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
        {/* Glass header */}
        <div className="sticky top-0 z-50 backdrop-blur-xl bg-gray-900/80 border-b border-gray-700/50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  className="p-2 rounded-xl bg-gradient-to-br from-blue-500/10 to-cyan-500/10 border border-blue-500/20"
                >
                  <Users className="w-6 h-6 text-blue-400" />
                </motion.div>
                <div>
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                    Customer Directory
                  </h1>
                  <p className="text-sm text-gray-400">
                    Manage all your customers in one place
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-4">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search customers..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10 pr-4 py-2 rounded-xl bg-gray-800/50 border border-gray-700/50 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-transparent"
                  />
                </div>
                <div className="flex items-center space-x-2">
                  <div className="p-2 rounded-xl bg-gray-800/50 border border-gray-700/50">
                    <span className="text-sm text-gray-300">{customers.length} customers</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Filter Section */}
          <div className="mb-8">
            <div className="flex flex-wrap gap-2">
              {channelFilters.map((filter) => (
                <motion.button
                  key={filter.id}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setFilterChannel(filter.id)}
                  className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${filterChannel === filter.id
                    ? "bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-lg"
                    : "bg-gray-800/50 text-gray-400 hover:text-white"
                    }`}
                >
                  {filter.label} ({filter.count})
                </motion.button>
              ))}
            </div>
          </div>

          {/* Customer List */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <AnimatePresence>
              {filteredCustomers.map((customer, index) => {
                // Get conversations for this customer
                const customerConversations = conversations.filter(c => c.customer_id === customer.id);
                const lastActivity = customerConversations.length > 0
                  ? Math.max(...customerConversations.map(c => new Date(c.updated_at).getTime()))
                  : new Date(customer.created_at).getTime();

                return (
                  <motion.div
                    key={customer.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.05 }}
                    whileHover={{ y: -5 }}
                    className="group relative overflow-hidden rounded-2xl"
                  >
                    <Link href={`/customer?email=${encodeURIComponent(customer.email)}`}>
                      <div className="relative z-10 bg-gradient-to-br from-gray-800/50 to-gray-900/50 rounded-2xl p-6 border border-gray-700/50 backdrop-blur-sm hover:border-blue-500/30 transition-all cursor-pointer">
                        <div className="flex items-start justify-between mb-4">
                          <div className="flex items-center space-x-3">
                            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500/20 to-cyan-500/20 flex items-center justify-center">
                              <User className="w-6 h-6 text-blue-400" />
                            </div>
                            <div>
                              <h3 className="font-bold text-white text-lg">{customer.name}</h3>
                              <p className="text-sm text-gray-400 truncate max-w-[160px]">{customer.email}</p>
                            </div>
                          </div>
                          <ChevronRight className="w-5 h-5 text-gray-500 group-hover:text-blue-400 transition-colors" />
                        </div>

                        <div className="space-y-3">
                          <div className="flex items-center justify-between p-3 rounded-xl bg-gray-800/30 border border-gray-700/50">
                            <div className="flex items-center space-x-2">
                              <Package className="w-4 h-4 text-amber-400" />
                              <span className="text-sm text-gray-400">Plan</span>
                            </div>
                            <span className="text-sm font-medium text-white">Professional</span>
                          </div>

                          <div className="flex items-center justify-between p-3 rounded-xl bg-gray-800/30 border border-gray-700/50">
                            <div className="flex items-center space-x-2">
                              <Phone className="w-4 h-4 text-green-400" />
                              <span className="text-sm text-gray-400">Contact</span>
                            </div>
                            <span className="text-sm font-medium text-white">{customer.phone || 'N/A'}</span>
                          </div>

                          <div className="pt-3">
                            <div className="flex items-center justify-between text-sm mb-2">
                              <span className="text-gray-400">Conversations</span>
                              <span className="text-blue-400">{customerConversations.length}</span>
                            </div>
                            <div className="h-2 w-full bg-gray-700 rounded-full overflow-hidden">
                              <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${Math.min(100, (customerConversations.length / 20) * 100)}%` }}
                                className="h-full bg-gradient-to-r from-blue-500 to-cyan-500"
                              />
                            </div>
                          </div>

                          <div className="pt-3">
                            <div className="flex items-center justify-between text-sm">
                              <span className="text-gray-400">Last Activity</span>
                              <span className="text-gray-400">
                                {new Date(lastActivity).toLocaleDateString()}
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </Link>
                  </motion.div>
                );
              })}
            </AnimatePresence>
          </div>

          {filteredCustomers.length === 0 && (
            <div className="text-center py-12">
              <div className="mx-auto w-24 h-24 rounded-full bg-gray-800/50 flex items-center justify-center mb-4">
                <Users className="w-12 h-12 text-gray-500" />
              </div>
              <h3 className="text-xl font-medium text-white mb-2">No customers found</h3>
              <p className="text-gray-400">Try adjusting your search or filter criteria</p>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}