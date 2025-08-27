# Asset Data Privacy - Web Frontend

A beautiful, modern web interface for the Asset Data Privacy system with OpenAI integration and tabular output display.

## 🌟 Features

### 🎨 **Modern UI Design**
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile devices
- **Beautiful Cards**: Clean, modern card-based design with hover effects
- **Professional Color Scheme**: Uses the comprehensive luxury color system
- **Smooth Animations**: Fade-in effects and smooth transitions

### 📊 **Tabular Output Display**
- **Masked Values Table**: Shows all masked numerical values with IDs, originals, and positions
- **Fund Names Table**: Displays obfuscated fund names and their placeholders
- **Statistics Dashboard**: Real-time processing statistics (masked values, funds, characters, pages)
- **Tabbed Interface**: Organized tabs for different views (Masked, Original, Details)

### 🤖 **OpenAI Integration**
- **AI Analysis**: Send masked documents to OpenAI for analysis
- **Custom Prompts**: Configure your own analysis prompts
- **Secure Processing**: Sensitive data never reaches OpenAI
- **Structured Results**: AI analysis displayed in organized format

### 🔧 **Interactive Features**
- **File Upload**: Drag-and-drop PDF upload with progress indication
- **Fund Management**: Add/remove fund names dynamically
- **Copy to Clipboard**: One-click copying of any content
- **Download Processing Info**: Export processing details as JSON
- **Real-time Updates**: Live updates during processing

## 🚀 Quick Start

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Set OpenAI API Key** (Optional)
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 3. **Start the Frontend**
```bash
python3 start_frontend.py
```

### 4. **Open in Browser**
Navigate to: `http://localhost:5000`

## 📱 **Interface Overview**

### **Left Panel - Controls**
- **Document Upload**: PDF file selection and processing
- **Fund Names Management**: Add/remove fund names for obfuscation
- **OpenAI Configuration**: Set analysis prompts and enable AI processing

### **Right Panel - Results**
- **Processing Results**: Main results with tabbed interface
- **AI Analysis**: OpenAI processing results
- **Decryption Results**: Original data recovery

### **Tabbed Views**
1. **Masked Document**: AI-ready masked content
2. **Original Document**: Source document content
3. **Processing Details**: Detailed tables and information

## 🎯 **Usage Workflow**

### **Step 1: Upload Document**
1. Click "Choose File" and select a PDF
2. Click "Process Document"
3. Wait for processing to complete

### **Step 2: Review Results**
1. View masked document in the first tab
2. Check processing details in the third tab
3. Review statistics and tables

### **Step 3: AI Analysis** (Optional)
1. Set your analysis prompt
2. Click "Analyze with AI"
3. Review AI-generated insights

### **Step 4: Decrypt Results**
1. Click the "Decrypt Results" button
2. View original sensitive data
3. Download processing information if needed

## 🔐 **Security Features**

### **Data Privacy**
- **Local Processing**: All sensitive data stays on your system
- **No Network Transmission**: Zero risk of data interception
- **Secure Masking**: Complete data obfuscation before any external processing

### **OpenAI Safety**
- **Masked Data Only**: Only obfuscated content sent to OpenAI
- **No Sensitive Information**: Original values never exposed
- **Audit Trail**: Complete logging of all operations

## 📊 **Table Structure**

### **Masked Values Table**
| Column | Description |
|--------|-------------|
| ID | Unique identifier for each masked value |
| Original Value | The original numerical value |
| Masked Value | The obfuscated identifier |
| Position | Character position in the document |

### **Obfuscated Funds Table**
| Column | Description |
|--------|-------------|
| ID | Unique identifier for each fund |
| Original Name | The actual fund name |
| Placeholder | The generic placeholder (Fund001, etc.) |
| Position | Character position in the document |

## 🛠️ **Configuration**

### **Environment Variables**
```bash
# Required for OpenAI integration
export OPENAI_API_KEY="your-api-key-here"

# Optional: Custom secret key
export SECRET_KEY="your-secret-key"
```

### **Fund Names Management**
- **Add Funds**: Type fund name and click "+"
- **Remove Funds**: Click the "×" button next to any fund
- **Automatic Mapping**: Placeholders generated automatically

