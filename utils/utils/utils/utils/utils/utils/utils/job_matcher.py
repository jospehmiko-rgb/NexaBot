class JobMatcher:
    def match_jobs(self, skills_text):
        """Match skills to job recommendations."""
        skills_lower = skills_text.lower()
        
        # Job categories with required skills
        job_categories = {
            'Technology & Software': {
                'keywords': ['python', 'javascript', 'java', 'c++', 'react', 'angular', 
                            'node', 'typescript', 'html', 'css', 'sql', 'database',
                            'aws', 'cloud', 'docker', 'kubernetes', 'git', 'api',
                            'full stack', 'frontend', 'backend', 'mobile', 'ios', 'android'],
                'roles': [
                    'Software Engineer',
                    'Web Developer',
                    'Mobile App Developer',
                    'Full Stack Developer',
                    'DevOps Engineer',
                    'Cloud Architect',
                    'Quality Assurance Engineer',
                    'Technical Lead'
                ],
                'salary_range': '$80,000 - $150,000+',
                'growth': 'High - continuous learning and advancement'
            },
            
            'Data Science & AI': {
                'keywords': ['python', 'r', 'sql', 'machine learning', 'deep learning', 
                            'nlp', 'computer vision', 'tensorflow', 'pytorch', 'scikit-learn',
                            'data analysis', 'statistics', 'probability', 'big data',
                            'hadoop', 'spark', 'tableau', 'power bi', 'data visualization'],
                'roles': [
                    'Data Scientist',
                    'Machine Learning Engineer',
                    'AI Research Scientist',
                    'Data Analyst',
                    'Data Engineer',
                    'Business Intelligence Developer',
                    'Quantitative Analyst'
                ],
                'salary_range': '$90,000 - $170,000+',
                'growth': 'Excellent - cutting edge field with strong demand'
            },
            
            'Product Management': {
                'keywords': ['product', 'management', 'leadership', 'strategy', 'roadmap',
                            'user experience', 'ux', 'agile', 'scrum', 'jira', 'analytics',
                            'business', 'market', 'user research', 'prioritization'],
                'roles': [
                    'Product Manager',
                    'Product Owner',
                    'Project Manager',
                    'Program Manager',
                    'Technical Product Manager',
                    'Product Analyst'
                ],
                'salary_range': '$85,000 - $160,000+',
                'growth': 'Good - versatile role with many opportunities'
            },
            
            'Finance & Accounting': {
                'keywords': ['finance', 'accounting', 'budget', 'forecast', 'analysis',
                            'financial', 'investment', 'banking', 'audit', 'tax',
                            'compliance', 'risk', 'fund', 'portfolio', 'valuation'],
                'roles': [
                    'Financial Analyst',
                    'Accountant',
                    'Investment Analyst',
                    'Risk Analyst',
                    'Auditor',
                    'Financial Manager',
                    'Wealth Management Advisor'
                ],
                'salary_range': '$70,000 - $140,000+',
                'growth': 'Stable - consistent demand with clear progression'
            },
            
            'Marketing & Communications': {
                'keywords': ['marketing', 'social media', 'content', 'seo', 'sem',
                            'digital', 'brand', 'strategy', 'analytics', 'communication',
                            'campaign', 'creative', 'design', 'pr', 'public relations'],
                'roles': [
                    'Marketing Manager',
                    'Digital Marketing Specialist',
                    'Content Strategist',
                    'Social Media Manager',
                    'Brand Manager',
                    'SEO Specialist',
                    'Marketing Analyst'
                ],
                'salary_range': '$60,000 - $120,000+',
                'growth': 'Growing - digital transformation driving demand'
            },
            
            'Human Resources': {
                'keywords': ['hr', 'human resources', 'recruitment', 'talent', 'employee',
                            'benefits', 'training', 'development', 'culture', 'engagement',
                            'workplace', 'policy', 'compensation', 'onboarding'],
                'roles': [
                    'HR Manager',
                    'Recruiter',
                    'Talent Acquisition Specialist',
                    'HR Business Partner',
                    'Training & Development Manager',
                    'Employee Relations Specialist'
                ],
                'salary_range': '$60,000 - $110,000+',
                'growth': 'Steady - essential function in all organizations'
            },
            
            'Healthcare': {
                'keywords': ['healthcare', 'medical', 'clinical', 'patient', 'pharma',
                            'biotech', 'research', 'nursing', 'physician', 'health',
                            'wellness', 'therapy', 'rehabilitation', 'care'],
                'roles': [
                    'Healthcare Administrator',
                    'Clinical Research Coordinator',
                    'Health Informatics Specialist',
                    'Medical Writer',
                    'Public Health Professional',
                    'Healthcare Consultant'
                ],
                'salary_range': '$65,000 - $130,000+',
                'growth': 'High - growing industry with many opportunities'
            },
            
            'Education': {
                'keywords': ['education', 'teaching', 'curriculum', 'training', 'learning',
                            'development', 'instruction', 'student', 'academic', 'pedagogy',
                            'edtech', 'classroom', 'assessment'],
                'roles': [
                    'Teacher',
                    'Curriculum Developer',
                    'Instructional Designer',
                    'Education Consultant',
                    'Learning Specialist',
                    'EdTech Professional'
                ],
                'salary_range': '$50,000 - $100,000+',
                'growth': 'Moderate - with growth in EdTech'
            }
        }
        
        # Find matching categories
        matches = []
        for category, info in job_categories.items():
            match_score = 0
            for keyword in info['keywords']:
                if keyword in skills_lower:
                    match_score += 1
            
            if match_score > 0:
                matches.append((match_score, category, info))
        
        # Sort by match score
        matches.sort(reverse=True)
        
        # Build output
        output = "🎯 **Top Job Matches for Your Skills**\n\n"
        
        if not matches:
            output += "⚠️ No direct matches found. Consider:\n"
            output += "• Expanding your skill set\n"
            output += "• Exploring related fields\n"
            output += "• Checking entry-level positions\n\n"
            output += "💡 **Suggested Keywords:**\n"
            output += "Try adding skills like: Python, Management, Communication, Data Analysis\n"
            return output
        
        for i, (score, category, info) in enumerate(matches[:4], 1):
            output += f"**{i}. {category}** (Match Score: {score}/10)\n"
            output += "─" * 30 + "\n"
            output += f"📌 **Recommended Roles:**\n"
            for role in info['roles'][:3]:
                output += f"   • {role}\n"
            output += f"\n💰 **Salary Range:** {info['salary_range']}\n"
            output += f"📈 **Growth Potential:** {info['growth']}\n"
            output += f"\n🔑 **Required Skills:**\n"
            skill_list = ', '.join(info['keywords'][:6])
            output += f"   {skill_list}\n\n"
        
        output += "---\n"
        output += "💡 **Next Steps:**\n"
        output += "1. 🎯 Focus on roles with the highest match scores\n"
        output += "2. 📝 Tailor your CV for specific roles\n"
        output += "3. 📚 Learn missing skills for your target role\n"
        output += "4. 🌐 Network with professionals in these fields\n"
        output += "5. 🎤 Practice interview questions for these roles\n\n"
        
        output += "🚀 **Quick Actions:**\n"
        output += "• Use /build_cv to create a tailored CV\n"
        output += "• Use /find_jobs to search for positions\n"
        output += "• Use /interview_prep to prepare for interviews\n"
        
        return output
