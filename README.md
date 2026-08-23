# AstroFetch-Voyager X: TESS Exoplanet Hunter, Star Light Curve Analyzer


AstroFetch-Voyager X is an exoplanet detection platform that uses star light curve data from the TESS accessed from the MAST API for planet identification and condition assessment
(temperature, atmosphere content etc.) 


# Features
Features a Light Curve Graph depicting the normalized flux of light from the specified star.

Uses that data to anaylze and depict a rough model of how the planet and the star compare in size to each other.

Also consists of real-time metrics - eg. planet radius, distance from Earth, etc.

Voyager-X features an AI Chatbot as well to explain the planetary characteristics and generates a simple story to make it easier to understand.

# How It Works
User enters Star TIC ID-
System fetches TESS lightcurve data -
Displays graph of transit data -
AI then analyzes characteristics to answer questions. -
Shows orbital system visualization with key metrics.

# My Contributions
Conceptualized the idea -- designed the exoplanet detection platform, orbital visualization, and UI direction

Debugged constant integration issues -- identified API errors, performance problems, button logic

Deployed to production — set up using Render, tested (a lot), handled feedback and broken iterations.

# Tech Stack
Frontend: HTML, JavaScript, Tailwind CSS, Chart.js

Backend: Python, FastAPI

External APIs: TESS light curve data, Groq AI

Hosting: Render

AI assistance: Google Gemini (initial coding and core structure), Claude (debugging/fixes/polishing)

# How To Use
Visit the live service at :  https://voyager-x-5aug.onrender.com/

Launch Mission Control -
Type in Star TIC ID of your choice -
Initialize BLS Scan -- and you are set.  

if you do not understand the graph/metrics just ask the AI Chatbot on the side panel.

# What I learned : patience is key and that there are no shortcuts in life (I'm serious).



