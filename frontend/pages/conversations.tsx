import React, { useState, useEffect, useRef } from "react";
import Head from "next/head";
import LayoutCreative from "../components/LayoutCreative";
import { motion, AnimatePresence } from "framer-motion";
import {
  MessageSquare,
  Send,
  Search,
  MoreVertical,
  User,
  Clock,
  CheckCircle,
  AlertCircle,
  Mail,
  MessageCircle,
  Globe,
  RefreshCw,
  Paperclip,
  Smile,
  Zap,
  Phone,
  Video,
  ChevronLeft,
  Check
} from "lucide-react";

interface Conversation {
  id: string;
  customer_id: string | number;
  channel: string;
  status: string;
  created_at: string;
  customer_name?: string;
  last_message?: string;
  unread_count?: number;
  [key: string]: any;
}

interface Message {
  id?: string;
  content: string;
  direction: "incoming" | "outgoing";
  timestamp: string;
  sender?: string;
  [key: string]: any;
}

const ConversationsPage: React.FC = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [activeFilter, setActiveFilter] = useState<string>("all");
  const [newMessage, setNewMessage] = useState<string>("");
  const [isTyping, setIsTyping] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchConversations();
    const interval = setInterval(fetchConversations, 10000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const fetchConversations = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/conversations");
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data: Conversation[] = await response.json();

      const enhancedData = data.map((conv) => ({
        ...conv,
        customer_name: `Customer #${String(conv.customer_id).slice(0, 8)}`,
        last_message: "Looking forward to hearing from you!",
        unread_count: Math.floor(Math.random() * 2), // Mock unread for demo
      }));

      setConversations(enhancedData);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching conversations:", error);
      setLoading(false);
    }
  };

  const fetchMessages = async (conversationId: string) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/messages/${conversationId}`);
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data: Message[] = await response.json();

      const enhancedMessages: Message[] = data.length > 0 ? data : [
        {
          id: "1",
          content: "Hello! I need help with my account status.",
          direction: "incoming",
          timestamp: new Date(Date.now() - 3600000).toISOString(),
          sender: "Customer",
        },
        {
          id: "2",
          content: "Hi there! I'd be happy to help. Can you provide your account ID?",
          direction: "outgoing",
          timestamp: new Date(Date.now() - 3540000).toISOString(),
          sender: "Support Agent",
        },
      ];

      setMessages(enhancedMessages);
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  };

  const handleConversationClick = (conversation: Conversation) => {
    setSelectedConversation(conversation);
    fetchMessages(conversation.id);
  };

  const sendMessage = () => {
    if (newMessage.trim()) {
      const message: Message = {
        id: Date.now().toString(),
        content: newMessage,
        direction: "outgoing",
        timestamp: new Date().toISOString(),
        sender: "Support Agent",
      };

      setMessages((prev) => [...prev, message]);
      setNewMessage("");

      // Simulate generic reply
      setTimeout(() => {
        setIsTyping(true);
        setTimeout(() => {
          setIsTyping(false);
          const reply: Message = {
            id: (Date.now() + 1).toString(),
            content: "Thank you for the update.",
            direction: "incoming",
            timestamp: new Date().toISOString(),
            sender: "Customer",
          };
          setMessages((prev) => [...prev, reply]);
        }, 1500);
      }, 1000);
    }
  };

  const getChannelIcon = (channel: string) => {
    switch (channel.toLowerCase()) {
      case "gmail":
      case "email": return <Mail className="w-4 h-4" />;
      case "whatsapp": return <MessageCircle className="w-4 h-4" />;
      case "web_form": return <Globe className="w-4 h-4" />;
      default: return <MessageSquare className="w-4 h-4" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "open": return "bg-green-100 text-green-700";
      case "closed": return "bg-gray-100 text-gray-600";
      case "pending": return "bg-orange-100 text-orange-700";
      default: return "bg-blue-100 text-blue-700";
    }
  };

  const filters = [
    { id: "all", label: "All" },
    { id: "open", label: "Open" },
    { id: "unread", label: "Unread" },
  ];

  const filteredConversations = conversations.filter(c => {
    if (activeFilter === 'open') return c.status === 'open';
    if (activeFilter === 'unread') return c.unread_count && c.unread_count > 0;
    return true;
  }).filter(c =>
    c.customer_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    c.id.includes(searchQuery)
  );

  return (
    <LayoutCreative>
      <Head>
        <title>Conversations | Abdullah's Digital Twin</title>
      </Head>

      <div className="h-[calc(100vh-140px)] flex flex-col lg:flex-row gap-6 items-stretch">

        {/* Sidebar List - Floating Glass Panel */}
        <div className={`
            lg:w-[400px] flex-shrink-0 flex flex-col gap-4
            ${selectedConversation ? 'hidden lg:flex' : 'flex w-full'}
        `}>
          {/* Header Card */}
          <div className="bg-white/40 backdrop-blur-xl rounded-[2rem] p-6 border border-[#3E2407]/5 shadow-2xl shadow-[#3E2407]/5 flex flex-col gap-4">
            <div className="flex justify-between items-center">
              <h1 className="text-3xl font-serif text-[#3E2407]">
                Inbox <span className="text-[#F97316] text-lg font-sans font-bold align-top ml-1">{conversations.length}</span>
              </h1>
              <div className="flex items-center gap-2">
                <button onClick={fetchConversations} className="p-2 bg-white/50 rounded-full hover:bg-white transition-all text-[#3E2407]/60 hover:text-[#F97316]">
                  <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                </button>
              </div>
            </div>

            {/* Custom Search Input */}
            <div className="relative group">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <Search className="h-4 w-4 text-[#3E2407]/40 group-focus-within:text-[#F97316] transition-colors" />
              </div>
              <input
                type="text"
                className="block w-full pl-10 pr-4 py-3 bg-white/60 border border-transparent rounded-xl text-sm placeholder-[#3E2407]/30 text-[#3E2407] focus:outline-none focus:bg-white focus:ring-2 focus:ring-[#F97316]/20 transition-all"
                placeholder="Search threads..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>

            {/* Filter Pills */}
            <div className="flex gap-2">
              {filters.map(f => (
                <button
                  key={f.id}
                  onClick={() => setActiveFilter(f.id)}
                  className={`
                            px-4 py-2 rounded-full text-xs font-bold uppercase tracking-wider transition-all border
                            ${activeFilter === f.id
                      ? 'bg-[#3E2407] text-[#FDF6EE] border-[#3E2407]'
                      : 'bg-white/40 text-[#3E2407]/60 border-transparent hover:bg-white hover:border-[#3E2407]/10'}
                        `}
                >
                  {f.label}
                </button>
              ))}
            </div>
          </div>

          {/* Conversation List */}
          <div className="flex-1 overflow-y-auto pr-2 space-y-3 custom-scrollbar">
            <AnimatePresence>
              {filteredConversations.map((conv, i) => (
                <motion.div
                  key={conv.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.05 }}
                  onClick={() => handleConversationClick(conv)}
                  className={`
                                group p-4 rounded-2xl cursor-pointer border transition-all duration-300 relative overflow-hidden
                                ${selectedConversation?.id === conv.id
                      ? 'bg-white border-[#F97316]/30 shadow-lg shadow-[#F97316]/10'
                      : 'bg-white/40 border-transparent hover:bg-white/80 hover:shadow-md hover:translate-x-1'}
                            `}
                >
                  {selectedConversation?.id === conv.id && (
                    <motion.div
                      layoutId="active-pill"
                      className="absolute left-0 top-0 bottom-0 w-1 bg-[#F97316]"
                    />
                  )}

                  <div className="flex justify-between items-start mb-2 pl-2">
                    <div className="flex items-center gap-3">
                      <div className={`
                                        w-10 h-10 rounded-full flex items-center justify-center text-[#3E2407] transition-colors
                                        ${selectedConversation?.id === conv.id ? 'bg-[#F97316]/10 text-[#F97316]' : 'bg-[#FDF6EE]'}
                                    `}>
                        {getChannelIcon(conv.channel)}
                      </div>
                      <div>
                        <div className="font-bold text-[#3E2407] text-sm group-hover:text-[#F97316] transition-colors">
                          {conv.customer_name}
                        </div>
                        <div className="text-[10px] text-[#3E2407]/40 font-medium uppercase tracking-wider">
                          {new Date(conv.created_at).toLocaleDateString()} • {new Date(conv.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </div>
                      </div>
                    </div>
                    {conv.unread_count && conv.unread_count > 0 && (
                      <div className="w-2 h-2 rounded-full bg-[#F97316] mt-2" />
                    )}
                  </div>
                  <p className="text-xs text-[#3E2407]/60 line-clamp-2 pl-[3.5rem] leading-relaxed">
                    {conv.last_message || "No messages yet..."}
                  </p>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </div>

        {/* Chat Window - Floating Glass Panel */}
        <div className={`
            flex-1 bg-white/60 backdrop-blur-2xl rounded-[2.5rem] border border-[#3E2407]/5 shadow-2xl shadow-[#3E2407]/10 flex flex-col overflow-hidden relative
            ${selectedConversation ? 'flex' : 'hidden lg:flex'}
        `}>
          {selectedConversation ? (
            <>
              {/* Chat Header */}
              <div className="px-8 py-5 border-b border-[#3E2407]/5 flex justify-between items-center bg-white/40 backdrop-blur-md z-10">
                <div className="flex items-center gap-4">
                  <button
                    onClick={() => setSelectedConversation(null)}
                    className="lg:hidden p-2 -ml-2 hover:bg-[#3E2407]/5 rounded-full"
                  >
                    <ChevronLeft className="w-5 h-5 text-[#3E2407]" />
                  </button>
                  <div className="relative">
                    <div className="w-12 h-12 rounded-full bg-[#3E2407] flex items-center justify-center text-[#FDF6EE] shadow-lg shadow-[#3E2407]/20">
                      <User className="w-5 h-5" />
                    </div>
                    <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-white" />
                  </div>
                  <div>
                    <h2 className="text-xl font-serif text-[#3E2407] leading-tight">{selectedConversation.customer_name}</h2>
                    <div className="flex items-center gap-2 text-xs text-[#3E2407]/50">
                      <span>Via {selectedConversation.channel}</span>
                      <span>•</span>
                      <span className={`px-2 py-0.5 rounded-full ${getStatusColor(selectedConversation.status)} text-[10px] font-bold uppercase tracking-wider`}>
                        {selectedConversation.status}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex gap-1">
                  <button className="p-3 rounded-full hover:bg-white hover:shadow-sm text-[#3E2407]/60 transition-all">
                    <Phone className="w-4 h-4" />
                  </button>
                  <button className="p-3 rounded-full hover:bg-white hover:shadow-sm text-[#3E2407]/60 transition-all">
                    <Video className="w-4 h-4" />
                  </button>
                  <div className="w-px h-8 bg-[#3E2407]/10 mx-1" />
                  <button className="p-3 rounded-full hover:bg-white hover:shadow-sm text-[#3E2407]/60 transition-all">
                    <MoreVertical className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Messages Area */}
              <div className="flex-1 overflow-y-auto p-8 space-y-6 scroll-smooth bg-gradient-to-b from-[#FDF6EE]/50 to-transparent">
                {messages.map((msg, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`flex ${msg.direction === 'incoming' ? 'justify-start' : 'justify-end'}`}
                  >
                    <div className={`flex flex-col ${msg.direction === 'incoming' ? 'items-start' : 'items-end'} max-w-[75%]`}>
                      <div className={`
                                        p-5 rounded-2xl text-sm leading-relaxed shadow-sm relative
                                        ${msg.direction === 'incoming'
                          ? 'bg-white text-[#3E2407] rounded-tl-sm border border-[#3E2407]/5'
                          : 'bg-[#3E2407] text-[#FDF6EE] rounded-tr-sm shadow-xl shadow-[#3E2407]/10'}
                                    `}>
                        {msg.content}
                      </div>
                      <span className="text-[10px] text-[#3E2407]/30 mt-1 px-1 flex items-center gap-1 font-medium">
                        {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        {msg.direction === 'outgoing' && <Check className="w-3 h-3" />}
                      </span>
                    </div>
                  </motion.div>
                ))}

                {isTyping && (
                  <div className="flex justify-start">
                    <div className="bg-white p-4 rounded-2xl rounded-tl-sm border border-[#3E2407]/5 flex gap-1 shadow-sm">
                      <div className="w-1.5 h-1.5 bg-[#3E2407]/40 rounded-full animate-bounce" />
                      <div className="w-1.5 h-1.5 bg-[#3E2407]/40 rounded-full animate-bounce delay-75" />
                      <div className="w-1.5 h-1.5 bg-[#3E2407]/40 rounded-full animate-bounce delay-150" />
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} className="h-4" />
              </div>

              {/* Input Area */}
              <div className="p-6 pt-2">
                <div className="bg-white p-2 pl-4 rounded-[2rem] border border-[#3E2407]/10 shadow-lg shadow-[#3E2407]/5 flex items-center gap-2 transition-all focus-within:ring-2 focus-within:ring-[#F97316]/20 focus-within:border-[#F97316]/30">
                  <button className="p-2 text-[#3E2407]/40 hover:text-[#F97316] transition-colors rounded-full hover:bg-[#F97316]/5">
                    <Paperclip className="w-5 h-5" />
                  </button>
                  <input
                    type="text"
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Type a message to the customer..."
                    className="flex-1 bg-transparent border-none focus:ring-0 text-[#3E2407] placeholder-[#3E2407]/30 text-sm py-2"
                  />
                  <div className="flex items-center gap-1">
                    <button className="p-2 text-[#3E2407]/40 hover:text-[#F97316] transition-colors rounded-full hover:bg-[#F97316]/5">
                      <Smile className="w-5 h-5" />
                    </button>
                    <button
                      onClick={sendMessage}
                      disabled={!newMessage.trim()}
                      className="p-3 bg-[#3E2407] text-[#FDF6EE] rounded-full hover:bg-[#F97316] transition-all disabled:opacity-50 disabled:hover:bg-[#3E2407] shadow-md shadow-[#3E2407]/20"
                    >
                      <Send className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            </>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-[#3E2407]/40">
              <div className="relative">
                <div className="w-32 h-32 bg-[#F97316]/10 rounded-full blur-3xl absolute inset-0 animate-pulse" />
                <div className="w-24 h-24 bg-white rounded-[2rem] flex items-center justify-center mb-6 shadow-xl shadow-[#3E2407]/5 border border-[#3E2407]/5 relative z-10">
                  <MessageSquare className="w-10 h-10 opacity-30 text-[#3E2407]" />
                </div>
              </div>
              <h3 className="text-3xl font-serif text-[#3E2407] mb-2">No Chat Selected</h3>
              <p className="max-w-xs text-center leading-relaxed opacity-60">
                Select a conversation from the inbox on the left to start viewing the neural logs.
              </p>
            </div>
          )}
        </div>
      </div>
    </LayoutCreative>
  );
};

export default ConversationsPage;
