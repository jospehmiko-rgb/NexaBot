import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from dotenv import load_dotenv
import json
from utils.cv_generator import CVGenerator
from utils.cover_letter import CoverLetterGenerator
from utils.interview_prep import InterviewPrep
from utils.job_matcher import JobMatcher
from utils.career_tips import CareerTips

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment variable
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set!")

# Conversation states
(JOB_TITLE, JOB_LOCATION, JOB_TYPE, JOB_EXPERIENCE, JOB_INDUSTRY,
 CV_NAME, CV_EMAIL, CV_PHONE, CV_EDUCATION, CV_EXPERIENCE, CV_SKILLS,
 CL_JOB_TITLE, CL_COMPANY, CL_JOB_DESCRIPTION,
 INTERVIEW_JOB_TITLE, INTERVIEW_COMPANY,
 CV_UPLOAD,
 SKILLS_INPUT) = range(19)

# Initialize utility classes
cv_gen = CVGenerator()
cover_gen = CoverLetterGenerator()
interview_prep = InterviewPrep()
job_matcher = JobMatcher()
career_tips = CareerTips()

# User data storage (in production, use a database)
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when /start is issued."""
    user = update.effective_user
    welcome_text = f"""
👋 Hello {user.first_name}! Welcome to NexaBot!

🎯 Your Ultimate Job Assistant

I'm here to help you find your dream job and prepare winning applications.

Choose an option below:
"""
    
    keyboard = [
        [InlineKeyboardButton("🔎 Find Jobs", callback_data='find_jobs')],
        [InlineKeyboardButton("📄 Build CV", callback_data='build_cv')],
        [InlineKeyboardButton("✉️ Cover Letter", callback_data='cover_letter')],
        [InlineKeyboardButton("🎤 Interview Prep", callback_data='interview_prep')],
        [InlineKeyboardButton("🧠 Improve CV", callback_data='improve_cv')],
        [InlineKeyboardButton("🎯 Job Match", callback_data='job_match')],
        [InlineKeyboardButton("📚 Career Tips", callback_data='career_tips')],
        [InlineKeyboardButton("❓ Help", callback_data='help')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == 'find_jobs':
        await find_jobs_start(query)
    elif data == 'build_cv':
        await build_cv_start(query, context)
    elif data == 'cover_letter':
        await cover_letter_start(query, context)
    elif data == 'interview_prep':
        await interview_prep_start(query, context)
    elif data == 'improve_cv':
        await improve_cv_start(query)
    elif data == 'job_match':
        await job_match_start(query, context)
    elif data == 'career_tips':
        await career_tips_show(query)
    elif data == 'help':
        await help_command(query)
    else:
        # Handle conversation continuation
        await query.edit_message_text("✅ Done! What would you like to do next?")
        await start(query.message, context)

async def find_jobs_start(query):
    """Start job search flow."""
    text = """
🔎 **Find Jobs**

To find jobs, please specify:

1. **Position** (e.g., Software Engineer)
2. **Location** (e.g., New York, Remote)
3. **Job Type** (Full-time, Part-time, Contract)
4. **Experience Level** (Entry, Mid, Senior)
5. **Industry** (Tech, Finance, Healthcare, etc.)

Simply reply with the details and I'll search for matching jobs.

📌 **Example:**
"Software Engineer, Remote, Full-time, Mid-level, Tech"

💡 **Pro Tip:** Use our **Job Match** feature to discover the best roles for your skills!
"""
    await query.edit_message_text(text, parse_mode='Markdown')

async def build_cv_start(query, context):
    """Start CV building process."""
    text = """
📄 **Build Your Professional CV**

I'll guide you through creating a professional CV step by step.

Please provide the following information:

1️⃣ **Full Name:**
"""
    await query.edit_message_text(text, parse_mode='Markdown')
    return CV_NAME

async def cv_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle CV name input."""
    user_id = update.effective_user.id
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]['cv_name'] = update.message.text
    
    await update.message.reply_text("2️⃣ **Email Address:**", parse_mode='Markdown')
    return CV_EMAIL

async def cv_email_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle CV email input."""
    user_id = update.effective_user.id
    user_data[user_id]['cv_email'] = update.message.text
    
    await update.message.reply_text("3️⃣ **Phone Number:**", parse_mode='Markdown')
    return CV_PHONE

async def cv_phone_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle CV phone input."""
    user_id = update.effective_user.id
    user_data[user_id]['cv_phone'] = update.message.text
    
    await update.message.reply_text("4️⃣ **Education** (e.g., BSc Computer Science, Harvard University, 2020):", parse_mode='Markdown')
    return CV_EDUCATION

async def cv_education_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle CV education input."""
    user_id = update.effective_user.id
    user_data[user_id]['cv_education'] = update.message.text
    
    await update.message.reply_text("5️⃣ **Work Experience** (e.g., Software Engineer, Google, 2020-2023):", parse_mode='Markdown')
    return CV_EXPERIENCE

async def cv_experience_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle CV experience input."""
    user_id = update.effective_user.id
    user_data[user_id]['cv_experience'] = update.message.text
    
    await update.message.reply_text("6️⃣ **Skills** (comma-separated, e.g., Python, JavaScript, Leadership, Communication):", parse_mode='Markdown')
    return CV_SKILLS

