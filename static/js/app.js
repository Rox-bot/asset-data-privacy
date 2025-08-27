// Asset Data Privacy Frontend JavaScript

class AssetDataPrivacyApp {
    constructor() {
        this.currentProcessingInfo = null;
        this.initializeEventListeners();
        this.loadFundNames();
        this.checkConfiguration();
    }

    initializeEventListeners() {
        // File upload
        document.getElementById('pdfFile').addEventListener('change', (e) => {
            this.handleFileSelection(e);
        });

        // Upload button
        document.getElementById('uploadBtn').addEventListener('click', () => {
            this.uploadAndProcess();
        });

        // Fund management
        document.getElementById('addFundBtn').addEventListener('click', () => {
            this.addFundName();
        });

        // OpenAI processing
        document.getElementById('openaiBtn').addEventListener('click', () => {
            this.processWithOpenAI();
        });

        // Decrypt button
        document.getElementById('decryptBtn').addEventListener('click', () => {
            this.decryptResults();
        });

        // Copy buttons
        document.getElementById('copyMaskedBtn').addEventListener('click', () => {
            this.copyToClipboard('maskedContent', 'copyMaskedBtn');
        });

        document.getElementById('copyOriginalBtn').addEventListener('click', () => {
            this.copyToClipboard('originalContent', 'copyOriginalBtn');
        });

        document.getElementById('copyDecryptedBtn').addEventListener('click', () => {
            this.copyToClipboard('decryptedContent', 'copyDecryptedBtn');
        });

        // Download button
        document.getElementById('downloadInfoBtn').addEventListener('click', () => {
            this.downloadProcessingInfo();
        });
    }

    handleFileSelection(event) {
        const file = event.target.files[0];
        const uploadBtn = document.getElementById('uploadBtn');
        
        if (file) {
            uploadBtn.disabled = false;
            uploadBtn.innerHTML = `<i class="fas fa-cloud-upload-alt me-2"></i>Process ${file.name}`;
        } else {
            uploadBtn.disabled = true;
            uploadBtn.innerHTML = `<i class="fas fa-cloud-upload-alt me-2"></i>Process Document`;
        }
    }

