import { useState, useEffect, useRef } from 'react'
import './App.css'
import jsPDF from 'jspdf'
import 'jspdf-autotable'



const CITIES_BY_STATE = {
  "Andaman and Nicobar Islands": ["Port Blair"],
  "Andhra Pradesh": ["Tirupati", "Visakhapatnam"],
  "Arunachal Pradesh": ["Itanagar"],
  "Assam": ["Guwahati"],
  "Bihar": ["Bodh Gaya"],
  "Chandigarh": ["Chandigarh"],
  "Chhattisgarh": ["Raipur"],
  "Dadra and Nagar Haveli and Daman and Diu": ["Daman"],
  "Delhi": ["Delhi"],
  "Goa": ["Goa"],
  "Gujarat": ["Ahmedabad", "Rann of Kutch"],
  "Haryana": ["Kurukshetra"],
  "Himachal Pradesh": ["Shimla"],
  "Jammu and Kashmir": ["Srinagar"],
  "Jharkhand": ["Ranchi"],
  "Karnataka": ["Bangalore", "Mysore"],
  "Kerala": ["Kochi", "Munnar"],
  "Ladakh": ["Leh"],
  "Lakshadweep": ["Lakshadweep"],
  "Madhya Pradesh": ["Indore"],
  "Maharashtra": ["Mumbai", "Pune"],
  "Manipur": ["Imphal"],
  "Meghalaya": ["Shillong"],
  "Mizoram": ["Aizawl"],
  "Nagaland": ["Kohima"],
  "Odisha": ["Puri"],
  "Puducherry": ["Pondicherry"],
  "Punjab": ["Amritsar"],
  "Rajasthan": ["Jaipur", "Jaisalmer", "Udaipur"],
  "Sikkim": ["Gangtok"],
  "Tamil Nadu": ["Chennai", "Madurai"],
  "Telangana": ["Hyderabad"],
  "Tripura": ["Agartala"],
  "Uttar Pradesh": ["Agra", "Lucknow", "Varanasi"],
  "Uttarakhand": ["Rishikesh"],
  "West Bengal": ["Darjeeling", "Kolkata"]
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
  "Uttarakhand": "https://images.unsplash.com/photo-1589820296156-2454bb8a6d54?auto=format&fit=crop&w=1920&q=80",
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

function App() {
  const [formData, setFormData] = useState({
    budget: '',
    days: '',
    city: '',
    preferences: []
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [selectedState, setSelectedState] = useState('')
  const resultRef = useRef(null)

  useEffect(() => {
    if (result && resultRef.current) {
      resultRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [result])

  useEffect(() => {
    const imageUrl = STATE_IMAGES[selectedState] || STATE_IMAGES["default"]
    const img = new Image()
    img.src = imageUrl
    img.onload = () => {
      document.body.style.backgroundImage = `linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), url('${imageUrl}')`
    }
  }, [selectedState])

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

    const allPreferences = ["sightseeing", "food", "shopping"]
    
    const randomCity = ALL_CITIES[Math.floor(Math.random() * ALL_CITIES.length)]
    const randomDays = Math.floor(Math.random() * 4) + 2 // 2 - 5
    
    const randomPreferences = allPreferences.filter(() => Math.random() > 0.5)
    if (randomPreferences.length === 0) {
      randomPreferences.push(allPreferences[Math.floor(Math.random() * allPreferences.length)])
    }

    const newData = {
      budget: formData.budget,
      days: randomDays.toString(),
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
      startY: 50,
      head: [tableColumn],
      body: tableRows,
      theme: 'grid',
      headStyles: { fillColor: [79, 70, 229] }
    })

    doc.save(`${result.city}_Itinerary.pdf`)
  }

  return (
    <div className="container">
      <h1>Plan Your Trip</h1>
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
      ) : !result ? (
        <>
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
                <label><input type="checkbox" name="preferences" value="sightseeing" onChange={handleCheckboxChange} /> Sightseeing</label>
                <label><input type="checkbox" name="preferences" value="food" onChange={handleCheckboxChange} /> Food</label>
                <label><input type="checkbox" name="preferences" value="shopping" onChange={handleCheckboxChange} /> Shopping</label>
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
          <button className="btn-download" onClick={handleDownloadPDF}>
            Download PDF 📄
          </button>
        </div>
      )}
    </div>
  )
}

export default App
