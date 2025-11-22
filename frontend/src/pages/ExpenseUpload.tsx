import React, { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import {
  Box,
  Typography,
  Paper,
  Button,
  Grid,
  Card,
  CardContent,
  Chip,
  LinearProgress,
  Alert,
} from '@mui/material'
import { CloudUpload, CheckCircle, Error as ErrorIcon, Visibility } from '@mui/icons-material'
import axios from 'axios'
import toast from 'react-hot-toast'

const ExpenseUpload: React.FC = () => {
  const [uploading, setUploading] = useState(false)
  const [processedExpenses, setProcessedExpenses] = useState<any[]>([])

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setUploading(true)
    const toastId = toast.loading('Processing receipts...')

    try {
      const uploadPromises = acceptedFiles.map(async (file) => {
        const formData = new FormData()
        formData.append('file', file)

        const response = await axios.post('/api/v1/expenses/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': 'Bearer demo_token',
          },
        })

        return response.data
      })

      const results = await Promise.all(uploadPromises)
      setProcessedExpenses((prev) => [...prev, ...results])
      
      toast.success(`${acceptedFiles.length} receipt(s) processed successfully!`, { id: toastId })
    } catch (error) {
      console.error(error)
      toast.error('Failed to process receipts', { id: toastId })
    } finally {
      setUploading(false)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg'],
      'application/pdf': ['.pdf'],
    },
    multiple: true,
  })

  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight={700}>
        Expense Upload
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Upload receipts for AI-powered classification and fraud detection
      </Typography>

      {/* Upload Area */}
      <Paper
        {...getRootProps()}
        elevation={3}
        sx={{
          p: 6,
          mb: 4,
          textAlign: 'center',
          cursor: 'pointer',
          backgroundColor: isDragActive ? '#e3f2fd' : '#fafafa',
          border: '2px dashed',
          borderColor: isDragActive ? '#1976d2' : '#bdbdbd',
          transition: 'all 0.3s',
          '&:hover': {
            backgroundColor: '#f5f5f5',
            borderColor: '#1976d2',
          },
        }}
      >
        <input {...getInputProps()} />
        <CloudUpload sx={{ fontSize: 64, color: '#1976d2', mb: 2 }} />
        {isDragActive ? (
          <Typography variant="h6">Drop the files here...</Typography>
        ) : (
          <>
            <Typography variant="h6" gutterBottom>
              Drag & drop receipts here, or click to select files
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Supports JPG, PNG, PDF
            </Typography>
          </>
        )}
      </Paper>

      {uploading && (
        <Box sx={{ mb: 4 }}>
          <Alert severity="info" icon={false}>
            <Typography variant="body2" gutterBottom>Processing receipts...</Typography>
            <LinearProgress />
          </Alert>
        </Box>
      )}

      {/* Processed Expenses */}
      {processedExpenses.length > 0 && (
        <>
          <Typography variant="h5" gutterBottom fontWeight={600} sx={{ mb: 3 }}>
            Processed Expenses
          </Typography>
          <Grid container spacing={3}>
            {processedExpenses.map((expense) => (
              <Grid item xs={12} md={6} key={expense.expense_id}>
                <Card elevation={2}>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                      <Typography variant="h6" fontWeight={600}>
                        ${expense.amount?.toFixed(2) || 'N/A'}
                      </Typography>
                      {expense.status === 'approved' ? (
                        <Chip icon={<CheckCircle />} label="Approved" color="success" />
                      ) : (
                        <Chip icon={<ErrorIcon />} label="Review Needed" color="warning" />
                      )}
                    </Box>

                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">Merchant</Typography>
                      <Typography variant="body1">{expense.merchant || 'Unknown'}</Typography>
                    </Box>

                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">Category</Typography>
                      <Chip label={expense.category || 'Other'} size="small" color="primary" />
                    </Box>

                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">Date</Typography>
                      <Typography variant="body1">{expense.date || 'N/A'}</Typography>
                    </Box>

                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">Confidence Score</Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <LinearProgress
                          variant="determinate"
                          value={expense.classification_confidence * 100}
                          sx={{ flexGrow: 1 }}
                          color={expense.classification_confidence >= 0.9 ? 'success' : 'warning'}
                        />
                        <Typography variant="body2">
                          {(expense.classification_confidence * 100).toFixed(0)}%
                        </Typography>
                      </Box>
                    </Box>

                    {expense.fraud_analysis && (
                      <Alert 
                        severity={expense.fraud_analysis.risk_score > 70 ? 'error' : 'info'}
                        sx={{ mt: 2 }}
                      >
                        <Typography variant="body2">
                          Fraud Risk: {expense.fraud_analysis.risk_score.toFixed(0)}/100
                        </Typography>
                      </Alert>
                    )}

                    <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                      <Button size="small" variant="outlined" startIcon={<Visibility />}>
                        View Receipt
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </>
      )}
    </Box>
  )
}

export default ExpenseUpload
