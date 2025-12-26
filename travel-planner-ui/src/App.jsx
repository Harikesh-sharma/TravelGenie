import { useState, useEffect, useRef } from 'react'
import './App.css'
import jsPDF from 'jspdf'
import 'jspdf-autotable'



const CITIES_BY_STATE = {
  "Andaman and Nicobar Islands": ["Port Blair"],
  "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool", "Tirupati"],
  "Arunachal Pradesh": ["Itanagar", "Tawang", "Ziro"],
  "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Tezpur"],
  "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Bodh Gaya"],
  "Chandigarh": ["Chandigarh"],
  "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba"],
  "Dadra and Nagar Haveli and Daman and Diu": ["Daman", "Diu", "Silvassa"],
  "Delhi": ["Delhi"],
  "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa"],
  "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar", "Gandhinagar", "Rann of Kutch"],
  "Haryana": ["Faridabad", "Gurgaon", "Panipat", "Ambala", "Kurukshetra"],
  "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala", "Kullu", "Solan", "Mandi"],
  "Jammu and Kashmir": ["Srinagar", "Jammu", "Gulmarg", "Pahalgam"],
  "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro"],
  "Karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore", "Belgaum", "Hampi", "Coorg"],
  "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Munnar", "Alleppey"],
  "Ladakh": ["Leh", "Kargil"],
  "Lakshadweep": ["Kavaratti", "Agatti"],
  "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain", "Khajuraho"],
  "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", "Thane", "Shirdi", "Mahabaleshwar"],
  "Manipur": ["Imphal"],
  "Meghalaya": ["Shillong", "Cherrapunji"],
  "Mizoram": ["Aizawl"],
  "Nagaland": ["Kohima", "Dimapur"],
  "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Puri", "Konark"],
  "Puducherry": ["Pondicherry"],
  "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda"],
  "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer", "Jaisalmer", "Pushkar"],
  "Sikkim": ["Gangtok", "Pelling"],
  "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Kanyakumari", "Ooty"],
  "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar"],
  "Tripura": ["Agartala"],
  "Uttar Pradesh": ["Lucknow", "Kanpur", "Ghaziabad", "Agra", "Varanasi", "Meerut", "Prayagraj", "Noida", "Mathura"],
  "Uttarakhand": ["Dehradun", "Haridwar", "Rishikesh", "Nainital", "Mussoorie"],
  "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Siliguri", "Darjeeling"]
}

const ALL_CITIES = Object.values(CITIES_BY_STATE).flat().sort()

const STATE_IMAGES = {
  "Goa": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1920&q=80",
  "Rajasthan": "https://images.unsplash.com/photo-1477587458883-47145ed94245?auto=format&fit=crop&w=1920&q=80",
  "Kerala": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1920&q=80",
  "Himachal Pradesh": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1920&q=80",
  "Uttar Pradesh": "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=1920&q=80",
  "Jammu and Kashmir": "https://images.unsplash.com/photo-1595846519845-68e298c2edd8?auto=format&fit=crop&w=1920&q=80",
  "Maharashtra": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?auto=format&fit=crop&w=1920&q=80",
  "Delhi": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=1920&q=80",
  "Karnataka": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=1920&q=80",
  "Tamil Nadu": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1920&q=80",
  "West Bengal": "https://images.unsplash.com/photo-1558431382-27e303142255?auto=format&fit=crop&w=1920&q=80",
  "Gujarat": "https://images.unsplash.com/photo-1578509476878-3c3924d52477?auto=format&fit=crop&w=1920&q=80",
  "Punjab": "https://images.unsplash.com/photo-1580836526476-8d492471676f?auto=format&fit=crop&w=1920&q=80",
  "Ladakh": "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?auto=format&fit=crop&w=1920&q=80",
  "Uttarakhand": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSTdORvAGK2Z_8FMYS7xR-2XC1nMabCXjpgvA&s",
  "Sikkim": "https://images.unsplash.com/photo-1588416936097-41850ab3d86d?auto=format&fit=crop&w=1920&q=80",
  "Telangana": "https://images.unsplash.com/photo-1626014903708-40aa47cd24ea?auto=format&fit=crop&w=1920&q=80",
  "Andhra Pradesh": "https://images.unsplash.com/photo-1621831536720-6024d88f1a6a?auto=format&fit=crop&w=1920&q=80",
  "Odisha": "https://images.unsplash.com/photo-1598605272254-16f0c0ecdfa5?auto=format&fit=crop&w=1920&q=80",
  "Meghalaya": "https://images.unsplash.com/photo-1592243283681-342085f5249f?auto=format&fit=crop&w=1920&q=80",
  "Madhya Pradesh": "https://images.unsplash.com/photo-1600607686527-6fb886090705?auto=format&fit=crop&w=1920&q=80",
  "Bihar": "https://images.unsplash.com/photo-1627894483216-2138af692e32?auto=format&fit=crop&w=1920&q=80",
  "Assam": "https://images.unsplash.com/photo-1598335624167-68381054514d?auto=format&fit=crop&w=1920&q=80",
  "default": "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80"
}