async def cv_skills_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle CV skills input and generate CV."""
    user_id = update.effective_user.id
    user_data[user_id]['cv_skills'] = update.message.text
    
    # Generate CV
    cv_data = user_data[user_id]
    cv_pdf = cv_gen.generate_cv(cv_data)
    
    if cv_pdf:
        await update.message.reply_document(
            document=cv_pdf,
            caption="✅ **Your Professional CV is Ready!**\n\n📎 I've created a customized CV based on your information.\n\n💡 **Next Steps:**\n• Review and edit if needed\n• Use with job applications\n• Consider improving with our CV Improvement feature",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text("❌ Sorry, there was an error generating your CV. Please try again.")
    
    # Clean up user data
    if user_id in user_data:
        del user_data[user_id]
    
    # Show main menu again
    await start(update, context)
    return ConversationHandler.END

async def cover_letter_start(query, context):
    """Start cover letter generation."""
    text = """
✉️ **Generate a Tailored Cover Letter**

To create a personalized cover letter, please provide:

1️⃣ **Job Title:** (e.g., Data Scientist)

2️⃣ **Company Name:** (e.g., Google)

3️⃣ **Job Description:** (paste the full description)

💡 **Tip:** Be as detailed as possible for the best results!
"""
    await query.edit_message_text(text, parse_mode='Markdown')
    return CL_JOB_TITLE

async def cl_job_title_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle cover letter job title."""
    user_id = update.effective_user.id
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]['cl_job_title'] = update.message.text
    
    await update.message.reply_text("2️⃣ **Company Name:**", parse_mode='Markdown')
    return CL_COMPANY

async def cl_company_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle cover letter company."""
    user_id = update.effective_user.id
    user_data[user_id]['cl_company'] = update.message.text
    
    await update.message.reply_text("3️⃣ **Job Description:** (paste the full description)", parse_mode='Markdown')
    return CL_JOB_DESCRIPTION

async def cl_description_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate cover letter."""
    user_id = update.effective_user.id
    user_data[user_id]['cl_description'] = update.message.text
    
    cl_data = user_data[user_id]
    cover_letter = cover_gen.generate_cover_letter(cl_data)
    
    await update.message.reply_text(
        f"✉️ **Your Tailored Cover Letter**\n\n{cover_letter}\n\n---\n💡 **Next Steps:**\n• Personalize the highlighted sections\n• Proofread carefully\n• Save as PDF for submission",
        parse_mode='Markdown'
    )
    
    if user_id in user_data:
        del user_data[user_id]
    await start(update, context)
    return ConversationHandler.END

async def interview_prep_start(query, context):
    """Start interview preparation."""
    text = """
🎤 **Interview Preparation**

I'll help you prepare for your interview by generating questions and sample answers.

Please provide:

1️⃣ **Job Title:** (e.g., Product Manager)

2️⃣ **Company:** (optional, for company-specific questions)
"""
    await query.edit_message_text(text, parse_mode='Markdown')
    return INTERVIEW_JOB_TITLE

