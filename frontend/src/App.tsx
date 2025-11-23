import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Box } from '@mui/material'

// Layout
import Layout from './components/Layout/Layout'

// Pages
import Dashboard from './pages/Dashboard'
import ExpenseUpload from './pages/ExpenseUpload'
import InvoiceCreation from './pages/InvoiceCreation'
import InvoiceTracking from './pages/InvoiceTracking'
import FraudAlerts from './pages/FraudAlerts'
import CashflowForecast from './pages/CashflowForecast'
import VoiceAssistant from './pages/VoiceAssistant'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="expenses" element={<ExpenseUpload />} />
          <Route path="invoices" element={<InvoiceCreation />} />
          <Route path="invoices/track" element={<InvoiceTracking />} />
          <Route path="fraud" element={<FraudAlerts />} />
          <Route path="cashflow" element={<CashflowForecast />} />
          <Route path="voice" element={<VoiceAssistant />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