### **OpenAI Settings**
- **Model**: Uses GPT-4 by default
- **Temperature**: Set to 0.3 for consistent analysis
- **Max Tokens**: Limited to 2000 for cost control
- **Custom Prompts**: Fully configurable analysis instructions

## 📁 **File Structure**

```
Asset-Data-Privacy/
├── app.py                      # Flask web application
├── start_frontend.py           # Frontend startup script
├── templates/
│   └── index.html             # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css          # Custom CSS styles
│   └── js/
│       └── app.js             # Frontend JavaScript
├── uploads/                    # Temporary file storage
├── output/                     # Processing results
└── sample_financial_report.pdf # Test PDF document
```

## 🔧 **Customization**

### **Styling**
- **Colors**: Modify CSS variables in `static/css/style.css`
- **Layout**: Adjust Bootstrap classes in `templates/index.html`
- **Animations**: Customize CSS animations and transitions

### **Functionality**
- **New Features**: Extend `static/js/app.js` with additional functionality
- **API Endpoints**: Add new routes in `app.py`
- **Processing Logic**: Modify the core privacy system components

## 🧪 **Testing**

### **Sample Document**
- **File**: `sample_financial_report.pdf`
- **Content**: Financial report with fund names and numerical data
- **Purpose**: Test all frontend functionality

### **Test Scenarios**
1. **Basic Processing**: Upload and process the sample PDF
2. **Fund Management**: Add/remove fund names
3. **AI Integration**: Test OpenAI analysis (requires API key)
4. **Decryption**: Verify data recovery
5. **Export**: Download processing information

## 🚨 **Troubleshooting**

### **Common Issues**

#### **Server Won't Start**
```bash
# Check dependencies
pip install -r requirements.txt

# Check Python version
python3 --version  # Should be 3.8+
```

#### **OpenAI Integration Not Working**
```bash
# Set API key
export OPENAI_API_KEY="your-key-here"

# Restart the server
python3 start_frontend.py
```

#### **File Upload Errors**
- **File Size**: Maximum 16MB
- **File Type**: PDF only
- **Permissions**: Check upload directory permissions

#### **Processing Errors**
- **PDF Format**: Ensure PDF is not corrupted or password-protected
- **Memory**: Large documents may require more RAM
- **Dependencies**: Verify PyMuPDF and PyPDF2 installation

### **Debug Mode**
```bash
# Enable Flask debug mode
export FLASK_ENV=development
python3 app.py
```

## 📈 **Performance**

### **Optimizations**
- **File Size Limits**: 16MB maximum for uploads
- **Memory Management**: Efficient text processing
- **Caching**: Processing results cached in memory
- **Async Operations**: Non-blocking file operations

### **Scalability**
- **Single Server**: Designed for single-user or small team use
- **Resource Usage**: Minimal memory and CPU footprint
- **File Handling**: Efficient PDF processing pipeline

## 🔮 **Future Enhancements**

### **Planned Features**
- **User Authentication**: Secure login system
- **Batch Processing**: Multiple file uploads
- **Advanced Analytics**: Enhanced AI analysis options
- **Export Formats**: Additional output formats (Excel, Word)
- **API Integration**: RESTful API for external systems

### **Extensibility**
- **Plugin System**: Modular architecture for custom features
- **Custom Masking Rules**: User-defined obfuscation patterns
- **Integration Hooks**: Webhooks and API endpoints

## 📞 **Support**

### **Getting Help**
1. **Check Documentation**: Review this README and main README
2. **Test with Sample**: Use the provided sample PDF
3. **Check Logs**: Review console output for error messages
4. **Verify Setup**: Ensure all dependencies are installed

### **Reporting Issues**
- **Error Messages**: Include complete error text
- **Steps to Reproduce**: Detailed reproduction steps
- **Environment**: OS, Python version, browser details
- **Sample Data**: Test case that demonstrates the issue

---

**🎉 The Asset Data Privacy Web Frontend provides a professional, user-friendly interface for secure financial document processing with AI integration!**
