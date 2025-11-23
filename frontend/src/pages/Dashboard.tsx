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
  CircularProgress,
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
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

// Sample cashflow data (will be replaced with API call later)
const cashflowData = [
  { month: 'Jan', inflow: 45000, outflow: 38000 },
  { month: 'Feb', inflow: 52000, outflow: 41000 },
  { month: 'Mar', inflow: 48000, outflow: 39000 },
  { month: 'Apr', inflow: 61000, outflow: 43000 },
  { month: 'May', inflow: 55000, outflow: 42000 },
  { month: 'Jun', inflow: 67000, outflow: 45000 },
]

const COLORS = ['#1976d2', '#2e7d32', '#f57c00', '#d32f2f', '#7b1fa2', '#0288d1']

interface ExpenseAnalytics {
  total_expenses: number
  expense_count: number
  average_expense: number
  by_category: Record<string, number>
  by_status: Record<string, number>
  recent_trend: Array<{ month: string; total: number }>
  top_merchants: Array<{ merchant: string; total: number; count: number }>
}

const Dashboard: React.FC = () => {
  const [loaded, setLoaded] = useState(false)
  const [analytics, setAnalytics] = useState<ExpenseAnalytics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setLoaded(true)
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await fetch('/api/v1/analytics/expenses')
      
      if (!response.ok) {
        throw new Error('Failed to fetch analytics')
      }
      
      const data = await response.json()
      setAnalytics(data)
    } catch (err) {
      console.error('Error fetching analytics:', err)
      setError('Failed to load analytics')
    } finally {
      setLoading(false)
    }
  }

  // Prepare category data for pie chart
  const categoryData = analytics?.by_category 
    ? Object.entries(analytics.by_category).map(([name, value]) => ({ name, value }))
    : []

  const stats = [
    {
      title: 'Total Expenses',
      value: analytics ? `$${analytics.total_expenses.toLocaleString()}` : '$0',
      change: '+12.5%',
      trend: 'up',
      icon: <Receipt fontSize="large" />,
      color: '#1976d2',
      bgColor: '#e3f2fd',
    },
    {
      title: 'Expense Count',
      value: analytics?.expense_count.toString() || '0',
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
      title: 'Avg Expense',
      value: analytics ? `$${analytics.average_expense.toLocaleString()}` : '$0',
      change: '+5.2%',
      trend: 'up',
      icon: <AccountBalance fontSize="large" />,
      color: '#f57c00',
      bgColor: '#fff3e0',
    },
  ]

  const recentExpenses = analytics?.top_merchants.slice(0, 4).map((m, idx) => ({
    id: idx + 1,
    merchant: m.merchant,
    amount: m.total,
    category: 'Various',
    status: 'Approved',
  })) || []

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress size={60} />
      </Box>
    )
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography color="error">{error}</Typography>
      </Box>
    )
  }

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
              onClick={fetchAnalytics}
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
        {/* Category Breakdown Pie Chart */}
        <Grid item xs={12} md={4}>
          <Paper elevation={2} sx={{ p: 3, borderRadius: 2, height: 380 }}>
            <Typography variant="h6" sx={{ fontWeight: 700, mb: 2, color: '#1976d2' }}>
              Expenses by Category
            </Typography>
            {categoryData.length > 0 ? (
              <ResponsiveContainer width="100%" height={280}>
                <PieChart>
                  <Pie
                    data={categoryData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {categoryData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value: number) => `$${value.toLocaleString()}`} />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 280 }}>
                <Typography color="text.secondary">No expense data</Typography>
              </Box>
            )}
          </Paper>
        </Grid>

        {/* Monthly Trend */}
        <Grid item xs={12} md={8}>
          <Paper elevation={2} sx={{ p: 3, borderRadius: 2 }}>
            <Typography variant="h6" sx={{ fontWeight: 700, mb: 3, color: '#1976d2' }}>
              {analytics?.recent_trend && analytics.recent_trend.length > 1 ? 'Expense Trend' : 'Cashflow Trend (Demo)'}
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={analytics?.recent_trend && analytics.recent_trend.length > 1 ? analytics.recent_trend : cashflowData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                <XAxis dataKey="month" stroke="#757575" />
                <YAxis stroke="#757575" />
                <Tooltip
                  contentStyle={{
                    background: '#ffffff',
                    border: '1px solid #e0e0e0',
                    borderRadius: '8px',
                  }}
                  formatter={(value: number) => `$${value.toLocaleString()}`}
                />
                <Legend />
                {analytics?.recent_trend && analytics.recent_trend.length > 1 ? (
                  <Line type="monotone" dataKey="total" stroke="#1976d2" strokeWidth={3} name="Total Expenses" />
                ) : (
                  <>
                    <Line type="monotone" dataKey="inflow" stroke="#2e7d32" strokeWidth={3} name="Inflow" />
                    <Line type="monotone" dataKey="outflow" stroke="#d32f2f" strokeWidth={3} name="Outflow" />
                  </>
                )}
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>

      {/* Agent Activity and Top Merchants */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 3, height: '100%', borderRadius: 2 }}>
            <Typography variant="h6" sx={{ fontWeight: 700, mb: 3, color: '#1976d2' }}>
              Top Merchants
            </Typography>
            {analytics?.top_merchants && analytics.top_merchants.length > 0 ? (
              <Box>
                {analytics.top_merchants.slice(0, 5).map((merchant, index) => (
                  <Box key={index} sx={{ mb: 2, pb: 2, borderBottom: index < 4 ? '1px solid #e0e0e0' : 'none' }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body1" sx={{ fontWeight: 600 }}>{merchant.merchant}</Typography>
                      <Typography variant="body1" sx={{ color: '#1976d2', fontWeight: 700 }}>
                        ${merchant.total.toLocaleString()}
                      </Typography>
                    </Box>
                    <Typography variant="body2" sx={{ color: '#757575' }}>
                      {merchant.count} transactions
                    </Typography>
                  </Box>
                ))}
              </Box>
            ) : (
              <Typography color="text.secondary">No merchant data yet</Typography>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
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
