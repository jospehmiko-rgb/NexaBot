class CoverLetterGenerator:
    def generate_cover_letter(self, data):
        """Generate a tailored cover letter."""
        job_title = data.get('cl_job_title', '[Job Title]')
        company = data.get('cl_company', '[Company]')
        job_desc = data.get('cl_description', '')
        
        # Extract keywords from job description
        keywords = self._extract_keywords(job_desc)
        
        cover_letter = f"""
📧 **[Your Email]**
📱 **[Your Phone]**
📍 **[Your Location]**

**[Date]**

**Hiring Manager**
{company}
**[Company Address]**

---

**Re: Application for {job_title} Position**

Dear Hiring Manager,

I am writing to express my enthusiastic interest in the {job_title} position at {company}. With my strong background in **{', '.join(keywords[:3]) or 'relevant skills'}**, I am confident in my ability to contribute significantly to your team.

**Why I'm the Right Fit:**

• **Experience:** [Describe your relevant experience]
• **Skills:** I bring expertise in {', '.join(keywords[:4]) or 'key areas'}
• **Achievements:** [Highlight a major achievement]
• **Passion:** I am passionate about [industry/field] and {company}'s mission

**Key Contributions I Can Make:**

1. [First key contribution]
2. [Second key contribution]
3. [Third key contribution]

**Why {company}:**

I admire {company}'s [mention something specific about the company] and would be honored to contribute to your continued success.

I would welcome the opportunity to discuss how my skills and experience can benefit {company}. Thank you for considering my application.

**Sincerely,**

[Your Name]

---

💡 **Instructions:**
1. Fill in the bracketed sections [...]
2. Customize the bullet points with your specific achievements
3. Research the company to personalize the "Why {company}" section
4. Proofread and save as PDF

📌 **Pro Tip:** This cover letter is tailored for the {job_title} role. Use keywords from the job description to make it more specific!
"""
        return cover_letter
    
    def _extract_keywords(self, text):
        """Extract key skills/terms from job description."""
        # Simple keyword extraction
        common_skills = [
            'Python', 'JavaScript', 'Java', 'C++', 'React', 'Angular',
            'Data Science', 'Machine Learning', 'AI', 'Cloud', 'AWS',
            'Leadership', 'Management', 'Communication', 'Teamwork',
            'Problem Solving', 'Critical Thinking', 'Agile', 'Scrum',
            'Marketing', 'Sales', 'Finance', 'Analytics', 'Strategic'
        ]
        
        found = []
        for skill in common_skills:
            if skill.lower() in text.lower():
                found.append(skill)
        
        return found[:5] if found else ['relevant skills', 'experience', 'dedication']
