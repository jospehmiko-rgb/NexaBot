import random

class CareerTips:
    def get_tips(self):
        """Get career tips and advice."""
        tips = [
            "🎯 **Interview Success Tips**\n\n"
            "• Research the company thoroughly\n"
            "• Practice common questions aloud\n"
            "• Prepare thoughtful questions for interviewers\n"
            "• Dress appropriately (even for virtual interviews)\n"
            "• Follow up with a thank-you email within 24 hours\n"
            "• Use the STAR method for behavioral questions\n"
            "• Show enthusiasm and genuine interest",
            
            "📝 **CV Writing Tips**\n\n"
            "• Keep it to 1-2 pages\n"
            "• Use action verbs (Led, Managed, Developed)\n"
            "• Quantify achievements (e.g., 'Increased sales by 30%')\n"
            "• Include relevant keywords from job descriptions\n"
            "• Highlight your most recent and relevant experience\n"
            "• Use a clean, professional format\n"
            "• Proofread carefully for errors",
            
            "🌐 **Networking Strategies**\n\n"
            "• Attend industry events and conferences\n"
            "• Connect with professionals on LinkedIn\n"
            "• Join professional associations\n"
            "• Participate in online forums and communities\n"
            "• Conduct informational interviews\n"
            "• Follow up and maintain relationships\n"
            "• Offer help before asking for favors",
            
            "💼 **Career Growth Tips**\n\n"
            "• Set clear career goals\n"
            "• Continuously learn new skills\n"
            "• Seek feedback and act on it\n"
            "• Volunteer for challenging projects\n"
            "• Find a mentor in your field\n"
            "• Build your personal brand\n"
            "• Track your achievements regularly",
            
            "🎓 **Skill Development**\n\n"
            "• Identify your skill gaps\n"
            "• Take online courses and certifications\n"
            "• Practice new skills regularly\n"
            "• Apply learning to real projects\n"
            "• Stay updated with industry trends\n"
            "• Join skill-sharing communities\n"
            "• Consider formal education if needed",
            
            "💪 **Workplace Success**\n\n"
            "• Build strong relationships with colleagues\n"
            "• Communicate clearly and effectively\n"
            "• Take initiative and show leadership\n"
            "• Manage your time effectively\n"
            "• Stay organized and meet deadlines\n"
            "• Be adaptable and open to change\n"
            "• Maintain a positive attitude",
            
            "💰 **Salary Negotiation**\n\n"
            "• Research market rates for your role\n"
            "• Know your worth and contributions\n"
            "• Practice your pitch\n"
            "• Consider the total compensation package\n"
            "• Be confident but reasonable\n"
            "• Prepare to negotiate benefits too\n"
            "• Have a clear bottom line",
            
            "🚀 **Job Search Strategies**\n\n"
            "• Use multiple job boards\n"
            "• Customize each application\n"
            "• Leverage your network\n"
            "• Follow companies you're interested in\n"
            "• Set up job alerts\n"
            "• Prepare for interviews\n"
            "• Stay organized with applications",
            
            "🤝 **Professional Branding**\n\n"
            "• Create a strong LinkedIn profile\n"
            "• Share thought leadership content\n"
            "• Build a professional portfolio\n"
            "• Connect with industry influencers\n"
            "• Showcase your expertise\n"
            "• Be consistent across platforms\n"
            "• Monitor your digital footprint",
            
            "💡 **Remote Work Tips**\n\n"
            "• Create a dedicated workspace\n"
            "• Establish a routine\n"
            "• Communicate proactively\n"
            "• Use the right tools and technology\n"
            "• Set boundaries between work and life\n"
            "• Stay connected with teammates\n"
            "• Take regular breaks"
        ]
        
        # Return 3 random tips
        selected = random.sample(tips, min(3, len(tips)))
        return "\n\n---\n\n".join(selected)
