import random

class InterviewPrep:
    def generate_questions(self, data):
        """Generate interview questions and sample answers."""
        job_title = data.get('interview_job', '')
        company = data.get('interview_company', '')
        
        questions = []
        
        # General questions
        general_questions = [
            "Tell me about yourself.",
            "What are your greatest strengths?",
            "What's your biggest weakness and how do you overcome it?",
            "Where do you see yourself in 5 years?",
            "Why do you want to work here?",
            "Describe a challenge you faced and how you handled it.",
            "What's your leadership style?",
            "How do you handle pressure and deadlines?",
            "Tell me about a successful project you led.",
            "What are your salary expectations?",
            "Why should we hire you?",
            "What's your approach to teamwork?",
            "How do you handle feedback and criticism?",
            "Describe a time you failed and what you learned.",
            "What's your biggest professional achievement?"
        ]
        
        # Job-specific questions
        specific_questions = {
            'Software Engineer': [
                "Explain the difference between functional and object-oriented programming.",
                "How would you design a scalable system?",
                "What's your experience with agile development?"
            ],
            'Data Scientist': [
                "Explain the difference between supervised and unsupervised learning.",
                "How do you handle missing data?",
                "What's your experience with big data technologies?"
            ],
            'Marketing Manager': [
                "How do you measure campaign success?",
                "Describe your experience with digital marketing.",
                "How do you stay updated with marketing trends?"
            ],
            'Product Manager': [
                "How do you prioritize features?",
                "Tell me about a product you launched.",
                "How do you work with engineering teams?"
            ],
            'Financial Analyst': [
                "Explain the importance of financial ratios.",
                "How do you evaluate investment opportunities?",
                "What's your experience with financial modeling?"
            ],
            'Project Manager': [
                "How do you handle project delays?",
                "Describe your experience with project management tools.",
                "How do you communicate with stakeholders?"
            ]
        }
        
        # Select general questions
        selected_general = random.sample(general_questions, min(5, len(general_questions)))
        questions.extend(selected_general)
        
        # Add specific questions
        for key, q_list in specific_questions.items():
            if key.lower() in job_title.lower():
                questions.extend(random.sample(q_list, min(3, len(q_list))))
                break
        
        # Add company-specific question
        if company and company.strip().lower() != 'skip':
            questions.append(f"What do you know about {company}'s recent projects?")
            questions.append(f"How would you contribute to {company}'s growth?")
        
        # Format output
        output = "🎯 **Common Interview Questions**\n\n"
        
        for i, q in enumerate(questions[:12], 1):
            output += f"**{i}. {q}**\n"
            output += "   💡 *Tip: Use the STAR method to answer behavioral questions*\n"
            output += "   - **S**ituation: Set the context\n"
            output += "   - **T**ask: Describe the goal\n"
            output += "   - **A**ction: What you did\n"
            output += "   - **R**esult: The outcome\n\n"
            
            # Add a sample answer for common questions
            if i <= 3:  # Add samples for first few questions
                output += f"   📝 **Sample Answer:** [Your tailored answer here]\n\n"
        
        output += "---\n"
        output += "🎤 **Practice Tips:**\n"
        output += "• Practice answering aloud\n"
        output += "• Record yourself and review\n"
        output += "• Research the company thoroughly\n"
        output += "• Prepare questions for the interviewer\n"
        output += "• Review your resume and portfolio\n"
        
        return output
