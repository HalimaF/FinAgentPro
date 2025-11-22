import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  IconButton,
  TextField,
  List,
  ListItem,
  ListItemText,
  Chip,
  Alert,
  CircularProgress
} from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';
import StopIcon from '@mui/icons-material/Stop';
import SendIcon from '@mui/icons-material/Send';
import SmartToyIcon from '@mui/icons-material/SmartToy';

interface VoiceCommand {
  id: string;
  transcript: string;
  parsed_intent: string;
  action_type: string;
  confidence: number;
  timestamp: string;
}

export default function VoiceAssistant() {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [commands, setCommands] = useState<VoiceCommand[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [recognition, setRecognition] = useState<any>(null);

  // Initialize Web Speech API
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
      const recognitionInstance = new SpeechRecognition();
      
      recognitionInstance.continuous = false;
      recognitionInstance.interimResults = false;
      recognitionInstance.lang = 'en-US';
      
      recognitionInstance.onresult = (event: any) => {
        const speechResult = event.results[0][0].transcript;
        setTranscript(speechResult);
        processVoiceCommand(speechResult);
      };
      
      recognitionInstance.onerror = (event: any) => {
        setError(`Speech recognition error: ${event.error}`);
        setIsListening(false);
      };
      
      recognitionInstance.onend = () => {
        setIsListening(false);
      };
      
      setRecognition(recognitionInstance);
    } else {
      setError('Speech recognition not supported in this browser');
    }
  }, []);

  const startListening = () => {
    if (recognition) {
      setError(null);
      setTranscript('');
      recognition.start();
      setIsListening(true);
    }
  };

  const stopListening = () => {
    if (recognition) {
      recognition.stop();
      setIsListening(false);
    }
  };

  const processVoiceCommand = async (voiceText: string) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/v1/ai/voice/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          transcript: voiceText,
          user_id: 'demo_user'
        })
      });

      if (!response.ok) throw new Error('Voice processing failed');

      const result = await response.json();
      
      const newCommand: VoiceCommand = {
        id: Date.now().toString(),
        transcript: voiceText,
        parsed_intent: result.parsed_intent || 'Processing...',
        action_type: result.action_type || 'unknown',
        confidence: result.confidence || 0,
        timestamp: new Date().toLocaleTimeString()
      };
      
      setCommands([newCommand, ...commands]);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleTextSubmit = () => {
    if (transcript.trim()) {
      processVoiceCommand(transcript);
    }
  };

  const getActionColor = (actionType: string) => {
    switch (actionType) {
      case 'create_expense': return 'success';
      case 'query': return 'info';
      case 'create_invoice': return 'warning';
      default: return 'default';
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        <SmartToyIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
        AI Voice Assistant
      </Typography>

      <Card sx={{ mb: 3, bgcolor: 'primary.main', color: 'white' }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Voice-Powered Financial Management
          </Typography>
          <Typography variant="body2">
            Try saying:
          </Typography>
          <List dense>
            <ListItem>• "Add lunch receipt for $45 at Chipotle"</ListItem>
            <ListItem>• "Show me all travel expenses this month"</ListItem>
            <ListItem>• "Create invoice for Project X"</ListItem>
            <ListItem>• "What's my biggest spending category?"</ListItem>
          </List>
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <IconButton
              color={isListening ? 'error' : 'primary'}
              size="large"
              onClick={isListening ? stopListening : startListening}
              disabled={loading || !recognition}
              sx={{
                bgcolor: isListening ? 'error.light' : 'primary.light',
                '&:hover': {
                  bgcolor: isListening ? 'error.main' : 'primary.main'
                }
              }}
            >
              {isListening ? <StopIcon /> : <MicIcon />}
            </IconButton>

            <TextField
              fullWidth
              placeholder="Or type your command here..."
              value={transcript}
              onChange={(e) => setTranscript(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleTextSubmit()}
              disabled={loading}
            />

            <IconButton
              color="primary"
              onClick={handleTextSubmit}
              disabled={!transcript.trim() || loading}
            >
              {loading ? <CircularProgress size={24} /> : <SendIcon />}
            </IconButton>
          </Box>

          {isListening && (
            <Box sx={{ mt: 2, textAlign: 'center' }}>
              <Typography variant="body2" color="error">
                🎤 Listening...
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>

      <Typography variant="h6" gutterBottom>
        Command History
      </Typography>

      <List>
        {commands.length === 0 && (
          <ListItem>
            <ListItemText
              primary="No commands yet"
              secondary="Start speaking or typing to interact with the AI assistant"
            />
          </ListItem>
        )}
        
        {commands.map((cmd) => (
          <Card key={cmd.id} sx={{ mb: 2 }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Chip
                  label={cmd.action_type.replace('_', ' ').toUpperCase()}
                  color={getActionColor(cmd.action_type) as any}
                  size="small"
                />
                <Typography variant="caption" color="text.secondary">
                  {cmd.timestamp}
                </Typography>
              </Box>
              
              <Typography variant="body1" gutterBottom>
                <strong>You said:</strong> "{cmd.transcript}"
              </Typography>
              
              <Typography variant="body2" color="text.secondary">
                <strong>AI understood:</strong> {cmd.parsed_intent}
              </Typography>
              
              <Box sx={{ mt: 1 }}>
                <Chip
                  label={`${Math.round(cmd.confidence * 100)}% confidence`}
                  size="small"
                  variant="outlined"
                />
              </Box>
            </CardContent>
          </Card>
        ))}
      </List>
    </Box>
  );
}
