import React, { useState } from 'react'
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  Chip,
  Divider,
} from '@mui/material'
import { Send, Description, Download, AttachMoney } from '@mui/icons-material'
import axios from 'axios'
import toast from 'react-hot-toast'

const InvoiceCreation: React.FC = () => {
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [invoice, setInvoice] = useState<any>(null)

  const handleCreateInvoice = async () => {
    if (!input.trim()) {
      toast.error('Please enter invoice details')
      return
    }

    setLoading(true)
    const toastId = toast.loading('Creating invoice...')

    try {
      const response = await axios.post(
        '/api/v1/invoices',
        {
          description: input,
          send_email: false,
        },
        {
          headers: {
            'Authorization': 'Bearer demo_token',
          },
        }
      )

      setInvoice(response.data)
      toast.success('Invoice created successfully!', { id: toastId })
      setInput('')
    } catch (error) {
      console.error(error)
      toast.error('Failed to create invoice', { id: toastId })
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleCreateInvoice()
    }
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight={700}>
        Invoice Creation
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Create professional invoices using natural language
      </Typography>

      <Grid container spacing={3}>
        {/* Input Section */}
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom fontWeight={600}>
              Describe Your Invoice
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Example: "Create invoice for Acme Corp for website redesign, $8,500, due in 30 days"
            </Typography>

            <TextField
              fullWidth
              multiline
              rows={6}
              placeholder="Type your invoice details in natural language..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              sx={{ mb: 2 }}
            />

            <Button
              fullWidth
              variant="contained"
              size="large"
              onClick={handleCreateInvoice}
              disabled={loading}
              startIcon={<Send />}
            >
              {loading ? 'Creating...' : 'Create Invoice'}
            </Button>

            <Box sx={{ mt: 3 }}>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Quick Templates:
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                <Chip
                  label="Consulting Service"
                  size="small"
                  onClick={() => setInput('Create invoice for ABC Corp for consulting services, $2,500, due net 30')}
                />
                <Chip
                  label="Software Development"
                  size="small"
                  onClick={() => setInput('Invoice for XYZ Inc for software development project, $15,000, payment terms net 45')}
                />
                <Chip
                  label="Design Work"
                  size="small"
                  onClick={() => setInput('Bill TechStart for UI/UX design work, $3,750, due in 30 days')}
                />
              </Box>
            </Box>
          </Paper>
        </Grid>

        {/* Output Section */}
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 3, minHeight: 400 }}>
            <Typography variant="h6" gutterBottom fontWeight={600}>
              Generated Invoice
            </Typography>

            {!invoice ? (
              <Box sx={{ textAlign: 'center', py: 8 }}>
                <Description sx={{ fontSize: 64, color: '#bdbdbd', mb: 2 }} />
                <Typography variant="body1" color="text.secondary">
                  Your invoice will appear here
                </Typography>
              </Box>
            ) : (
              <Card variant="outlined">
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Box>
                      <Typography variant="overline" color="text.secondary">
                        Invoice Number
                      </Typography>
                      <Typography variant="h6" fontWeight={600}>
                        {invoice.invoice_number}
                      </Typography>
                    </Box>
                    <Chip label={invoice.status} color="primary" />
                  </Box>

                  <Divider sx={{ my: 2 }} />

                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" color="text.secondary">
                      Client
                    </Typography>
                    <Typography variant="body1" fontWeight={600}>
                      {invoice.client_name}
                    </Typography>
                    {invoice.client_email && (
                      <Typography variant="body2" color="text.secondary">
                        {invoice.client_email}
                      </Typography>
                    )}
                  </Box>

                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" color="text.secondary">
                      Due Date
                    </Typography>
                    <Typography variant="body1">
                      {invoice.due_date || 'Upon receipt'}
                    </Typography>
                  </Box>

                  <Divider sx={{ my: 2 }} />

                  <Box sx={{ mb: 1 }}>
                    <Typography variant="body2" color="text.secondary">
                      Items
                    </Typography>
                    {invoice.items?.map((item: any, index: number) => (
                      <Box key={index} sx={{ display: 'flex', justifyContent: 'space-between', py: 1 }}>
                        <Typography variant="body2">
                          {item.description} (×{item.quantity})
                        </Typography>
                        <Typography variant="body2">
                          ${item.unit_price?.toFixed(2)}
                        </Typography>
                      </Box>
                    ))}
                  </Box>

                  <Divider sx={{ my: 2 }} />

                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2">Subtotal:</Typography>
                    <Typography variant="body2">${invoice.subtotal?.toFixed(2)}</Typography>
                  </Box>

                  {invoice.tax_amount > 0 && (
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2">Tax:</Typography>
                      <Typography variant="body2">${invoice.tax_amount?.toFixed(2)}</Typography>
                    </Box>
                  )}

                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
                    <Typography variant="h6" fontWeight={700}>Total:</Typography>
                    <Typography variant="h6" fontWeight={700} color="primary">
                      ${invoice.total_amount?.toFixed(2)}
                    </Typography>
                  </Box>

                  <Box sx={{ mt: 3, display: 'flex', gap: 1 }}>
                    <Button
                      variant="outlined"
                      size="small"
                      fullWidth
                      startIcon={<Download />}
                      href={invoice.pdf_url}
                      target="_blank"
                    >
                      Download PDF
                    </Button>
                    <Button
                      variant="contained"
                      size="small"
                      fullWidth
                      startIcon={<AttachMoney />}
                      href={invoice.payment_url}
                      target="_blank"
                    >
                      Payment Link
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  )
}

export default InvoiceCreation
