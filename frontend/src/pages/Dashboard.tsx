import React from 'react'
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  LinearProgress,
  Chip,
} from '@mui/material'
import {
  TrendingUp,
  TrendingDown,
  Receipt,
  Description,
  Security,
  AccountBalance,
} from '@mui/icons-material'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

// Sample data for charts
const cashflowData = [
  { month: 'Jan', inflow: 45000, outflow: 38000 },
  { month: 'Feb', inflow: 52000, outflow: 41000 },
  { month: 'Mar', inflow: 48000, outflow: 39000 },
  { month: 'Apr', inflow: 61000, outflow: 43000 },
  { month: 'May', inflow: 55000, outflow: 42000 },
  { month: 'Jun', inflow: 67000, outflow: 45000 },
]

const Dashboard: React.FC = () => {
  const stats = [
    {
      title: 'Total Expenses',
      value: '$48,392',
      change: '+12.5%',
      trend: 'up',
      icon: <Receipt fontSize="large" />,
      color: '#1976d2',
    },
    {
      title: 'Invoices Sent',
      value: '24',
      change: '+8',
      trend: 'up',
      icon: <Description fontSize="large" />,
      color: '#2e7d32',
    },
    {
      title: 'Fraud Alerts',
      value: '3',
      change: '-2',
      trend: 'down',
      icon: <Security fontSize="large" />,
      color: '#d32f2f',
    },
    {
      title: 'Cashflow Position',
      value: '$152K',
      change: '+$18K',
      trend: 'up',
      icon: <AccountBalance fontSize="large" />,
      color: '#7b1fa2',
    },
  ]

  const recentExpenses = [
    { id: 1, merchant: 'Office Depot', amount: 245.50, category: 'Office Supplies', status: 'Approved' },
    { id: 2, merchant: 'Amazon Web Services', amount: 892.00, category: 'Software', status: 'Approved' },
    { id: 3, merchant: 'Delta Airlines', amount: 1250.00, category: 'Travel', status: 'Under Review' },
    { id: 4, merchant: 'Starbucks', amount: 45.80, category: 'Meals', status: 'Approved' },
  ]

  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight={700}>
        Dashboard Overview
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Real-time insights powered by AI agents
      </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card elevation={2}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Box sx={{ color: stat.color }}>{stat.icon}</Box>
                  <Chip
                    label={stat.change}
                    size="small"
                    color={stat.trend === 'up' ? 'success' : 'error'}
                    icon={stat.trend === 'up' ? <TrendingUp /> : <TrendingDown />}
                  />
                </Box>
                <Typography variant="h4" fontWeight={700}>
                  {stat.value}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {stat.title}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Charts */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={8}>
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom fontWeight={600}>
              Cashflow Trend (6 Months)
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={cashflowData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="inflow" stroke="#2e7d32" strokeWidth={2} name="Inflow" />
                <Line type="monotone" dataKey="outflow" stroke="#d32f2f" strokeWidth={2} name="Outflow" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper elevation={2} sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom fontWeight={600}>
              Agent Activity
            </Typography>
            <Box sx={{ mt: 3 }}>
              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" gutterBottom>Expense Classifier</Typography>
                <LinearProgress variant="determinate" value={92} color="primary" />
                <Typography variant="caption" color="text.secondary">92% accuracy</Typography>
              </Box>
              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" gutterBottom>Invoice Agent</Typography>
                <LinearProgress variant="determinate" value={87} color="success" />
                <Typography variant="caption" color="text.secondary">87% automation rate</Typography>
              </Box>
              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" gutterBottom>Fraud Analyzer</Typography>
                <LinearProgress variant="determinate" value={95} color="error" />
                <Typography variant="caption" color="text.secondary">95% detection rate</Typography>
              </Box>
              <Box>
                <Typography variant="body2" gutterBottom>Cashflow Forecast</Typography>
                <LinearProgress variant="determinate" value={89} color="secondary" />
                <Typography variant="caption" color="text.secondary">89% accuracy (MAPE: 11%)</Typography>
              </Box>
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Recent Expenses Table */}
      <Paper elevation={2} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom fontWeight={600}>
          Recent Expenses
        </Typography>
        <Box sx={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '2px solid #e0e0e0' }}>
                <th style={{ textAlign: 'left', padding: '12px' }}>Merchant</th>
                <th style={{ textAlign: 'left', padding: '12px' }}>Amount</th>
                <th style={{ textAlign: 'left', padding: '12px' }}>Category</th>
                <th style={{ textAlign: 'left', padding: '12px' }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {recentExpenses.map((expense) => (
                <tr key={expense.id} style={{ borderBottom: '1px solid #f0f0f0' }}>
                  <td style={{ padding: '12px' }}>{expense.merchant}</td>
                  <td style={{ padding: '12px' }}>${expense.amount.toFixed(2)}</td>
                  <td style={{ padding: '12px' }}>
                    <Chip label={expense.category} size="small" />
                  </td>
                  <td style={{ padding: '12px' }}>
                    <Chip
                      label={expense.status}
                      size="small"
                      color={expense.status === 'Approved' ? 'success' : 'warning'}
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
