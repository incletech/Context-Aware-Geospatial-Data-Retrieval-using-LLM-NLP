import React, { useState } from 'react';
import { Dialog, DialogActions, DialogContent, DialogTitle, Button, TextField } from '@mui/material';

const SettingsDialog = ({ open, onClose, onSave }) => {
  const [userId, setUserId] = useState('');
  const [latitude, setLatitude] = useState('');
  const [longitude, setLongitude] = useState('');
  const [conversationId, setConversationId] = useState('');

  const handleSave = () => {
    onSave({ userId, latitude, longitude, conversationId });
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Settings</DialogTitle>
      <DialogContent>
        <TextField
          autoFocus
          margin="dense"
          label="User ID"
          type="text"
          fullWidth
          variant="outlined"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
        />
        <TextField
          margin="dense"
          label="Latitude"
          type="text"
          fullWidth
          variant="outlined"
          value={latitude}
          onChange={(e) => setLatitude(e.target.value)}
        />
        <TextField
          margin="dense"
          label="Longitude"
          type="text"
          fullWidth
          variant="outlined"
          value={longitude}
          onChange={(e) => setLongitude(e.target.value)}
        />
        <TextField
          margin="dense"
          label="Conversation ID"
          type="text"
          fullWidth
          variant="outlined"
          value={conversationId}
          onChange={(e) => setConversationId(e.target.value)}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="primary">
          Cancel
        </Button>
        <Button onClick={handleSave} color="primary">
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default SettingsDialog;
