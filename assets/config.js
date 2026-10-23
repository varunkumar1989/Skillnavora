/* =====================================================================
   SKILLNAVORA SETTINGS: edit this one file to update every page.
   After editing on GitHub, click "Commit changes"; the site updates in
   about a minute. Leave a value as "" to hide it.
   ===================================================================== */

const SITE = {
  // Contact. Phone numbers work with or without 91 in front.
  email: "varunebix@gmail.com",
  phone: "919211315006",
  whatsapp: "919211315006",
  city: "India · sessions online",

  // Social links (full links). Empty ones are hidden.
  linkedin: "https://www.linkedin.com/in/varun-pm01",
  instagram: "",
  youtube: "",

  // Booking link for mentoring calls, e.g. "https://calendly.com/your-name/30min"
  // or "https://cal.com/your-name". When set, the Mentoring page shows your
  // calendar so people can pick a time. When empty, it shows WhatsApp and email.
  booking: "",

  // Free key from web3forms.com so form messages arrive in your inbox.
  // Without it, the form opens the visitor's email app instead.
  web3formsKey: ""
};

/* ---- Programs page: courses and prices -------------------------------
   price: text shown on the card, e.g. "Free", "₹2,999", "₹9,999 / month".
          Leave "" to show "Ask for fees".
   link:  where the button goes. Leave "" to open WhatsApp with a message
          about this program.                                              */
const PROGRAMS = [
  { name: "PM Master Handbook", tag: "Free", price: "Free", unit: "self-paced",
    text: "23 modules from PM fundamentals to agentic AI, with quizzes, frameworks and PDFs.",
    points: ["12 core PM modules", "Framework and case study libraries", "Interview handbook"],
    button: "Start reading", link: "resources.html" },
  { name: "AI Tools Lab", tag: "Free", price: "Free", unit: "self-paced",
    text: "11 classes, basic to advanced, on the AI tools PMs use every day.",
    points: ["Claude and Claude Code", "Lovable, Replit, Figma, Notion", "Zapier, Make, n8n, chatbots, voice agents"],
    button: "See the classes", link: "resources.html#ai-tools-lab" },
  { name: "12-week guided plan", tag: "Free", price: "Free", unit: "about 5 hours a week",
    text: "One portfolio-ready assignment a week, ending with a capstone case study.",
    points: ["Weekly assignment brief", "Portfolio write-up template", "Capstone project"],
    button: "View the roadmap", link: "programs.html#roadmap" },
  { name: "1:1 PM mentoring", tag: "Most popular", price: "", unit: "per session", featured: true,
    text: "Personal guidance to plan your switch into product management and stay on track.",
    points: ["Career plan for your background", "Weekly check-ins and feedback", "Help choosing roles to apply for"],
    button: "Book a call", link: "mentoring.html" },
  { name: "Resume and portfolio review", tag: "1:1", price: "", unit: "one-time",
    text: "Detailed feedback on your resume, LinkedIn and case studies before you apply.",
    points: ["Line-by-line resume edits", "Portfolio and case study feedback", "LinkedIn profile tips"],
    button: "Ask about this", link: "" },
  { name: "Mock PM interviews", tag: "1:1", price: "", unit: "per interview",
    text: "Practise real PM interview rounds and get a scorecard with what to improve.",
    points: ["Product sense and design", "Metrics and analytics", "Behavioural and strategy rounds"],
    button: "Ask about this", link: "" }
];

/* ---- Testimonials -----------------------------------------------------
   Add real quotes from students or mentees (with their permission).
   photo is optional: upload an image to the assets folder and write e.g.
   "assets/priya.jpg". The section stays hidden until you add one.
   Example:
   { name: "Priya S.", role: "Associate PM, fintech startup",
     quote: "The case study feedback helped me land my first PM role.", photo: "" },  */
const TESTIMONIALS = [
];