const POPULAR_DESTINATIONS = [
  { name: "Goa", price: "₹15,000" },
  { name: "Rajasthan", price: "₹12,000" },
  { name: "Kerala", price: "₹18,000" },
  { name: "Himachal Pradesh", price: "₹10,000" },
  { name: "Ladakh", price: "₹25,000" },
  { name: "Uttarakhand", price: "₹8,000" }
]

const Hero = ({ onStart }) => (
  <div className="hero-section">
    <div className="hero-badge">🚀 AI-Powered Travel Planning</div>
    <div className="hero-content">
      <h1>Your Dream Trip, <br /> <span className="gradient-text">Planned in Seconds</span> ✨</h1>
      <p>Experience the magic of AI-powered travel planning. Tailored itineraries, budget optimization, and hidden gems await.</p>
      <div className="hero-buttons">
        <button className="btn-hero" onClick={onStart}>Start Planning Free</button>
        <button className="btn-hero secondary" onClick={() => document.querySelector('.destinations-section').scrollIntoView({ behavior: 'smooth' })}>Explore Destinations</button>
      </div>
      <div className="hero-stats">
        <div className="stat-item">
          <span className="stat-number">10k+</span>
          <span className="stat-label">Trips Planned</span>
        </div>
        <div className="stat-divider"></div>
        <div className="stat-item">
          <span className="stat-number">50+</span>
          <span className="stat-label">Cities Covered</span>
        </div>
        <div className="stat-divider"></div>
        <div className="stat-item">
          <span className="stat-number">4.9/5</span>
          <span className="stat-label">User Rating</span>
        </div>
      </div>
    </div>
  </div>
)

const HowItWorks = () => (
  <div className="how-it-works-section">
    <h2 style={{ textAlign: 'center', marginBottom: '3rem', color: 'var(--text-main)' }}>How It Works 🛠️</h2>
    <div className="steps-container">
      <div className="step-card">
        <div className="step-icon">🎯</div>
        <h3>1. Set Preferences</h3>
        <p>Enter your budget, duration, and interests.</p>
      </div>
      <div className="step-connector"></div>
      <div className="step-card">
        <div className="step-icon">🤖</div>
        <h3>2. AI Magic</h3>
        <p>Our AI crafts the perfect route for you.</p>
      </div>
      <div className="step-connector"></div>
      <div className="step-card">
        <div className="step-icon">🎒</div>
        <h3>3. Travel Ready</h3>
        <p>Get a full itinerary with costs & travel info.</p>
      </div>
    </div>
  </div>
)

const CTASection = ({ onStart }) => (
  <div className="cta-section">
    <div className="cta-content">
      <h2>Ready to Explore India? 🇮🇳</h2>
      <p>Stop worrying about planning and start dreaming about your journey.</p>
      <button className="btn-hero" onClick={onStart} style={{ marginTop: '1.5rem', backgroundColor: 'white', color: 'var(--primary-color)' }}>Plan My Trip Now</button>
    </div>
  </div>
)

