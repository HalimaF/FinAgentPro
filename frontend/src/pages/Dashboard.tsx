import React, { useState, useEffect } from 'react'
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  IconButton,
  Fade,
  Grow,
} from '@mui/material'
import {
  TrendingUp,
  TrendingDown,
  Receipt,
  Description,
  Security,
  AccountBalance,
  Refresh,
} from '@mui/icons-material'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

// Sample data
const cashflowData = [
  { month: 'Jan', inflow: 45000, outflow: 38000 },
  { month: 'Feb', inflow: 52000, outflow: 41000 },
  { month: 'Mar', inflow: 48000, outflow: 39000 },
  { month: 'Apr', inflow: 61000, outflow: 43000 },
  { month: 'May', inflow: 55000, outflow: 42000 },
  { month: 'Jun', inflow: 67000, outflow: 45000 },
]

const Dashboard: React.FC = () => {
  const [loaded, setLoaded] = useState(false)

  useEffect(() => {
    setLoaded(true)
  }, [])

  const stats = [
    {
      title: 'Total Expenses',
      value: '$48,392',
      change: '+12.5%',
      trend: 'up',
      icon: <Receipt fontSize="large" />,
      color: '#1976d2',
      bgColor: '#e3f2fd',
    },
    {
      title: 'Invoices Sent',
      value: '24',
      change: '+8',
      trend: 'up',
      icon: <Description fontSize="large" />,
      color: '#2e7d32',
      bgColor: '#e8f5e9',
    },
    {
      title: 'Fraud Alerts',
      value: '3',
      change: '-2',
      trend: 'down',
      icon: <Security fontSize="large" />,
      color: '#d32f2f',
      bgColor: '#ffebee',
    },
    {
      title: 'Cashflow Position',
      value: '$152K',
      change: '+$18K',
      trend: 'up',
      icon: <AccountBalance fontSize="large" />,
      color: '#f57c00',
      bgColor: '#fff3e0',
    },
  ]

  const recentExpenses = [
    { id: 1, merchant: 'Office Depot', amount: 245.50, category: 'Office Supplies', status: 'Approved' },
    { id: 2, merchant: 'Amazon Web Services', amount: 892.00, category: 'Software', status: 'Approved' },
    { id: 3, merchant: 'Delta Airlines', amount: 1250.00, category: 'Travel', status: 'Under Review' },
    { id: 4, merchant: 'Starbucks', amount: 45.80, category: 'Meals', status: 'Approved' },
  ]

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Fade in={loaded} timeout={400}>
        <Box sx={{ mb: 4 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
            <Typography
              variant="h4"
              sx={{
                fontWeight: 700,
                color: '#1976d2',
              }}
            >
              Dashboard Overview
            </Typography>
            <IconButton
              sx={{
                '&:hover': {
                  transform: 'rotate(180deg)',
                },
                transition: 'all 0.5s ease',
              }}
            >
              <Refresh sx={{ color: '#1976d2' }} />
            </IconButton>
          </Box>
          <Typography variant="body1" sx={{ color: '#757575' }}>
            Real-time insights powered by AI agents
          </Typography>
        </Box>
      </Fade>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Grow in={loaded} timeout={400 + index * 100}>
              <Card
                elevation={2}
                sx={{
                  borderRadius: 2,
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: '0 8px 16px rgba(0,0,0,0.1)',
                  },
                }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Box
                      sx={{
                        width: 56,
                        height: 56,
                        borderRadius: 2,
                        background: stat.bgColor,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: stat.color,
                      }}
                    >
                      {stat.icon}
                    </Box>
                    <Chip
                      label={stat.change}
                      size="small"
                      icon={stat.trend === 'up' ? <TrendingUp /> : <TrendingDown />}
                      color={stat.trend === 'up' ? 'success' : 'error'}
                      sx={{ fontWeight: 600 }}
                    />
                  </Box>
                  <Typography
                    variant="h4"
                    sx={{
                      fontWeight: 700,
                      color: stat.color,
                      mb: 0.5,
                    }}
                  >
                    {stat.value}
                  </Typography>
                  <Typography variant="body2" sx={{ color: '#757575', fontWeight: 500 }}>
                    {stat.title}
                  </Typography>
                </CardContent>
              </Card>
            </Grow>
          </Grid>
        ))}
      </Grid>

      {/* Charts */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={8}>
          <Paper elevation={2} sx={{ p: 3, borderRadius: 2 }}>
            <Typography variant="h6" sx={{ fontWeight: 700, mb: 3, color: '#1976d2' }}>
              Cashflow Trend (6 Months)
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={cashflowData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                <XAxis dataKey="month" stroke="#757575" />
                <YAxis stroke="#757575" />
                <Tooltip
                  contentStyle={{
                    background: '#ffffff',
                    border: '1px solid #e0e0e0',
                    borderRadius: '8px',
                  }}
                />
                <Legend />
                <Line type="monotone" dataKey="inflow" stroke="#2e7d32" strokeWidth={3} name="Inflow" />
                <Line type="monotone" dataKey="outflow" stroke="#d32f2f" strokeWidth={3} name="Outflow" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper elevation={2} sx={{ p: 3, height: '100%', borderRadius: 2 }}>
            <Typography variant="h6" sx={{ fontWeight: 700, mb: 3, color: '#1976d2' }}>
              Agent Activity
            </Typography>
            <Box sx={{ mt: 3 }}>
              {[
                { name: 'Expense Classifier', value: 92, color: '#1976d2' },
                { name: 'Invoice Agent', value: 87, color: '#2e7d32' },
                { name: 'Fraud Analyzer', value: 95, color: '#d32f2f' },
                { name: 'Cashflow Forecast', value: 89, color: '#f57c00' },
              ].map((agent, index) => (
                <Box key={index} sx={{ mb: 3 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2" sx={{ fontWeight: 600 }}>{agent.name}</Typography>
                    <Typography variant="body2" sx={{ color: agent.color, fontWeight: 700 }}>{agent.value}%</Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={agent.value}
                    sx={{
                      height: 8,
                      borderRadius: 4,
                      backgroundColor: '#e0e0e0',
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: agent.color,
                        borderRadius: 4,
                      }
                    }}
                  />
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Recent Expenses Table */}
      <Paper elevation={2} sx={{ p: 3, borderRadius: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 700, mb: 3, color: '#1976d2' }}>
          Recent Expenses
        </Typography>
        <Box sx={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #e0e0e0' }}>
                <th style={{ textAlign: 'left', padding: '12px', color: '#757575', fontWeight: 600 }}>Merchant</th>
                <th style={{ textAlign: 'left', padding: '12px', color: '#757575', fontWeight: 600 }}>Amount</th>
                <th style={{ textAlign: 'left', padding: '12px', color: '#757575', fontWeight: 600 }}>Category</th>
                <th style={{ textAlign: 'left', padding: '12px', color: '#757575', fontWeight: 600 }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {recentExpenses.map((expense) => (
                <tr
                  key={expense.id}
                  style={{
                    borderBottom: '1px solid #f5f5f5',
                    transition: 'background 0.2s ease',
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.background = '#f5f5f5'}
                  onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                >
                  <td style={{ padding: '16px', fontWeight: 600 }}>{expense.merchant}</td>
                  <td style={{ padding: '16px', fontWeight: 700, color: '#1976d2' }}>${expense.amount.toFixed(2)}</td>
                  <td style={{ padding: '16px' }}>
                    <Chip
                      label={expense.category}
                      size="small"
                      sx={{
                        backgroundColor: '#e3f2fd',
                        color: '#1976d2',
                        fontWeight: 600,
                      }}
                    />
                  </td>
                  <td style={{ padding: '16px' }}>
                    <Chip
                      label={expense.status}
                      size="small"
                      color={expense.status === 'Approved' ? 'success' : 'warning'}
                      sx={{ fontWeight: 600 }}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Box>
      </Paper>
    </Box>
  )
}

export default Dashboard
