import React, { useState } from 'react';
import { Loader2 } from 'lucide-react';

interface FormData {
    name: string;
    email: string;
    subject: string;
    category: string;
    message: string;
    priority: 'low' | 'medium' | 'high' | 'urgent';
}

interface WebSupportFormDelphiProps { }

const WebSupportFormDelphi: React.FC<WebSupportFormDelphiProps> = () => {
    const [formData, setFormData] = useState<FormData>({
        name: '',
        email: '',
        subject: '',
        category: '',
        message: '',
        priority: 'medium'
    });
    const [loading, setLoading] = useState<boolean>(false);
    const [success, setSuccess] = useState<boolean>(false);
    const [error, setError] = useState<string>('');
    const [ticketId, setTicketId] = useState<string | null>(null);

    // Categories for the dropdown
    const categories = [
        'Technical Issue',
        'Billing Question',
        'Account Management',
        'Feature Request',
        'General Inquiry',
        'Security Concern',
        'Training Request',
        'Data Export'
    ];

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            // Validate required fields
            if (!formData.name || !formData.email || !formData.subject || !formData.category || !formData.message) {
                throw new Error('All fields are required');
            }

            // Validate email format
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(formData.email)) {
                throw new Error('Please enter a valid email address');
            }

            // Submit the form - point to backend server
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
            const response = await fetch(`${apiUrl}/api/support/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (data.success) {
                setSuccess(true);
                setTicketId(data.ticket_id);
                // Reset form after successful submission
                setFormData({
                    name: '',
                    email: '',
                    subject: '',
                    category: '',
                    message: '',
                    priority: 'medium'
                });
            } else {
                throw new Error(data.message || 'Failed to submit form');
            }
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const resetForm = () => {
        setSuccess(false);
        setTicketId(null);
        setError('');
    };

    if (success) {
        return (
            <div className="w-full h-full min-h-[500px] flex flex-col items-center justify-center p-12 text-center bg-delphi-cream/30 rounded-xl">
                <h3 className="text-3xl font-serif font-medium text-delphi-brown mb-4">Request Received</h3>
                <p className="text-delphi-brown/60 mb-8 font-sans max-w-xs mx-auto">
                    We have successfully logged your inquiry. <br /> Reference ID: <span className="font-mono text-delphi-brown">{ticketId}</span>
                </p>
                <button
                    onClick={resetForm}
                    className="text-xs font-bold tracking-widest uppercase text-delphi-brown border-b border-delphi-brown/20 pb-1 hover:border-delphi-brown transition-colors"
                >
                    Start New Inquiry
                </button>
            </div>
        );
    }

    return (
        <div className="w-full p-6 md:p-8">
            <div className="flex items-end justify-between mb-12 border-b border-delphi-brown/10 pb-6">
                <h2 className="text-3xl font-serif text-delphi-brown">Console</h2>
                <div className="text-xs font-bold text-delphi-brown/30 uppercase tracking-widest">
                    System V.2.0
                </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-8">
                {error && (
                    <div className="text-red-600 text-sm bg-red-50 p-4 rounded-lg">
                        {error}
                    </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div className="group space-y-2">
                        <label htmlFor="name" className="block text-xs font-bold text-delphi-brown/40 uppercase tracking-widest group-focus-within:text-delphi-brown transition-colors">
                            Name
                        </label>
                        <input
                            type="text"
                            id="name"
                            name="name"
                            value={formData.name}
                            onChange={handleChange}
                            className="w-full bg-transparent border-b border-delphi-brown/10 py-3 text-lg text-delphi-brown focus:outline-none focus:border-delphi-brown/50 transition-colors placeholder-delphi-brown/20"
                            placeholder="Full Name"
                            required
                        />
                    </div>

                    <div className="group space-y-2">
                        <label htmlFor="email" className="block text-xs font-bold text-delphi-brown/40 uppercase tracking-widest group-focus-within:text-delphi-brown transition-colors">
                            Email
                        </label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            className="w-full bg-transparent border-b border-delphi-brown/10 py-3 text-lg text-delphi-brown focus:outline-none focus:border-delphi-brown/50 transition-colors placeholder-delphi-brown/20"
                            placeholder="Email Address"
                            required
                        />
                    </div>
                </div>

                <div className="group space-y-2">
                    <label htmlFor="subject" className="block text-xs font-bold text-delphi-brown/40 uppercase tracking-widest group-focus-within:text-delphi-brown transition-colors">
                        Subject
                    </label>
                    <input
                        type="text"
                        id="subject"
                        name="subject"
                        value={formData.subject}
                        onChange={handleChange}
                        className="w-full bg-transparent border-b border-delphi-brown/10 py-3 text-lg text-delphi-brown focus:outline-none focus:border-delphi-brown/50 transition-colors placeholder-delphi-brown/20"
                        placeholder="Inquiry Subject"
                        required
                    />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div className="group space-y-2">
                        <label htmlFor="category" className="block text-xs font-bold text-delphi-brown/40 uppercase tracking-widest group-focus-within:text-delphi-brown transition-colors">
                            Category
                        </label>
                        <div className="relative">
                            <select
                                id="category"
                                name="category"
                                value={formData.category}
                                onChange={handleChange}
                                className="w-full bg-transparent border-b border-delphi-brown/10 py-3 text-lg text-delphi-brown focus:outline-none focus:border-delphi-brown/50 transition-colors appearance-none cursor-pointer"
                                required
                            >
                                <option value="">Select...</option>
                                {categories.map((category, index) => (
                                    <option key={index} value={category}>{category}</option>
                                ))}
                            </select>
                        </div>
                    </div>

                    <div className="group space-y-2">
                        <label htmlFor="priority" className="block text-xs font-bold text-delphi-brown/40 uppercase tracking-widest group-focus-within:text-delphi-brown transition-colors">
                            Priority
                        </label>
                        <div className="relative">
                            <select
                                id="priority"
                                name="priority"
                                value={formData.priority}
                                onChange={handleChange}
                                className="w-full bg-transparent border-b border-delphi-brown/10 py-3 text-lg text-delphi-brown focus:outline-none focus:border-delphi-brown/50 transition-colors appearance-none cursor-pointer"
                            >
                                <option value="low">Low</option>
                                <option value="medium">Medium</option>
                                <option value="high">High</option>
                                <option value="urgent">Urgent</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div className="group space-y-2">
                    <label htmlFor="message" className="block text-xs font-bold text-delphi-brown/40 uppercase tracking-widest group-focus-within:text-delphi-brown transition-colors">
                        Message
                    </label>
                    <textarea
                        id="message"
                        name="message"
                        value={formData.message}
                        onChange={handleChange}
                        rows={4}
                        className="w-full bg-transparent border-b border-delphi-brown/10 py-3 text-lg text-delphi-brown focus:outline-none focus:border-delphi-brown/50 transition-colors placeholder-delphi-brown/20 resize-none"
                        placeholder="Details..."
                        required
                    ></textarea>
                </div>

                <div className="pt-4 flex justify-end">
                    <button
                        type="submit"
                        disabled={loading}
                        className="px-8 py-4 bg-delphi-brown text-white text-sm font-bold tracking-widest uppercase hover:bg-delphi-brown/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-3"
                    >
                        {loading ? (
                            <Loader2 className="w-4 h-4 animate-spin" />
                        ) : (
                            "Submit Query"
                        )}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default WebSupportFormDelphi;
