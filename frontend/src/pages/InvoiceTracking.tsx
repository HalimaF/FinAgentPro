import React, { useState, useEffect } from 'react'
import {
  Box,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Button,
  IconButton,
  Menu,
  MenuItem,
  CircularProgress,
  Tabs,
  Tab,
  Card,
  CardContent,
  Grid,
} from '@mui/material'
import {
  Download,
  MoreVert,
  Send,
  CheckCircle,
  Warning,
  Schedule,
} from '@mui/icons-material'

interface Invoice {
  invoice_id: string
  invoice_number: string
  client_name: string
  total_amount: number
  due_date: string
  payment_status: string
  status: string
  created_date: string
}

const InvoiceTracking: React.FC = () => {
  const [invoices, setInvoices] = useState<Invoice[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [tabValue, setTabValue] = useState(0)
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const [selectedInvoice, setSelectedInvoice] = useState<Invoice | null>(null)

  useEffect(() => {
    fetchInvoices()
  }, [tabValue])

  const fetchInvoices = async () => {
    try {
      setLoading(true)
      setError(null)
      
      const statusFilter = tabValue === 1 ? 'pending' : tabValue === 2 ? 'paid' : tabValue === 3 ? 'overdue' : undefined
      const url = statusFilter ? `/api/v1/invoices?status=${statusFilter}` : '/api/v1/invoices'
      
      const response = await fetch(url)
      
      if (!response.ok) {
        throw new Error('Failed to fetch invoices')
      }
      
      const data = await response.json()
      setInvoices(data)
    } catch (err) {
      console.error('Error fetching invoices:', err)
      setError('Failed to load invoices')
    } finally {
      setLoading(false)
    }
  }

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>, invoice: Invoice) => {
    setAnchorEl(event.currentTarget)
    setSelectedInvoice(invoice)
  }

  const handleMenuClose = () => {
    setAnchorEl(null)
    setSelectedInvoice(null)
  }

  const handleStatusUpdate = async (status: string) => {
    if (!selectedInvoice) return
    
    try {
      const response = await fetch(`/api/v1/invoices/${selectedInvoice.invoice_id}/status?payment_status=${status}`, {
        method: 'PUT',
      })
      
      if (!response.ok) {
        throw new Error('Failed to update status')
      }
      
      await fetchInvoices()
    } catch (err) {
      console.error('Error updating status:', err)
    } finally {
      handleMenuClose()
    }
  }

  const handleDownload = (invoice: Invoice) => {
    window.open(`/api/v1/invoices/${invoice.invoice_id}/pdf`, '_blank')
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'paid':
        return <CheckCircle sx={{ color: '#2e7d32' }} />
      case 'overdue':
        return <Warning sx={{ color: '#d32f2f' }} />
      default:
        return <Schedule sx={{ color: '#f57c00' }} />
    }
  }

  const getStatusColor = (status: string): "default" | "success" | "error" | "warning" => {
    switch (status) {
      case 'paid':
        return 'success'
      case 'overdue':
        return 'error'
      default:
        return 'warning'
    }
  }

  const stats = [
    {
      title: 'Total Invoices',
      value: invoices.length,
      icon: <Send sx={{ color: '#1976d2', fontSize: 40 }} />,
    },
    {
      title: 'Pending Payment',
      value: invoices.filter(inv => inv.payment_status === 'pending').length,
      icon: <Schedule sx={{ color: '#f57c00', fontSize: 40 }} />,
    },
    {
      title: 'Paid',
      value: invoices.filter(inv => inv.payment_status === 'paid').length,
      icon: <CheckCircle sx={{ color: '#2e7d32', fontSize: 40 }} />,
    },
    {
      title: 'Overdue',
      value: invoices.filter(inv => inv.payment_status === 'overdue').length,
      icon: <Warning sx={{ color: '#d32f2f', fontSize: 40 }} />,
    },
  ]

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
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 700, color: '#1976d2', mb: 1 }}>
          Invoice Tracking
        </Typography>
        <Typography variant="body1" sx={{ color: '#757575' }}>
          Monitor invoice status and payment history
        </Typography>
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {stats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card elevation={2}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Box>
                    <Typography variant="h4" sx={{ fontWeight: 700, color: '#1976d2' }}>
                      {stat.value}
                    </Typography>
                    <Typography variant="body2" sx={{ color: '#757575', mt: 1 }}>
                      {stat.title}
                    </Typography>
                  </Box>
                  {stat.icon}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Tabs */}
      <Paper elevation={2} sx={{ borderRadius: 2 }}>
        <Tabs
          value={tabValue}
          onChange={(_, newValue) => setTabValue(newValue)}
          sx={{ borderBottom: 1, borderColor: 'divider', px: 2 }}
        >
          <Tab label="All" />
          <Tab label="Pending" />
          <Tab label="Paid" />
          <Tab label="Overdue" />
        </Tabs>

        {/* Invoice Table */}
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: 700 }}>Invoice #</TableCell>
                <TableCell sx={{ fontWeight: 700 }}>Client</TableCell>
                <TableCell sx={{ fontWeight: 700 }}>Amount</TableCell>
                <TableCell sx={{ fontWeight: 700 }}>Due Date</TableCell>
                <TableCell sx={{ fontWeight: 700 }}>Status</TableCell>
                <TableCell sx={{ fontWeight: 700 }}>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {invoices.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} align="center" sx={{ py: 4 }}>
                    <Typography color="text.secondary">No invoices found</Typography>
                  </TableCell>
                </TableRow>
              ) : (
                invoices.map((invoice) => (
                  <TableRow key={invoice.invoice_id} hover>
                    <TableCell sx={{ fontWeight: 600 }}>{invoice.invoice_number}</TableCell>
                    <TableCell>{invoice.client_name}</TableCell>
                    <TableCell sx={{ fontWeight: 700, color: '#1976d2' }}>
                      ${invoice.total_amount.toLocaleString()}
                    </TableCell>
                    <TableCell>{new Date(invoice.due_date).toLocaleDateString()}</TableCell>
                    <TableCell>
                      <Chip
                        icon={getStatusIcon(invoice.payment_status)}
                        label={invoice.payment_status.toUpperCase()}
                        color={getStatusColor(invoice.payment_status)}
                        size="small"
                        sx={{ fontWeight: 600 }}
                      />
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', gap: 1 }}>
                        <IconButton
                          size="small"
                          onClick={() => handleDownload(invoice)}
                          sx={{ color: '#1976d2' }}
                        >
                          <Download />
                        </IconButton>
                        <IconButton
                          size="small"
                          onClick={(e) => handleMenuOpen(e, invoice)}
                        >
                          <MoreVert />
                        </IconButton>
                      </Box>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Context Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={() => handleStatusUpdate('pending')}>
          Mark as Pending
        </MenuItem>
        <MenuItem onClick={() => handleStatusUpdate('paid')}>
          Mark as Paid
        </MenuItem>
        <MenuItem onClick={() => handleStatusUpdate('overdue')}>
          Mark as Overdue
        </MenuItem>
      </Menu>
    </Box>
  )
}

export default InvoiceTracking
