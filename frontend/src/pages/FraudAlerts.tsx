import React from 'react'
import { Box, Card, CardContent, Typography, Chip, Stack, Button, Grid } from '@mui/material'

type Alert = {
  id: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  riskScore: number
  title: string
  explanation: string
  recommended: string[]
  time: string
}

const sampleAlerts: Alert[] = [
  {
    id: 'fa-001',
    severity: 'high',
    riskScore: 85,
    title: 'Suspicious merchant + unusual amount',
    explanation: 'Amount 20x above average at previously unseen merchant at 02:35 AM.',
    recommended: ['Block transaction', 'Require 2FA', 'Notify security'],
    time: 'Just now'
  },
  {
    id: 'fa-002',
    severity: 'medium',
    riskScore: 62,
    title: 'Geolocation mismatch',
    explanation: 'Transaction originated from an unusual location pattern.',
    recommended: ['Request user confirmation'],
    time: '12 min ago'
  }
]

const severityColor = (s: Alert['severity']) => {
  switch (s) {
    case 'low': return 'success'
    case 'medium': return 'warning'
    case 'high': return 'error'
    case 'critical': return 'error'
    default: return 'default'
  }
}

export default function FraudAlerts() {
  return (
    <Box p={3}>
      <Typography variant="h5" fontWeight={700} mb={2}>Fraud Alerts</Typography>
      <Typography color="text.secondary" mb={3}>
        Real-time alerts from the Fraud Analyzer. Resolve by approving, rejecting, or escalating.
      </Typography>

      <Grid container spacing={2}>
        {sampleAlerts.map((a) => (
          <Grid item xs={12} md={6} key={a.id}>
            <Card variant="outlined">
              <CardContent>
                <Stack direction="row" justifyContent="space-between" alignItems="center" mb={1}>
                  <Typography variant="subtitle1" fontWeight={700}>{a.title}</Typography>
                  <Chip size="small" color={severityColor(a.severity)} label={`${a.severity.toUpperCase()} • ${a.riskScore}`} />
                </Stack>
                <Typography color="text.secondary" mb={1}>{a.explanation}</Typography>
                <Stack direction="row" spacing={1} flexWrap="wrap" mb={2}>
                  {a.recommended.map((r, idx) => (
                    <Chip key={idx} size="small" variant="outlined" label={r} />
                  ))}
                </Stack>
                <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1}>
                  <Button variant="contained" color="error">Block</Button>
                  <Button variant="outlined" color="primary">Require 2FA</Button>
                  <Button variant="text">Mark as Safe</Button>
                </Stack>
                <Typography variant="caption" color="text.disabled" display="block" mt={1}>{a.time}</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  )
}
