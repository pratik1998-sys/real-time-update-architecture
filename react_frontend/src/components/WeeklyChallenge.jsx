import React, { useEffect, useState } from "react"
import webSocketService from "../socket"
import socket from "../socket"

const WeeklyChallenge = () => {
  const [messages, setMessages] = useState([])

  useEffect(() => {
    const handleTopic1Event = (data) => {
      console.log("Received data for weekly_challenge_topic1_event:", data)
      setMessages((prev) => [
        ...prev,
        { topic: "weekly_challenge_topic1", data },
      ])
    }

    const handleTopic2Event = (data) => {
      console.log("Received data for weekly_challenge_topic2_event:", data)
      setMessages((prev) => [
        ...prev,
        { topic: "weekly_challenge_topic1", data },
      ])
    }

    socket.on("weekly_challenge_topic1_event_back", handleTopic1Event)
    socket.on("weekly_challenge_topic2_event_back", handleTopic2Event)

    return () => {
      socket.off(
        "weekly_challenge_topic1_event_back"
      )
      socket.off(
        "weekly_challenge_topic2_event_back"
      )
    }
  }, [])

  

  const sendMessage = (topic) => {
    const message = { id: Math.random(),topic:topic, data: `Message for ${topic}` }
    socket.emit(topic, message)
  }

  return (
    <div>
      <h1>Weekly Challenge Module</h1>
      <button onClick={() => sendMessage("weekly_challenge_topic1_event")}>
        Send to Topic 1
      </button>
      <button onClick={() => sendMessage("weekly_challenge_topic2_event")}>
        Send to Topic 2
      </button>
      <ul>
        {messages.map((msg, index) => (
          <li key={index}>
            {msg.topic}: {JSON.stringify(msg.data)}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default WeeklyChallenge
