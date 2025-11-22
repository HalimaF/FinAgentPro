import React from 'react'
import { Box, Card, CardContent, Typography, Grid, Chip, Stack } from '@mui/material'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts'

const data = Array.from({ length: 12 }).map((_, i) => ({
  month: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][i],
  expected: 100 + i * 15,
  best: 120 + i * 18,
  worst: 80 + i * 12,
}))

export default function CashflowForecast() {
  return (
    <Box p={3}>
      <Typography variant="h5" fontWeight={700} mb={2}>Cashflow Forecast</Typography>
      <Typography color="text.secondary" mb={3}>
        Expected cash position over the next 12 months with scenario bands.
      </Typography>

      <Grid container spacing={2}>
        <Grid item xs={12} md={8}>
          <Card variant="outlined">
            <CardContent>
              <Typography variant="subtitle1" fontWeight={700} mb={2}>12‑Month Projection</Typography>
              <Box height={320}>
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                    <defs>
                      <linearGradient id="colorBest" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#4caf50" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#4caf50" stopOpacity={0}/>
                      </linearGradient>
                      <linearGradient id="colorWorst" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#f44336" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#f44336" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Area type="monotone" dataKey="best" stroke="#4caf50" fill="url(#colorBest)" name="Best" />
                    <Area type="monotone" dataKey="worst" stroke="#f44336" fill="url(#colorWorst)" name="Worst" />
                    <Line type="monotone" dataKey="expected" stroke="#1976d2" strokeWidth={2} name="Expected" />
                  </AreaChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card variant="outlined">
            <CardContent>
              <Typography variant="subtitle1" fontWeight={700} mb={2}>Metrics</Typography>
              <Stack spacing={1}>
                <Typography>Runway: <b>15.3 months</b></Typography>
                <Typography>Average Burn: <b>$25,000 / mo</b></Typography>
                <Typography>12‑Month Net: <b>+$125,400</b></Typography>
                <Typography>Confidence: <Chip size="small" color="success" label="95%" /></Typography>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}
