import React, { useEffect } from "react"
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import Home from "./components/Home"
import Assessment from "./components/Assessment"
import WeeklyChallenge from "./components/WeeklyChallenge"
import socket from "./socket"

const App = () => {
  
  
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/assessment" element={<Assessment />} />
        <Route path="/weekly-challenge" element={<WeeklyChallenge />} />
      </Routes>
    </Router>
  )
}

export default App