    async uploadAndProcess() {
        const fileInput = document.getElementById('pdfFile');
        const file = fileInput.files[0];
        
        if (!file) {
            this.showAlert('Please select a PDF file first.', 'danger');
            return;
        }

        // Show loading state
        const uploadBtn = document.getElementById('uploadBtn');
        const originalText = uploadBtn.innerHTML;
        uploadBtn.disabled = true;
        uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';

        try {
            const formData = new FormData();
            formData.append('file', file);

            console.log('Uploading file:', file.name);
            console.log('File size:', file.size, 'bytes');
            console.log('File type:', file.type);
            
            // Log FormData contents
            for (let [key, value] of formData.entries()) {
                console.log('FormData entry:', key, value);
            }
            
            // Check if server is reachable
            try {
                const serverCheck = await fetch('/');
                console.log('Server check response:', serverCheck.status);
                if (!serverCheck.ok) {
                    throw new Error('Server not responding');
                }
            } catch (serverError) {
                console.error('Server check failed:', serverError);
                throw new Error('Cannot connect to server. Please check if the server is running.');
            }
            
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            console.log('Response status:', response.status);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('Server error response:', errorText);
                throw new Error(`Server error: ${response.status} - ${errorText}`);
            }
            
            const result = await response.json();
            console.log('Response data:', result);

            this.displayResults(result);
            this.showAlert('Document processed successfully!', 'success');

        } catch (error) {
            console.error('Upload error:', error);
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                this.showAlert('Network error: Unable to connect to server. Please check if the server is running.', 'danger');
            } else {
                this.showAlert(`Error: ${error.message}`, 'danger');
            }
        } finally {
            // Restore button state
            uploadBtn.disabled = false;
            uploadBtn.innerHTML = originalText;
        }
    }

    displayResults(processingInfo) {
        this.currentProcessingInfo = processingInfo;

        // Update statistics
        document.getElementById('totalMasked').textContent = processingInfo.total_masked_values;
        document.getElementById('totalFunds').textContent = processingInfo.total_obfuscated_funds;
        document.getElementById('totalChars').textContent = processingInfo.total_characters.toLocaleString();
        document.getElementById('totalPages').textContent = processingInfo.pdf_metadata.total_pages;

        // Display content
        document.getElementById('maskedContent').textContent = processingInfo.masked_text;
        document.getElementById('originalContent').textContent = processingInfo.original_text;

        // Populate tables
        this.populateMaskedValuesTable(processingInfo.masking_info);
        this.populateObfuscatedFundsTable(processingInfo.obfuscation_info);

        // Show results
        document.getElementById('resultsCard').style.display = 'block';
        document.getElementById('decryptButtonContainer').style.display = 'block';
        document.getElementById('openaiBtn').disabled = false;

        // Add fade-in animation
        document.getElementById('resultsCard').classList.add('fade-in');
    }

    populateMaskedValuesTable(maskingInfo) {
        const tbody = document.getElementById('maskedValuesTable');
        tbody.innerHTML = '';

        Object.entries(maskingInfo.masked_values).forEach(([id, info]) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><code>${id}</code></td>
                <td><strong>${info.original}</strong></td>
                <td><code class="text-primary">${info.masked}</code></td>
                <td><small>${info.position[0]}-${info.position[1]}</small></td>
            `;
            tbody.appendChild(row);
        });
    }

    populateObfuscatedFundsTable(obfuscationInfo) {
        const tbody = document.getElementById('obfuscatedFundsTable');
        tbody.innerHTML = '';

        Object.entries(obfuscationInfo.obfuscated_funds).forEach(([id, info]) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><code>${id}</code></td>
                <td><strong>${info.original}</strong></td>
                <td><code class="text-info">${info.placeholder}</code></td>
                <td><small>${info.position[0]}-${info.position[1]}</small></td>
            `;
            tbody.appendChild(row);
        });
    }

    async processWithOpenAI() {
        if (!this.currentProcessingInfo) {
            this.showAlert('Please process a document first.', 'warning');
            return;
        }

        const prompt = document.getElementById('openaiPrompt').value || 'Extract all investment portfolio data and present it in a structured table format with asset names in the first column and all available details in subsequent columns.';
        const openaiBtn = document.getElementById('openaiBtn');
        
        try {
            openaiBtn.disabled = true;
            openaiBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';

            const response = await fetch('/openai_process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    masked_text: this.currentProcessingInfo.masked_text,
                    prompt: prompt
                })
            });

            const result = await response.json();

            if (response.ok) {
                // Store AI response for later decryption
                this.currentProcessingInfo.ai_response = result.ai_response;
                this.displayOpenAIResults(result.ai_response);
                this.showAlert('AI analysis completed successfully!', 'success');
            } else {
                throw new Error(result.error || 'AI processing failed');
            }

        } catch (error) {
            this.showAlert(`AI Processing Error: ${error.message}`, 'danger');
        } finally {
            openaiBtn.disabled = false;
            openaiBtn.innerHTML = '<i class="fas fa-brain me-2"></i>Analyze with AI';
        }
    }

    displayOpenAIResults(aiResponse) {
        const container = document.getElementById('openaiContent');
        container.innerHTML = `
            <div class="openai-content">
                <h6><i class="fas fa-robot me-2"></i>AI Analysis</h6>
                <div class="ai-response">
                    ${aiResponse.replace(/\n/g, '<br>')}
                </div>
                <div class="mt-3">
                    <button class="btn btn-info btn-sm" id="decryptAIResultsBtn">
                        <i class="fas fa-unlock me-2"></i>Decrypt AI Results
                    </button>
                </div>
            </div>
        `;
        
        // Add event listener for decrypt AI results button
        document.getElementById('decryptAIResultsBtn').addEventListener('click', () => {
            this.decryptAIResults(aiResponse);
        });
        
        document.getElementById('openaiResultsCard').style.display = 'block';
        document.getElementById('openaiResultsCard').classList.add('fade-in');
    }

    async decryptAIResults(aiResponse) {
        if (!this.currentProcessingInfo) {
            this.showAlert('No processing info available for decryption.', 'warning');
            return;
        }

        try {
            const response = await fetch('/decrypt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    masked_text: aiResponse,
                    processing_info: this.currentProcessingInfo
                })
            });

            const result = await response.json();

            if (response.ok) {
                this.displayDecryptedAIResults(result.decrypted_text);
                this.showAlert('AI Results decrypted successfully!', 'success');
            } else {
                throw new Error(result.error || 'Decryption failed');
            }

        } catch (error) {
            this.showAlert(`Decryption Error: ${error.message}`, 'danger');
        }
    }

    displayDecryptedAIResults(decryptedText) {
        const container = document.getElementById('openaiContent');
        container.innerHTML = `
            <div class="openai-content">
                <h6><i class="fas fa-robot me-2"></i>AI Analysis (Decrypted)</h6>
                <div class="ai-response">
                    ${decryptedText.replace(/\n/g, '<br>')}
                </div>
                <div class="mt-3">
                    <button class="btn btn-secondary btn-sm" id="showMaskedAIResultsBtn">
                        <i class="fas fa-eye-slash me-2"></i>Show Masked Results
                    </button>
                </div>
            </div>
        `;
        
        // Add event listener to toggle back to masked results
        document.getElementById('showMaskedAIResultsBtn').addEventListener('click', () => {
            this.displayOpenAIResults(this.currentProcessingInfo.ai_response || '');
        });
    }

    async decryptResults() {
        if (!this.currentProcessingInfo) {
            this.showAlert('No results to decrypt.', 'warning');
            return;
        }

        try {
            const response = await fetch('/decrypt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    masked_text: this.currentProcessingInfo.masked_text,
                    processing_info: this.currentProcessingInfo
                })
            });

            const result = await response.json();

            if (response.ok) {
                this.displayDecryptionResults(result.decrypted_text);
                this.showAlert('Document decrypted successfully!', 'success');
            } else {
                throw new Error(result.error || 'Decryption failed');
            }

        } catch (error) {
            this.showAlert(`Decryption Error: ${error.message}`, 'danger');
        }
    }

    displayDecryptionResults(decryptedText) {
        document.getElementById('decryptedContent').textContent = decryptedText;
        document.getElementById('decryptionCard').style.display = 'block';
        document.getElementById('decryptionCard').classList.add('fade-in');
    }

    async checkConfiguration() {
        try {
            const response = await fetch('/api/config');
            const config = await response.json();
            
            if (response.ok) {
                this.updateConfigurationUI(config);
            }
        } catch (error) {
            console.error('Failed to check configuration:', error);
        }
    }

    updateConfigurationUI(config) {
        const openaiBtn = document.getElementById('openaiBtn');
        const openaiStatus = document.getElementById('openaiStatus');
        
        if (config.openai_configured) {
            openaiBtn.disabled = false;
            if (openaiStatus) {
                openaiStatus.innerHTML = '<i class="fas fa-check-circle text-success me-2"></i>OpenAI API Configured';
                openaiStatus.className = 'text-success';
            }
        } else {
            openaiBtn.disabled = true;
            if (openaiStatus) {
                openaiStatus.innerHTML = '<i class="fas fa-exclamation-triangle text-warning me-2"></i>OpenAI API Key Required';
                openaiStatus.className = 'text-warning';
            }
        }
    }

    async loadFundNames() {
        try {
            const response = await fetch('/api/fund_names');
            const data = await response.json();
            
            if (response.ok) {
                this.displayFundNames(data.fund_names, data.placeholder_mapping);
            }
        } catch (error) {
            console.error('Error loading fund names:', error);
        }
    }

    displayFundNames(fundNames, placeholderMapping) {
        const container = document.getElementById('fundNamesList');
        container.innerHTML = '';

        fundNames.forEach(fundName => {
            const placeholder = placeholderMapping[fundName];
            const item = document.createElement('div');
            item.className = 'fund-name-item';
            item.innerHTML = `
                <div>
                    <span class="fund-name">${fundName}</span>
                    <span class="placeholder ms-2">${placeholder}</span>
                </div>
                <button class="remove-btn" onclick="app.removeFundName('${fundName}')">
                    <i class="fas fa-times"></i>
                </button>
            `;
            container.appendChild(item);
        });
    }

    async addFundName() {
        const input = document.getElementById('newFundName');
        const fundName = input.value.trim();
        
        if (!fundName) {
            this.showAlert('Please enter a fund name.', 'warning');
            return;
        }

        try {
            const response = await fetch('/api/fund_names', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ fund_name: fundName })
            });

            const result = await response.json();

            if (response.ok) {
                this.showAlert(result.message, 'success');
                input.value = '';
                this.loadFundNames();
            } else {
                throw new Error(result.error || 'Failed to add fund name');
            }

        } catch (error) {
            this.showAlert(`Error: ${error.message}`, 'danger');
        }
    }

    async removeFundName(fundName) {
        try {
            const response = await fetch('/api/fund_names', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ fund_name: fundName })
            });

            const result = await response.json();

            if (response.ok) {
                this.showAlert(result.message, 'success');
                this.loadFundNames();
            } else {
                throw new Error(result.error || 'Failed to remove fund name');
            }

        } catch (error) {
            this.showAlert(`Error: ${error.message}`, 'danger');
        }
    }

    async copyToClipboard(elementId, buttonId) {
        const element = document.getElementById(elementId);
        const text = element.textContent;
        
        try {
            await navigator.clipboard.writeText(text);
            
            const button = document.getElementById(buttonId);
            const originalText = button.innerHTML;
            
            button.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
            button.classList.add('copied');
            
            setTimeout(() => {
                button.innerHTML = originalText;
                button.classList.remove('copied');
            }, 2000);
            
            this.showAlert('Text copied to clipboard!', 'success');
        } catch (error) {
            this.showAlert('Failed to copy text to clipboard.', 'danger');
        }
    }

    downloadProcessingInfo() {
        if (!this.currentProcessingInfo) {
            this.showAlert('No processing information available.', 'warning');
            return;
        }

        const filename = this.currentProcessingInfo.processing_info_file;
        const downloadUrl = `/download/${filename}`;
        
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        this.showAlert('Processing information downloaded!', 'success');
    }

    showAlert(message, type) {
        // Remove existing alerts
        const existingAlerts = document.querySelectorAll('.alert');
        existingAlerts.forEach(alert => alert.remove());

        // Create new alert
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(alertDiv);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.app = new AssetDataPrivacyApp();
});