const BudgetCalculator = () => {
  const [type, setType] = useState('beach')
  const [style, setStyle] = useState('budget')
  const [days, setDays] = useState(3)
  const [travelers, setTravelers] = useState(1)

  const baseRates = {
    beach: 1500,
    mountains: 1200,
    city: 2000,
    heritage: 1800
  }

  const multipliers = {
    budget: 1,
    comfort: 2,
    luxury: 4
  }

  const calculateEstimate = () => {
    const base = baseRates[type] * multipliers[style] * days * travelers
    const min = Math.round(base * 0.9)
    const max = Math.round(base * 1.1)
    return `₹${min.toLocaleString()} - ₹${max.toLocaleString()}`
  }

  return (
    <div className="budget-calculator-section">
      <h2 style={{ textAlign: 'center', marginBottom: '2rem', color: 'var(--text-main)' }}>Quick Budget Estimator 🧮</h2>
      <div className="calculator-card">
        <div className="calc-inputs">
          <div className="form-group">
            <label>Destination Vibe</label>
            <select value={type} onChange={(e) => setType(e.target.value)}>
              <option value="beach">🏖️ Beach</option>
              <option value="mountains">🏔️ Mountains</option>
              <option value="city">🏙️ City Life</option>
              <option value="heritage">🛕 Heritage</option>
            </select>
          </div>
          <div className="form-group">
            <label>Travel Style</label>
            <select value={style} onChange={(e) => setStyle(e.target.value)}>
              <option value="budget">🎒 Budget (Backpacker)</option>
              <option value="comfort">🧳 Comfort (3-4 Star)</option>
              <option value="luxury">👑 Luxury (5 Star)</option>
            </select>
          </div>
          <div className="form-group">
            <label>Duration: {days} Days</label>
            <input type="range" min="1" max="15" value={days} onChange={(e) => setDays(parseInt(e.target.value))} />
          </div>
           <div className="form-group">
            <label>Travelers: {travelers}</label>
            <input type="range" min="1" max="10" value={travelers} onChange={(e) => setTravelers(parseInt(e.target.value))} />
          </div>
        </div>
        <div className="calc-result">
          <h3>Estimated Cost</h3>
          <div className="estimate-amount">{calculateEstimate()}</div>
          <p>Includes stay, food & local travel</p>
        </div>
      </div>
    </div>
  )
}

const About = () => (
  <div className="travel-form about-section">
    <h2>About TravelGenie 🧞‍♂️</h2>
    <p>Welcome to <strong>TravelGenie</strong>, your personal AI-powered travel assistant designed to make exploring India easier and more exciting!</p>
    <p>Whether you're a solo backpacker, a couple seeking a romantic getaway, or a family on vacation, TravelGenie helps you craft the perfect itinerary based on your <strong>budget</strong>, <strong>duration</strong>, and <strong>interests</strong>.</p>
    <div style={{ margin: '2rem 0', textAlign: 'left', display: 'inline-block' }}>
      <h3 style={{ marginTop: 0, textAlign: 'left' }}>How it Works:</h3>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        <li style={{ marginBottom: '0.5rem' }}>📍 <strong>Select a Destination:</strong> Choose a specific city or let us surprise you.</li>
        <li style={{ marginBottom: '0.5rem' }}>💰 <strong>Set Your Budget:</strong> We optimize for your financial comfort.</li>
        <li style={{ marginBottom: '0.5rem' }}>⏳ <strong>Pick Duration:</strong> From weekend getaways to long vacations.</li>
        <li style={{ marginBottom: '0.5rem' }}>🎨 <strong>Choose Preferences:</strong> Accommodation, Food, and more.</li>
      </ul>
    </div>
    <p>Built with ❤️ for travelers.</p>
  </div>
)

