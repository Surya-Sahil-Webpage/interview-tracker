import { Routes, Route } from 'react-router-dom'

function App() {
  return (
    <Routes>
      <Route path="/" element={<h1 className="p-8 text-3xl font-bold text-blue-600">Interview Tracker</h1>} />
    </Routes>
  )
}

export default App