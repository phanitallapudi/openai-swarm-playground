import React, { useState, useEffect, useRef } from 'react';
import {
  ConfigProvider,
  theme,
  Input,
  Button,
  Card,
  List,
  message,
  Avatar,
  Spin
} from 'antd';
import {
  CopyOutlined,
  UserOutlined,
  RobotOutlined,
  ReloadOutlined,
  SendOutlined
} from '@ant-design/icons';
import { v4 as uuidv4 } from 'uuid';
import { marked } from 'marked';
import DOMPurify from 'dompurify';

const { darkAlgorithm, defaultAlgorithm } = theme;

function App() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentTheme, setCurrentTheme] = useState('light');

  const messageListRef = useRef(null);

  // Restore theme from localStorage
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setCurrentTheme(savedTheme);
  }, []);

  // Persist theme to localStorage
  useEffect(() => {
    localStorage.setItem('theme', currentTheme);
  }, [currentTheme]);

  // Scroll to bottom when messages change
  useEffect(() => {
    if (messageListRef.current) {
      messageListRef.current.scrollTop = messageListRef.current.scrollHeight;
    }
  }, [messages]);

  // Toggle theme
  const toggleTheme = () => {
    setCurrentTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  // Send message to your API
  const sendMessage = async () => {
    if (!inputText.trim()) {
      message.error('Please enter a message');
      return;
    }
    const userMessage = inputText;
    setIsLoading(true);
    setMessages((prev) => [
      ...prev,
      { id: uuidv4(), type: 'user', text: userMessage }
    ]);
    setInputText('');

    try {
      // Example endpoint (replace with your own)
      const endpoint = `http://localhost:8000/api/swarm/interact?query=${encodeURIComponent(
        userMessage
      )}`;
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { accept: 'application/json' },
        body: ''
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      // If your API returns something like { output: "some text" }:
      const chatbotOutput = data.message || data.output || JSON.stringify(data);
      setMessages((prev) => [
        ...prev,
        { id: uuidv4(), type: 'chatbot', text: chatbotOutput }
      ]);
    } catch (error) {
      console.error('Error sending message:', error);
      message.error('Failed to send message');
    } finally {
      setIsLoading(false);
    }
  };

  // Copy text to clipboard
  const copyToClipboard = (text) => {
    navigator.clipboard
      .writeText(text)
      .then(() => message.success('Copied to clipboard'))
      .catch(() => message.error('Failed to copy'));
  };

  // Send on Enter (without Shift)
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Refresh session
  const handleRefreshSession = () => {
    setMessages([]);
    message.success('Session refreshed');
  };

  // Chatbot bubble styling
  const getChatbotMessageStyle = () => ({
    maxWidth: '70%',
    padding: '10px',
    borderRadius: '8px',
    backgroundColor: currentTheme === 'dark' ? '#444' : '#f0f0f0',
    color: currentTheme === 'dark' ? '#fff' : '#000'
  });

  // Convert markdown to sanitized HTML
  const markdownToHtml = (markdown) => {
    const rawHtml = marked.parse(markdown, { breaks: true });
    return DOMPurify.sanitize(rawHtml);
  };

  return (
    <ConfigProvider
      theme={{
        algorithm: currentTheme === 'dark' ? darkAlgorithm : defaultAlgorithm
      }}
    >
      {/* Outer container: full viewport height */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          height: '100vh',
          background: currentTheme === 'dark' ? '#1a1a1a' : '#fff'
        }}
      >
        {/* Header */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '10px 20px'
          }}
        >
          <h1 style={{ color: currentTheme === 'dark' ? '#fff' : '#000' }}>
            Swarm Chatbot
          </h1>
          <div>
            <Button onClick={toggleTheme} style={{ marginRight: '10px' }}>
              {currentTheme === 'light' ? 'Dark Mode' : 'Light Mode'}
            </Button>
            <Button icon={<ReloadOutlined />} onClick={handleRefreshSession}>
              Refresh
            </Button>
          </div>
        </div>

        {/* Main content (chat area + input). Use flex to push input to the bottom */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
          {/* Chat Window Card (takes all remaining vertical space) */}
          <Card
            title="Chat Window"
            style={{
              flex: 1,
              margin: '0 20px',
              display: 'flex',
              flexDirection: 'column'
            }}
            bodyStyle={{ 
              flex: 1, 
              display: 'flex', 
              flexDirection: 'column', 
              overflow: 'hidden', 
              minHeight: 0 
            }}
          >
            {/* Spinner covers only the message list area */}
            <Spin
              spinning={isLoading}
              tip="Loading..."
              size="large"
              style={{ flex: 1, display: 'flex', flexDirection: 'column' }}
            >
              <div
                ref={messageListRef}
                style={{
                  flex: 1,
                  overflowY: 'auto',
                  wordWrap: 'break-word',
                  paddingRight: '5px',
                  minHeight: 0
                }}
              >
                <List
                  dataSource={messages}
                  renderItem={(item) => (
                    <List.Item
                      key={item.id}
                      style={{
                        display: 'flex',
                        justifyContent:
                          item.type === 'user' ? 'flex-end' : 'flex-start'
                      }}
                    >
                      <div
                        style={
                          item.type === 'user'
                            ? {
                                maxWidth: '70%',
                                padding: '10px',
                                borderRadius: '8px',
                                backgroundColor: '#1890ff',
                                color: '#fff'
                              }
                            : getChatbotMessageStyle()
                        }
                      >
                        {/* User or Chatbot message */}
                        {item.type === 'user' ? (
                          <div style={{ display: 'flex', alignItems: 'center' }}>
                            <Avatar
                              size={40}
                              icon={<UserOutlined />}
                              style={{ marginRight: '8px' }}
                            />
                            <span>{item.text}</span>
                          </div>
                        ) : (
                          <div
                            style={{
                              display: 'flex',
                              flexDirection: 'column',
                              alignItems: 'flex-start'
                            }}
                          >
                            <Avatar
                              size={40}
                              icon={<RobotOutlined />}
                              style={{ marginBottom: '8px' }}
                            />
                            <div
                              dangerouslySetInnerHTML={{
                                __html: markdownToHtml(item.text)
                              }}
                            />
                          </div>
                        )}
                        {/* Copy button for chatbot messages */}
                        {item.type === 'chatbot' && (
                          <Button
                            type="link"
                            icon={<CopyOutlined />}
                            onClick={() => copyToClipboard(item.text)}
                            style={{ marginTop: '5px', padding: 0 }}
                          >
                            Copy
                          </Button>
                        )}
                      </div>
                    </List.Item>
                  )}
                />
              </div>
            </Spin>
          </Card>

          {/* Input area pinned to bottom (outside the Card) */}
          <div
            style={{
              display: 'flex',
              padding: '10px 20px',
              background: currentTheme === 'dark' ? '#1a1a1a' : '#fff'
            }}
          >
            <Input.TextArea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Type your message..."
              autoSize={{ minRows: 2, maxRows: 5 }}
              onKeyDown={handleKeyDown}
              style={{
                flex: 1,
                marginRight: '10px',
                background: currentTheme === 'dark' ? '#444' : '#fff',
                color: currentTheme === 'dark' ? '#fff' : '#000'
              }}
            />
            <Button
              type="primary"
              icon={<SendOutlined />}
              onClick={sendMessage}
              loading={isLoading}
              disabled={isLoading}
            />
          </div>
        </div>
      </div>
    </ConfigProvider>
  );
}

export default App;