const Features = () => (
  <div className="features-section">
    <div className="feature-card">
      <div className="feature-icon">🧠</div>
      <h3>AI-Powered Planning</h3>
      <p>Smart algorithms craft the perfect schedule tailored to your interests.</p>
    </div>
    <div className="feature-card">
      <div className="feature-icon">💸</div>
      <h3>Budget Optimized</h3>
      <p>Get the most out of your money with real-time cost estimations.</p>
    </div>
    <div className="feature-card">
      <div className="feature-icon">💎</div>
      <h3>Hidden Gems</h3>
      <p>Discover local secrets alongside famous landmarks.</p>
    </div>
  </div>
)

const PopularDestinations = ({ onSelect }) => (
  <div className="destinations-section">
    <h2 style={{ textAlign: 'center', marginBottom: '1rem', color: 'var(--text-main)' }}>Popular This Season</h2>
    <div className="destinations-grid">
      {POPULAR_DESTINATIONS.map(dest => (
        <div key={dest.name} className="destination-card" onClick={() => onSelect(dest.name)}>
          <img src={STATE_IMAGES[dest.name]} alt={dest.name} />
          <div className="destination-info">
            <h3>{dest.name}</h3>
            <span>Tap to Plan →</span>
            <div className="price-tag">Starts @ {dest.price}</div>
          </div>
        </div>
      ))}
    </div>
  </div>
)

const Testimonials = () => {
  const [index, setIndex] = useState(0)
  const reviews = [
    { name: "Aarav Patel", location: "Mumbai", text: "TravelGenie planned my perfect weekend in Goa! The budget estimation was spot on.", rating: "⭐⭐⭐⭐⭐" },
    { name: "Priya Sharma", location: "Delhi", text: "I discovered hidden cafes in Manali I would have never found on my own. Highly recommend!", rating: "⭐⭐⭐⭐⭐" },
    { name: "Rohan Gupta", location: "Bangalore", text: "The itinerary was well-paced. Not too rushed, not too slow. Just right for my family trip.", rating: "⭐⭐⭐⭐⭐" }
  ]

  useEffect(() => {
    const timer = setInterval(() => {
      setIndex((prev) => (prev + 1) % reviews.length)
    }, 5000)
    return () => clearInterval(timer)
  }, [reviews.length])

  const next = () => setIndex((prev) => (prev + 1) % reviews.length)
  const prev = () => setIndex((prev) => (prev - 1 + reviews.length) % reviews.length)

  const review = reviews[index]

  return (
    <div className="testimonials-section">
      <h2 style={{ textAlign: 'center', marginBottom: '2rem', color: 'var(--text-main)' }}>What Travelers Say</h2>
      <div className="testimonial-slider">
        <button className="slider-btn prev" onClick={prev}>&#10094;</button>
        <div className="testimonial-card" key={index}>
          <div className="testimonial-header">
            <div className="avatar">{review.name[0]}</div>
            <div className="testimonial-info">
              <h4>{review.name}</h4>
              <span>{review.location}</span>
            </div>
          </div>
          <p>"{review.text}"</p>
          <div className="rating">{review.rating}</div>
        </div>
        <button className="slider-btn next" onClick={next}>&#10095;</button>
      </div>
      <div className="slider-dots">
        {reviews.map((_, i) => (
          <span key={i} className={`dot ${i === index ? 'active' : ''}`} onClick={() => setIndex(i)}></span>
        ))}
      </div>
    </div>
  )
}

const getTravelEstimates = (origin, destination) => {
  const isIsland = ["Port Blair", "Lakshadweep", "Havelock"].some(island => destination.includes(island))
  const seed = (origin.length + destination.length) * 100
  
  if (origin && destination && origin.toLowerCase() === destination.toLowerCase()) {
    return {
      bus: { available: true, price: "₹50 - ₹200", label: "Local Transport" },
      train: { available: true, price: "₹20 - ₹100", label: "Local Train / Metro" },
      flight: { available: false, label: "N/A (Same City)" }
    }
  }

  return {
    bus: isIsland ? { available: false, label: "Not Applicable (Island)" } : { available: true, price: `₹${500 + seed} - ₹${1200 + seed}`, label: "AC / Volvo" },
    train: isIsland ? { available: false, label: "Not Applicable (Island)" } : { available: true, price: `₹${400 + seed} - ₹${2000 + seed}`, label: "Sleeper / 3AC" },
    flight: { available: true, price: `₹${3500 + seed * 2} - ₹${8000 + seed * 2}`, label: "Economy / Direct" }
  }
}

