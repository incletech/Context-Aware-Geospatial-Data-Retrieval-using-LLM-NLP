import React from 'react';

const IframeWidget = ({ url }) => (
  <iframe
    src={url}
    title="Map"
    width="100%"
    height="450"
    style={{ border: 0 }}
    allowFullScreen=""
    loading="lazy"
  ></iframe>
);

export default IframeWidget;
