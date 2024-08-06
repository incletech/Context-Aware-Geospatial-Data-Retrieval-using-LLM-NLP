import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { ThemeProvider } from '@mui/material/styles';
import IframeWidget from './IframeWidget';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import { TextField, IconButton, Typography, Button, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import MicIcon from '@mui/icons-material/Mic';
import MicOffIcon from '@mui/icons-material/MicOff';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import PersonIcon from '@mui/icons-material/Person';
import RobotIcon from '@mui/icons-material/Android';
import darkTheme from './theme';
import './App.css';

const generateConversationId = () => 'conv_' + Math.random().toString(36).substr(2, 9);

const ChatApp = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [settings, setSettings] = useState({
    userName: '',
    latitude: '',
    longitude: '',
    conversationId: generateConversationId(),
  });
  const [voices, setVoices] = useState([]);
  const [loading, setLoading] = useState(false);
  const { transcript, listening, resetTranscript, browserSupportsSpeechRecognition } = useSpeechRecognition();
  const messagesEndRef = useRef(null);

  const API_URL = 'https://incletech-incle-ai71.hf.space/agent';
  const API_KEY = process.env.REACT_APP_AI71_API_KEY;
  const BROWSER_KEY = process.env.REACT_APP_GOOGLE_MAPS_API_KEY;
  const ELEVENLABS_API_KEY = process.env.REACT_APP_ELEVENLABS_API_KEY;
  const ELEVENLABS_VOICE_ID = process.env.REACT_APP_ELEVENLABS_VOICE_ID;

  useEffect(() => {
    const handleVoicesChanged = () => {
      setVoices(window.speechSynthesis.getVoices());
    };

    window.speechSynthesis.onvoiceschanged = handleVoicesChanged;
    handleVoicesChanged(); // Initial call to populate voices
  }, []);

  useEffect(() => {
    if (transcript) {
      handleSend(transcript);
      resetTranscript();
    }
  }, [transcript, resetTranscript]);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);
  if (!browserSupportsSpeechRecognition) {
    return <span>Your browser doesn't support speech recognition.</span>;
  }

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const generateGoogleMapsEmbedUrl = (address) => {
    const encodedAddress = encodeURIComponent(address);
    return `https://www.google.com/maps/embed/v1/place?key=${BROWSER_KEY}&q=${encodedAddress}`;
  };

  const handleSend = async (messageText) => {
    if (messageText.trim()) {
      const userMessage = { text: messageText, type: 'user', userName: settings.userName };
      setMessages((prevMessages) => [...prevMessages, userMessage]);
      setInputValue('');
      setLoading(true);

      try {
        const response = await axios.post(
          API_URL,
          {
            prompt: messageText,
            conversation_id: settings.conversationId,
            user_name: settings.userName,
            latitude: parseFloat(settings.latitude),
            longitude: parseFloat(settings.longitude),
          },
          {
            headers: {
              accept: 'application/json',
              'Content-Type': 'application/json',
              Authorization: `Bearer ${API_KEY}`,
            },
          }
        );

        if (response.status === 200) {
          const { completion, conversation_id, intent, map_url, reference_url } = response.data;
          const botMessage = { text: '', type: 'bot', userName: 'Aadheera', mapUrl: map_url, referenceUrl: reference_url };
          setSettings((prevSettings) => ({ ...prevSettings, conversationId: conversation_id }));

          // Stream the bot's response
          await streamBotResponse(completion, botMessage);
        } else {
          console.error('Error:', response.status, response.data);
        }
      } catch (error) {
        console.error('Error:', error);
      } finally {
        setLoading(false);
      }
    }
  };

  const streamBotResponse = async (text, botMessage) => {
    const words = text.split(' ');
    for (const word of words) {
      botMessage.text += word + ' ';
      setMessages((prevMessages) => {
        const lastMessage = prevMessages[prevMessages.length - 1];
        if (lastMessage && lastMessage.type === 'bot') {
          return [...prevMessages.slice(0, -1), botMessage];
        } else {
          return [...prevMessages, botMessage];
        }
      });
      await new Promise((resolve) => setTimeout(resolve, 50));
    }
  };

  const textToSpeech = async (text) => {
    const url = `https://api.elevenlabs.io/v1/text-to-speech/${ELEVENLABS_VOICE_ID}`;
    const headers = {
      Accept: 'audio/mpeg',
      'Content-Type': 'application/json',
      'xi-api-key': ELEVENLABS_API_KEY,
    };

    const data = {
      text: text,
      model_id: 'eleven_monolingual_v1',
      voice_settings: {
        stability: 0.5,
        similarity_boost: 0.5,
      },
    };

    try {
      const response = await axios.post(url, data, { headers, responseType: 'arraybuffer' });

      if (response.status === 200) {
        const audioBlob = new Blob([response.data], { type: 'audio/mpeg' });
        const audioUrl = URL.createObjectURL(audioBlob);

        const audio = new Audio(audioUrl);
        audio.play();
      } else {
        console.error('Error:', response.status, response.data);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleReset = () => {
    setMessages([]);
    setSettings({
      userName: '',
      latitude: '',
      longitude: '',
      conversationId: generateConversationId(),
    });
  };

  const handleSaveSettings = () => {
    // Logic to save settings if needed
  };

  return (
    <ThemeProvider theme={darkTheme}>
      <div className="rightSection">
        <div className="sidebar">
          <Typography variant="h6">Settings</Typography>
          <TextField
            autoFocus
            margin="dense"
            label="User Name"
            type="text"
            fullWidth
            variant="outlined"
            value={settings.userName}
            onChange={(e) => setSettings({ ...settings, userName: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Latitude"
            type="text"
            fullWidth
            variant="outlined"
            value={settings.latitude}
            onChange={(e) => setSettings({ ...settings, latitude: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Longitude"
            type="text"
            fullWidth
            variant="outlined"
            value={settings.longitude}
            onChange={(e) => setSettings({ ...settings, longitude: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Conversation ID"
            type="text"
            fullWidth
            variant="outlined"
            value={settings.conversationId}
            onChange={(e) => setSettings({ ...settings, conversationId: e.target.value })}
          />
          <div className="button-container">
            <Button className="save-button" onClick={handleSaveSettings}>
              Save
            </Button>
            <Button className="reset-button" onClick={handleReset}>
              Reset
            </Button>
          </div>
        </div>
        <div className="chatArea">
          <div className="schoolbg"></div>
          <div className="rightin">
            <div className="messages">
              {messages.length === 0 ? (
                <div className="nochat">
                  <div className="s1">
                    <h1>Welcome to Aadheera Chat</h1>
                  </div>
                  <div className="s2">
                    <div className="suggestioncard">
                      <h2>Type 'hi' to see a map</h2>
                      <p>Interact with the chat to see more responses.</p>
                    </div>
                  </div>
                </div>
              ) : (
                messages.map((message, index) => (
                  <div className="message" key={index}>
                    <div className="message-icon">
                      {message.type === 'bot' ? <RobotIcon /> : <PersonIcon />}
                    </div>
                    <div className="message-content">
                      <div className="message-header">
                        <h2 className={message.type === 'bot' ? 'bot-name' : ''}>{message.userName}</h2>
                        <IconButton className="audio-button" onClick={() => textToSpeech(message.text)}>
                          <PlayArrowIcon />
                        </IconButton>
                      </div>
                      <p>{message.text}</p>
                      {message.mapUrl && (
                        <div style={{ marginTop: '10px' }}>
                          <IframeWidget url={message.mapUrl} />
                        </div>
                      )}
                      {message.referenceUrl && (
                        <div style={{ marginTop: '10px' }}>
                          <a href={message.referenceUrl} target="_blank" rel="noopener noreferrer">
                            Reference Link
                          </a>
                        </div>
                      )}
                    </div>
                  </div>
                ))
              )}
              <div ref={messagesEndRef} />
            </div>
            <div className="bottomsection">
              <div className="messagebar">
                <TextField
                  variant="outlined"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSend(inputValue)}
                  placeholder="Type a message..."
                  fullWidth
                />
                <IconButton color="primary" onClick={() => handleSend(inputValue)}>
                  {loading ? <CircularProgress size={24} /> : <SendIcon />}
                </IconButton>
                <IconButton color="primary" onClick={SpeechRecognition.startListening}>
                  {listening ? <MicOffIcon /> : <MicIcon />}
                </IconButton>
              </div>
              {listening && <p>Listening...</p>}
            </div>
          </div>
        </div>
      </div>
    </ThemeProvider>
  );
};

export default ChatApp;