function App() {
  const [formData, setFormData] = useState({
    budget: '',
    days: '',
    originCity: '',
    city: '',
    preferences: []
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [view, setView] = useState('landing') // 'landing', 'planner', 'about'
  const [error, setError] = useState(null)
  const [selectedState, setSelectedState] = useState('')
  const [isScrolled, setIsScrolled] = useState(false)
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('darkMode') === 'true'
  })
  const [copySuccess, setCopySuccess] = useState(false)
  const [subscribed, setSubscribed] = useState(false)
  const [subscribing, setSubscribing] = useState(false)
  const [emailError, setEmailError] = useState('')
  const resultRef = useRef(null)

  useEffect(() => {
    if (result && resultRef.current) {
      resultRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [result])

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', darkMode ? 'dark' : 'light')
    localStorage.setItem('darkMode', darkMode)
  }, [darkMode])

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleCheckboxChange = (e) => {
    const { value, checked } = e.target
    setFormData(prev => {
      const newPrefs = checked 
        ? [...prev.preferences, value]
        : prev.preferences.filter(p => p !== value)
      return { ...prev, preferences: newPrefs }
    })
  }

  const handleStateChange = (e) => {
    setSelectedState(e.target.value)
    setFormData(prev => ({ ...prev, city: '' }))
  }

  const handleCardClick = (state) => {
    setSelectedState(state)
    setFormData(prev => ({ ...prev, city: '' }))
    setView('planner')
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const generatePlan = async (data) => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      // Use relative path; the proxy in vite.config.js will forward this to http://127.0.0.1:8000
      const response = await fetch('/plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...data,
          budget: parseInt(data.budget),
          days: parseInt(data.days)
        })
      })
      
      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        const resultData = await response.json()
        resultData.travel_options = getTravelEstimates(data.originCity || "Delhi", resultData.city)
        if (response.ok) {
          setResult(resultData)
        } else {
          setError(resultData.detail || 'An error occurred')
        }
      } else {
        const text = await response.text()
        setError(`Server returned non-JSON response (${response.status}): ${text.slice(0, 100)}`)
      }
    } catch (err) {
      setError('Network error: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    generatePlan(formData)
  }

  const handleSurpriseMe = () => {
    if (!formData.budget) {
      alert("Please enter a budget first!")
      return
    }

    const allPreferences = ["accommodation", "food"]
    
    const randomCity = ALL_CITIES[Math.floor(Math.random() * ALL_CITIES.length)]
    const randomDays = Math.floor(Math.random() * 4) + 2 // 2 - 5
    
    const randomPreferences = allPreferences.filter(() => Math.random() > 0.5)
    if (randomPreferences.length === 0) {
      randomPreferences.push(allPreferences[Math.floor(Math.random() * allPreferences.length)])
    }

    const newData = {
      budget: formData.budget,
      days: randomDays.toString(),
      originCity: formData.originCity || "Delhi",
      city: randomCity,
      preferences: randomPreferences
    }

    setSelectedState('')
    setFormData(newData)
    generatePlan(newData)
  }

  const handleDownloadPDF = () => {
    const doc = new jsPDF()
    
    // Title
    doc.setFontSize(20)
    doc.text(`Trip Itinerary: ${result.city}`, 14, 22)
    
    // Summary
    doc.setFontSize(12)
    doc.text(`Total Budget: ₹${result.total_budget}`, 14, 32)
    doc.text(`Total Cost: ₹${result.total_cost}`, 14, 38)
    doc.text(`Remaining: ₹${result.total_budget - result.total_cost}`, 14, 44)

    // Travel Options
    doc.text(`Estimated Travel Costs:`, 14, 54)
    const travelData = [
      ["Mode", "Estimated Fare", "Type/Note"],
      ["Bus 🚌", result.travel_options.bus.available ? result.travel_options.bus.price : "-", result.travel_options.bus.label],
      ["Train 🚆", result.travel_options.train.available ? result.travel_options.train.price : "-", result.travel_options.train.label],
      ["Flight ✈️", result.travel_options.flight.available ? result.travel_options.flight.price : "-", result.travel_options.flight.label]
    ]

    // Table Data
    const tableColumn = ["Day", "Activity", "Cost (₹)", "Hours"]
    const tableRows = []

    Object.entries(result.itinerary).forEach(([day, activities]) => {
      if (activities.length === 0) {
        tableRows.push([day, "No activities planned", "-", "-"])
      } else {
        activities.forEach(act => {
          tableRows.push([day, act.activity, act.cost, act.hours])
        })
      }
    })

    doc.autoTable({
      startY: 60,
      head: [travelData[0]],
      body: travelData.slice(1),
      theme: 'grid',
      headStyles: { fillColor: [100, 100, 100] }
    })

    doc.autoTable({
      startY: doc.lastAutoTable.finalY + 10,
      head: [tableColumn],
      body: tableRows,
      theme: 'grid',
      headStyles: { fillColor: [79, 70, 229] }
    })

    doc.save(`${result.city}_Itinerary.pdf`)
  }

  const handleShare = async () => {
    if (!result) return

    let shareText = `Trip to ${result.city} 🇮🇳\n\n`
    shareText += `💰 Budget: ₹${result.total_budget}\n`
    shareText += `💵 Cost: ₹${result.total_cost}\n`
    shareText += `🏷️ Remaining: ₹${result.total_budget - result.total_cost}\n\n`
    
    shareText += `🚆 Travel Estimates:\n`
    shareText += `   • Bus: ${result.travel_options.bus.available ? result.travel_options.bus.price : result.travel_options.bus.label}\n`
    shareText += `   • Train: ${result.travel_options.train.available ? result.travel_options.train.price : result.travel_options.train.label}\n`
    shareText += `   • Flight: ${result.travel_options.flight.price}\n\n`
    shareText += `📅 Itinerary:\n`

    Object.entries(result.itinerary).forEach(([day, activities]) => {
      shareText += `\n📌 ${day}:\n`
      if (activities.length === 0) {
        shareText += `   No activities planned\n`
      } else {
        activities.forEach(act => {
          shareText += `   • ${act.activity} (${act.hours})\n`
        })
      }
    })
    
    shareText += `\nPlanned with TravelGenie 🧞‍♂️`

    try {
      await navigator.clipboard.writeText(shareText)
      setCopySuccess(true)
      setTimeout(() => setCopySuccess(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  const handleSubscribe = async (e) => {
    e.preventDefault()
    const email = e.target.email.value

    // Basic Email Validation Regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      setEmailError('Please enter a valid email address (e.g., user@example.com)')
      return
    }
    setEmailError('')
    setSubscribing(true)

    try {
      const response = await fetch('/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      })

      if (response.ok) {
        setSubscribed(true)
        setTimeout(() => setSubscribed(false), 3000)
        e.target.reset()
      } else {
        const data = await response.json()
        setEmailError(data.detail || 'Subscription failed. Please try again.')
      }
    } catch (err) {
      console.error('Failed to subscribe:', err)
      setEmailError('Network error. Please try again later.')
    } finally {
      setSubscribing(false)
    }
  }

  const bgImage = STATE_IMAGES[selectedState] || STATE_IMAGES["default"]
  const overlayColor = darkMode ? 'rgba(17, 24, 39, 0.92)' : 'rgba(255, 255, 255, 0.85)'

  return (
    <div className="app-wrapper">
      <div className="app-background" style={{
        backgroundImage: `linear-gradient(${overlayColor}, ${overlayColor}), url('${bgImage}')`
      }}>
        {selectedState && <span className="watermark-text">{selectedState}</span>}
      </div>
      <header className={`app-header ${!result && !isScrolled ? 'header-transparent' : ''}`}>
        <div className="header-content">
          <span className="logo" onClick={() => { setResult(null); setView('landing'); }}>✈️ TravelGenie</span>
          <nav className="nav-menu">
            <a href="#" className="nav-link" onClick={(e) => { e.preventDefault(); setResult(null); setView('landing'); }}>Home</a>
            <a href="#" className="nav-link" onClick={(e) => { e.preventDefault(); setResult(null); setView('planner'); }}>Plan Trip</a>
            <a href="#" className="nav-link" onClick={(e) => { e.preventDefault(); setView('about'); }}>About</a>
            <button onClick={() => setDarkMode(!darkMode)} className="theme-toggle" aria-label="Toggle Dark Mode">
              {darkMode ? '☀️' : '🌙'}
            </button>
          </nav>
        </div>
      </header>
      <main className="container">
      {loading ? (
        <div className="skeleton-container">
          <div className="spinner-container">
            <div className="spinner"></div>
            <p>Crafting your itinerary...</p>
          </div>
          <div className="skeleton-summary">
            <div className="skeleton-line title"></div>
            <div className="skeleton-table-placeholder">
              <div className="skeleton-row"></div>
              <div className="skeleton-row"></div>
              <div className="skeleton-row"></div>
            </div>
          </div>
          <div className="skeleton-itinerary">
            <div className="skeleton-line title"></div>
            <div className="skeleton-table-placeholder">
              <div className="skeleton-row"></div>
              <div className="skeleton-row"></div>
              <div className="skeleton-row"></div>
              <div className="skeleton-row"></div>
            </div>
          </div>
        </div>
      ) : result ? (
        // Result View (Rendered below)
        <div className="output" ref={resultRef}>
          {/* ... result content ... */}
        </div>
      ) : view === 'about' ? (
        <About />
      ) : view === 'planner' ? (
        <>
          <h1>Plan Your Trip</h1>
          <form onSubmit={handleSubmit} className="travel-form">
            <div className="form-group">
              <label htmlFor="budget">Total Budget (₹)</label>
              <input type="number" id="budget" name="budget" required min="1" placeholder="e.g., 5000" value={formData.budget} onChange={handleInputChange} />
            </div>

            <div className="form-group">
              <label htmlFor="days">Number of Days</label>
              <input type="number" id="days" name="days" required min="1" placeholder="e.g., 3" value={formData.days} onChange={handleInputChange} />
            </div>

            <div className="form-group">
              <label htmlFor="originCity">Origin City</label>
              <input type="text" id="originCity" name="originCity" placeholder="e.g., Bangalore" value={formData.originCity} onChange={handleInputChange} list="city-options" />
            </div>

            <div className="form-group">
              <label htmlFor="state">State (Optional Filter)</label>
              <select id="state" value={selectedState} onChange={handleStateChange}>
                <option value="">All States</option>
                {Object.keys(CITIES_BY_STATE).sort().map(state => (
                  <option key={state} value={state}>{state}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="city">City</label>
              <input type="text" id="city" name="city" required placeholder="e.g., Delhi, Mumbai" value={formData.city} onChange={handleInputChange} list="city-options" />
              <datalist id="city-options">
                {(selectedState ? CITIES_BY_STATE[selectedState] : ALL_CITIES).map(city => (
                  <option key={city} value={city} />
                ))}
              </datalist>
            </div>

            <div className="form-group">
              <label>Activity Preferences</label>
              <div className="checkbox-group">
                <label><input type="checkbox" name="preferences" value="accommodation" onChange={handleCheckboxChange} /> Accommodation</label>
                <label><input type="checkbox" name="preferences" value="food" onChange={handleCheckboxChange} /> Food</label>
              </div>
            </div>

            <button type="submit" disabled={loading}>Generate Itinerary</button>
            <button type="button" className="btn-surprise" onClick={handleSurpriseMe} disabled={loading}>
              Surprise Me! 🎲
            </button>
          </form>

          {error && <div className="error-message">{error}</div>}
        </>
      ) : (
        // Landing View
        <>
          <Hero onStart={() => setView('planner')} />
          <Features />
          <HowItWorks />
          <BudgetCalculator />
          <PopularDestinations onSelect={handleCardClick} />
          <Testimonials />
          <CTASection onStart={() => setView('planner')} />
        </>
      )}

      {result && (
        <div className="output" ref={resultRef}>
          <button 
            onClick={() => setResult(null)}
            style={{ marginBottom: '20px', padding: '10px 20px', cursor: 'pointer', backgroundColor: '#646cff', color: 'white', border: 'none', borderRadius: '4px' }}
          >
            ← Back to Planner
          </button>
          <h3>Trip Summary</h3>
          <table className="summary-table">
            <tbody>
              <tr><td><strong>City:</strong></td><td>{result.city}</td></tr>
              <tr><td><strong>Total Budget:</strong></td><td>₹{result.total_budget}</td></tr>
              <tr><td><strong>Total Cost:</strong></td><td>₹{result.total_cost}</td></tr>
              <tr><td><strong>Remaining:</strong></td><td>₹{result.total_budget - result.total_cost}</td></tr>
            </tbody>
          </table>

          <h3>Estimated Travel Costs (from {formData.originCity || "Major Hubs"})</h3>
          <table className="summary-table">
            <thead>
              <tr>
                <th>Mode</th>
                <th>Estimated Fare</th>
                <th>Type / Note</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Bus 🚌</strong></td>
                <td>{result.travel_options.bus.available ? result.travel_options.bus.price : <span style={{color: '#991b1b'}}>N/A</span>}</td>
                <td>{result.travel_options.bus.label}</td>
              </tr>
              <tr>
                <td><strong>Train 🚆</strong></td>
                <td>{result.travel_options.train.available ? result.travel_options.train.price : <span style={{color: '#991b1b'}}>N/A</span>}</td>
                <td>{result.travel_options.train.label}</td>
              </tr>
              <tr>
                <td><strong>Flight ✈️</strong></td>
                <td>{result.travel_options.flight.price}</td>
                <td>{result.travel_options.flight.label}</td>
              </tr>
            </tbody>
          </table>

          <h3>Detailed Itinerary</h3>
          <table className="itinerary-table">
            <thead>
              <tr>
                <th>Day</th>
                <th>Activity</th>
                <th>Cost (₹)</th>
                <th>Hours</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(result.itinerary).map(([day, activities]) => (
                activities.length === 0 ? (
                  <tr key={day}><td colSpan="4">No activities planned for {day}</td></tr>
                ) : (
                  activities.map((act, index) => (
                    <tr key={`${day}-${index}`}>
                      <td>{day}</td>
                      <td>{act.activity}</td>
                      <td>{act.cost}</td>
                      <td>{act.hours}</td>
                    </tr>
                  ))
                )
              ))}
            </tbody>
          </table>
          <div style={{ display: 'flex', gap: '1rem' }}>
            <button className="btn-download" onClick={handleDownloadPDF} style={{ flex: 1 }}>
              Download PDF 📄
            </button>
            <button className="btn-share" onClick={handleShare} style={{ flex: 1 }}>
              {copySuccess ? 'Copied! ✅' : 'Share Itinerary 🔗'}
            </button>
          </div>
        </div>
      )}
      </main>
      <footer className="app-footer">
        <div className="footer-content">
          <div className="newsletter-section">
            <h3>Subscribe to our Newsletter</h3>
            <p>Get the latest travel tips and hidden gems delivered to your inbox.</p>
            {subscribed ? (
              <p className="success-message">Thanks for subscribing! 📬</p>
            ) : (
              <form onSubmit={handleSubscribe} className="newsletter-form">
                <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  <input 
                    type="email" 
                    name="email" 
                    placeholder="Enter your email" 
                    required 
                    className={emailError ? 'input-error' : ''}
                    onChange={() => setEmailError('')}
                  />
                  {emailError && <span className="newsletter-error">{emailError}</span>}
                </div>
                <button type="submit" disabled={subscribing}>
                  {subscribing ? <div className="btn-spinner"></div> : 'Subscribe'}
                </button>
              </form>
            )}
          </div>
          <p className="copyright">&copy; {new Date().getFullYear()} TravelGenie AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}

export default App
