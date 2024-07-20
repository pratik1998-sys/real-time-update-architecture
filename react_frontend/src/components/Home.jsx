import React from "react"
import { Link } from "react-router-dom"

const Home = () => {
  return (
    <div>
      <h1>Home</h1>
      <nav>
        <ul>
          <li>
            <Link to="/assessment">Assessment</Link>
          </li>
          <li>
            <Link to="/weekly-challenge">Weekly Challenge</Link>
          </li>
        </ul>
      </nav>
    </div>
  )
}

export default Home