async def interview_job_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle interview job title."""
    user_id = update.effective_user.id
    if user_id not in user_data:
        user_data[user_id] = {}
    user_data[user_id]['interview_job'] = update.message.text
    
    await update.message.reply_text("2️⃣ **Company:** (optional, type 'skip' to skip)", parse_mode='Markdown')
    return INTERVIEW_COMPANY

async def interview_company_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle interview company and generate questions."""
    user_id = update.effective_user.id
    company = update.message.text
    if company.lower() != 'skip':
        user_data[user_id]['interview_company'] = company
    
    interview_data = user_data[user_id]
    questions = interview_prep.generate_questions(interview_data)
    
    await update.message.reply_text(
        f"🎤 **Interview Preparation for {interview_data['interview_job']}**\n\n{questions}\n\n---\n💡 **Tips:**\n• Practice answering aloud\n• Use the STAR method for behavioral questions\n• Research the company thoroughly",
        parse_mode='Markdown'
    )
    
    # Offer practice mode
    keyboard = [
        [InlineKeyboardButton("🎯 Practice Now", callback_data='practice_interview')],
        [InlineKeyboardButton("📚 More Questions", callback_data='more_questions')],
        [InlineKeyboardButton("🏠 Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Would you like to practice?", reply_markup=reply_markup)
    
    if user_id in user_data:
        del user_data[user_id]
    return ConversationHandler.END

async def improve_cv_start(query):
    """Start CV improvement feature."""
    text = """
🧠 **CV Improvement Service**

Upload your current CV (PDF or Word) and I'll analyze it for:

• 📝 **Formatting Issues**
• 💪 **Weak Descriptions**
• 🎯 **Missing Keywords**
• 📊 **Achievement Opportunities**
• 🌟 **ATS Compatibility**

📎 Please upload your CV file.
"""
    await query.edit_message_text(text, parse_mode='Markdown')

async def job_match_start(query, context):
    """Start job matching."""
    text = """
🎯 **Job Matcher**

Enter your skills and experience, and I'll suggest the best job categories for you.

**Example:**
"Python, Machine Learning, Data Analysis, 3 years, Leadership"

I'll recommend roles like:
• Data Scientist
• Machine Learning Engineer
• AI Research Scientist
• Data Analytics Manager

Please enter your skills and experience:
"""
    await query.edit_message_text(text, parse_mode='Markdown')
    return SKILLS_INPUT

async def skills_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process skills and suggest jobs."""
    skills = update.message.text
    suggestions = job_matcher.match_jobs(skills)
    
    await update.message.reply_text(
        f"🎯 **Job Recommendations Based on Your Skills**\n\n{suggestions}\n\n---\n💡 **Next Steps:**\n• Use these keywords in your job search\n• Tailor your CV for these roles\n• Apply through our Find Jobs feature",
        parse_mode='Markdown'
    )
    
    await start(update, context)
    return ConversationHandler.END

async def career_tips_show(query):
    """Show career tips."""
    tips = career_tips.get_tips()
    await query.edit_message_text(
        f"📚 **Career Tips & Advice**\n\n{tips}\n\n---\n💡 **Pro Tip:** Check back regularly for new tips and strategies!",
        parse_mode='Markdown'
    )

async def help_command(query):
    """Show help information."""
    help_text = """
❓ **NexaBot Help**

**Features:**
🔎 **Find Jobs** - Search for jobs by criteria
📄 **Build CV** - Create professional CVs
✉️ **Cover Letter** - Generate tailored cover letters
🎤 **Interview Prep** - Practice and prepare
🧠 **Improve CV** - Get feedback on your CV
🎯 **Job Match** - Find roles matching your skills
📚 **Career Tips** - Expert advice and strategies

**How to Use:**
1. Click any button to start
2. Follow the prompts
3. Provide information when asked
4. Review and use the results

**Tips:**
• Be detailed in your responses
• Save your CV and cover letters
• Practice interview questions regularly
• Keep your skills updated

**Support:** Contact @support for help
"""
    await query.edit_message_text(help_text, parse_mode='Markdown')

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle CV upload for improvement."""
    document = update.message.document
    
    if document.mime_type in ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        await update.message.reply_text("📎 **CV Received!** Analyzing your document...")
        
        # In production, you would process the file here
        # For now, provide generic feedback
        feedback = """
🧠 **CV Improvement Suggestions**

Based on best practices, here are some suggestions:

1️⃣ **Formatting:** Ensure consistent font styles and sizes
2️⃣ **Summary:** Add a compelling professional summary
3️⃣ **Achievements:** Use numbers (e.g., "Increased sales by 30%")
4️⃣ **Keywords:** Add industry-specific keywords
5️⃣ **Education:** Include relevant certifications
6️⃣ **Length:** Aim for 1-2 pages

**Specific Recommendations:**
• Add action verbs (Led, Managed, Developed)
• Quantify your achievements
• Tailor for each application
• Remove outdated experience
• Add a professional photo (optional)

💡 **Need more help?** Use our CV Builder to create a new optimized CV!
"""
        await update.message.reply_text(feedback, parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ Please upload a PDF or Word document.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Create conversation handlers
    cv_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(build_cv_start, pattern='build_cv')],
        states={
            CV_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, cv_name_handler)],
            CV_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, cv_email_handler)],
            CV_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, cv_phone_handler)],
            CV_EDUCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, cv_education_handler)],
            CV_EXPERIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, cv_experience_handler)],
            CV_SKILLS: [MessageHandler(filters.TEXT & ~filters.COMMAND, cv_skills_handler)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    cover_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(cover_letter_start, pattern='cover_letter')],
        states={
            CL_JOB_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, cl_job_title_handler)],
            CL_COMPANY: [MessageHandler(filters.TEXT & ~filters.COMMAND, cl_company_handler)],
            CL_JOB_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, cl_description_handler)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    interview_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(interview_prep_start, pattern='interview_prep')],
        states={
            INTERVIEW_JOB_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, interview_job_handler)],
            INTERVIEW_COMPANY: [MessageHandler(filters.TEXT & ~filters.COMMAND, interview_company_handler)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    job_match_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(job_match_start, pattern='job_match')],
        states={
            SKILLS_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, skills_input_handler)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(cv_conv_handler)
    application.add_handler(cover_conv_handler)
    application.add_handler(interview_conv_handler)
    application.add_handler(job_match_conv_handler)
    
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(CallbackQueryHandler(career_tips_show, pattern='career_tips'))
    application.add_handler(CallbackQueryHandler(help_command, pattern='help'))
    
    # Add error handler
    application.add_error_handler(error_handler)

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
