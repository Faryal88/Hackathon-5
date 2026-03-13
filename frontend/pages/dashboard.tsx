import React, { useState, useEffect } from "react";
import Head from "next/head";
import Link from "next/link";
import LayoutCreative from "../components/LayoutCreative";
import { motion } from "framer-motion";
import {
  Ticket,
  MessageSquare,
  AlertCircle,
  Zap,
  ArrowUpRight,
  TrendingDown,
  Globe,
  Mail,
  ChevronRight,
  RefreshCw,
  Clock,
  CheckCircle2,
  Users,
  Activity,
  BarChart3,
  PieChart,
  Layers
} from "lucide-react";

interface DashboardStats {
  total_tickets: number;
  active_conversations: number;
  escalations: number;
  avg_response_time: number;
}

interface Conversation {
  id: string;
  customer_id: string | number;
  channel: string;
  status: string;
  created_at: string;
  customer_name?: string;
  customer_email?: string;
  [key: string]: any;
}

// Custom SVG Chart Component: Sparkline
const Sparkline = ({ data, color = "#F97316" }: { data: number[], color?: string }) => {
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;
  const points = data.map((val, i) => {
    const x = (i / (data.length - 1)) * 100;
    const y = 100 - ((val - min) / range) * 100;
    return `${x},${y}`;
  }).join(" ");

  return (
    <div className="w-full h-12 overflow-hidden">
      <svg viewBox="0 0 100 100" preserveAspectRatio="none" className="w-full h-full overflow-visible">
        <polyline
          fill="none"
          stroke={color}
          strokeWidth="2"
          points={points}
          vectorEffect="non-scaling-stroke"
        />
        <defs>
          <linearGradient id={`gradient-${color}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={color} stopOpacity="0.2" />
            <stop offset="100%" stopColor={color} stopOpacity="0" />
          </linearGradient>
        </defs>
        <polygon
          points={`0,100 ${points} 100,100`}
          fill={`url(#gradient-${color})`}
        />
      </svg>
    </div>
  );
};

// Custom SVG Chart Component: Progress Ring
const ProgressRing = ({ progress, size = 40, stroke = 4, color = "#F97316" }: { progress: number, size?: number, stroke?: number, color?: string }) => {
  const radius = size / 2 - stroke * 2;
  const circumference = radius * 2 * Math.PI;
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  return (
    <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
      <svg className="transform -rotate-90 w-full h-full">
        <circle
          stroke={color}
          strokeWidth={stroke}
          fill="transparent"
          r={radius}
          cx={size / 2}
          cy={size / 2}
          opacity={0.2}
        />
        <circle
          stroke={color}
          strokeWidth={stroke}
          fill="transparent"
          r={radius}
          cx={size / 2}
          cy={size / 2}
          strokeDasharray={circumference + ' ' + circumference}
          style={{ strokeDashoffset }}
          strokeLinecap="round"
        />
      </svg>
      <div className="absolute text-[10px] font-bold text-[#3E2407]">{progress}%</div>
    </div>
  );
};

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats>({
    total_tickets: 0,
    active_conversations: 0,
    escalations: 0,
    avg_response_time: 0,
  });
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [refreshing, setRefreshing] = useState<boolean>(false);

  // Mock Data for Charts
  const chartData = [10, 25, 15, 30, 45, 20, 55, 40, 60, 50, 75, 80];
  const chartData2 = [50, 40, 60, 30, 70, 40, 50, 60, 40, 50, 45, 50];

  const fetchStats = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/dashboard/stats");
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data: DashboardStats = await response.json();
      setStats(data);
    } catch (error) {
      console.error("Error fetching stats:", error);
    }
  };

  const fetchConversations = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/conversations?limit=6");
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data: Conversation[] = await response.json();

      const enhancedConversations = await Promise.all(
        data.map(async (conv) => {
          try {
            const messageResponse = await fetch(`http://127.0.0.1:8000/api/messages/${conv.id}`);
            if (messageResponse.ok) {
              const messages = await messageResponse.json();
              if (messages.length > 0) {
                // Simple logic to get name, similar to previous version but cleaner
                let customerName = `Customer #${conv.customer_id}`;
                // We preserve the core logic but skip the deep fetch for speed/simplicity in V2 unless needed
                return { ...conv, customer_name: customerName };
              }
            }
            return { ...conv, customer_name: `Customer #${conv.customer_id}` };
          } catch (err) {
            return { ...conv, customer_name: `Customer #${conv.customer_id}` };
          }
        })
      );
      setConversations(enhancedConversations);
    } catch (error) {
      console.error("Error fetching conversations:", error);
    }
  };

  const refreshData = async () => {
    setRefreshing(true);
    await Promise.all([fetchStats(), fetchConversations()]);
    setTimeout(() => setRefreshing(false), 800);
  };

  useEffect(() => {
    const loadData = async () => {
      await Promise.all([fetchStats(), fetchConversations()]);
      setLoading(false);
    };
    loadData();
  }, []);

  const getChannelIcon = (channel: string) => {
    switch (channel.toLowerCase()) {
      case "gmail":
      case "email": return <Mail className="w-4 h-4" />;
      case "whatsapp": return <MessageSquare className="w-4 h-4" />;
      default: return <Globe className="w-4 h-4" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'open': return 'bg-green-100 text-green-700';
      case 'closed': return 'bg-gray-100 text-gray-600';
      case 'pending': return 'bg-orange-100 text-orange-700';
      case 'escalated': return 'bg-red-100 text-red-700';
      default: return 'bg-blue-100 text-blue-700';
    }
  };

  if (loading) {
    return (
      <LayoutCreative>
        <div className="h-[80vh] flex items-center justify-center">
          <div className="relative w-24 h-24">
            <div className="absolute inset-0 rounded-full border-4 border-[#3E2407]/10"></div>
            <div className="absolute inset-0 rounded-full border-4 border-t-[#F97316] animate-spin"></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <Zap className="w-8 h-8 text-[#F97316] animate-pulse" />
            </div>
          </div>
        </div>
      </LayoutCreative>
    )
  }

  return (
    <LayoutCreative>
      <Head>
        <title>Dashboard | Abdullah's Digital Twin</title>
      </Head>

      <div className="space-y-8">
        {/* Header with Stats Row */}
        <div className="flex flex-col lg:flex-row justify-between items-end gap-6">
          <div>
            <h1 className="text-4xl font-serif text-[#3E2407]">
              Command Center
            </h1>
            <p className="text-[#3E2407]/60 mt-2 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              System Operational • Last updated just now
            </p>
          </div>
          <button
            onClick={refreshData}
            disabled={refreshing}
            className="flex items-center gap-2 px-6 py-2 bg-white rounded-full text-[#3E2407] hover:shadow-lg transition-all disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
            <span className="text-sm font-bold uppercase tracking-wider">Refresh Data</span>
          </button>
        </div>

        {/* Bento Grid Layout */}
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">

          {/* Primary Stats - Large Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="md:col-span-2 lg:col-span-2 bg-[#3E2407] rounded-[2rem] p-8 text-[#FDF6EE] relative overflow-hidden group"
          >
            <div className="absolute top-0 right-0 w-64 h-64 bg-[#F97316]/20 rounded-full blur-[80px] group-hover:bg-[#F97316]/30 transition-all duration-700" />
            <div className="relative z-10">
              <div className="flex justify-between items-start mb-8">
                <div>
                  <p className="text-[#FDF6EE]/60 font-medium mb-1">Total Tickets</p>
                  <h2 className="text-6xl font-serif">{stats.total_tickets}</h2>
                </div>
                <div className="p-3 bg-[#FDF6EE]/10 rounded-2xl backdrop-blur-sm">
                  <Ticket className="w-8 h-8 text-[#F97316]" />
                </div>
              </div>
              <div className="h-24">
                <Sparkline data={chartData} color="#F97316" />
              </div>
              <div className="flex items-center gap-2 mt-4 text-[#FDF6EE]/60 text-sm">
                <ArrowUpRight className="w-4 h-4 text-green-400" />
                <span className="text-green-400 font-bold">+12.5%</span>
                from last week
              </div>
            </div>
          </motion.div>

          {/* Response Time - Medium Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white/60 backdrop-blur-xl rounded-[2rem] p-6 border border-[#3E2407]/5 shadow-xl shadow-[#3E2407]/5 flex flex-col justify-between"
          >
            <div className="flex justify-between items-start">
              <div className="p-3 bg-blue-100/50 rounded-2xl text-blue-600">
                <Zap className="w-6 h-6" />
              </div>
              <ProgressRing progress={85} color="#2563EB" />
            </div>
            <div>
              <h3 className="text-3xl font-serif text-[#3E2407] mt-4">{stats.avg_response_time.toFixed(1)}s</h3>
              <p className="text-[#3E2407]/60 text-sm font-medium">Avg Response Time</p>
            </div>
            <div className="mt-4 pt-4 border-t border-[#3E2407]/5 flex items-center justify-between text-xs text-[#3E2407]/60">
              <span>Target: 2.0s</span>
              <span className="text-green-600 font-bold">Excellent</span>
            </div>
          </motion.div>

          {/* Active Chats - Medium Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white/60 backdrop-blur-xl rounded-[2rem] p-6 border border-[#3E2407]/5 shadow-xl shadow-[#3E2407]/5 flex flex-col justify-between"
          >
            <div className="flex justify-between items-start">
              <div className="p-3 bg-purple-100/50 rounded-2xl text-purple-600">
                <MessageSquare className="w-6 h-6" />
              </div>
              <Sparkline data={chartData2} color="#9333EA" />
            </div>
            <div>
              <h3 className="text-3xl font-serif text-[#3E2407] mt-4">{stats.active_conversations}</h3>
              <p className="text-[#3E2407]/60 text-sm font-medium">Active Conversations</p>
            </div>
          </motion.div>

          {/* System Health / Escalations - Tall Card in Mobile, Split in Desktop */}
          <div className="md:col-span-1 lg:col-span-1 grid grid-rows-2 gap-6">
            {/* Escalations */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
              className={`
                        rounded-[2rem] p-6 border flex items-center justify-between
                        ${stats.escalations > 0
                  ? 'bg-red-50 border-red-100 shadow-xl shadow-red-500/10'
                  : 'bg-white/60 border-[#3E2407]/5'}
                    `}
            >
              <div>
                <p className="text-sm font-medium text-[#3E2407]/60">Escalations</p>
                <h3 className="text-3xl font-serif text-[#3E2407]">{stats.escalations}</h3>
              </div>
              <div className={`p-3 rounded-full ${stats.escalations > 0 ? 'bg-red-100 text-red-600 animate-pulse' : 'bg-green-100 text-green-600'}`}>
                <AlertCircle className="w-6 h-6" />
              </div>
            </motion.div>

            {/* Twin Core Visual */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
              className="bg-[#3E2407] rounded-[2rem] relative overflow-hidden flex items-center justify-center"
            >
              <div className="absolute inset-0 bg-[#F97316]/10" />
              <div className="relative z-10 w-16 h-16 rounded-full bg-[#FDF6EE]/10 border border-[#FDF6EE]/20 flex items-center justify-center backdrop-blur-sm">
                <Activity className="w-8 h-8 text-[#F97316] animate-pulse" />
              </div>
              <div className="absolute w-32 h-32 bg-[#F97316]/20 rounded-full animate-ping" />
            </motion.div>
          </div>

          {/* Activity Feed - Wide Bottom Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="md:col-span-3 lg:col-span-4 bg-white/40 backdrop-blur-xl rounded-[2.5rem] p-8 border border-[#3E2407]/5 shadow-2xl shadow-[#3E2407]/5"
          >
            <div className="flex justify-between items-center mb-8">
              <div className="flex items-center gap-4">
                <div className="p-3 bg-white rounded-xl shadow-sm">
                  <Layers className="w-6 h-6 text-[#3E2407]" />
                </div>
                <h3 className="text-xl font-serif text-[#3E2407]">Live Activity Feed</h3>
              </div>
              <Link href="/conversations" className="text-xs font-bold uppercase tracking-widest text-[#F97316] hover:text-[#3E2407] transition-colors">
                View All Activity
              </Link>
            </div>

            <div className="space-y-3">
              {conversations.map((conv, i) => (
                <div
                  key={conv.id}
                  className="group flex items-center justify-between p-4 bg-white/60 hover:bg-white rounded-2xl transition-all border border-transparent hover:border-[#F97316]/20 hover:shadow-lg hover:shadow-[#F97316]/5 cursor-pointer"
                >
                  <div className="flex items-center gap-4">
                    <div className="min-w-[40px] h-10 rounded-full bg-[#FDF6EE] flex items-center justify-center text-[#3E2407] border border-[#3E2407]/5">
                      {getChannelIcon(conv.channel)}
                    </div>
                    <div className="min-w-0">
                      <h4 className="font-bold text-[#3E2407] truncate">{conv.customer_name}</h4>
                      <div className="flex items-center gap-2 text-xs text-[#3E2407]/40">
                        <span>Via {conv.channel}</span>
                        <span>•</span>
                        <span>{new Date(conv.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    <span className={`hidden md:inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${getStatusColor(conv.status)}`}>
                      {conv.status}
                    </span>
                    <div className="w-8 h-8 rounded-full bg-[#3E2407]/5 flex items-center justify-center text-[#3E2407]/20 group-hover:bg-[#F97316] group-hover:text-white transition-all">
                      <ChevronRight className="w-4 h-4" />
                    </div>
                  </div>
                </div>
              ))}
              {conversations.length === 0 && (
                <div className="text-center py-12 text-[#3E2407]/30 font-medium">
                  System idle. No active conversations relative to query.
                </div>
              )}
            </div>
          </motion.div>
        </div>
      </div>
    </LayoutCreative>
  );
}
