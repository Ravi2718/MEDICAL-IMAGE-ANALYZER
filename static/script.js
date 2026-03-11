// File upload and analysis logic
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const fileInfo = document.getElementById('fileInfo');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const uploadSection = document.querySelector('.upload-section');

let selectedFile = null;

// Drag and drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
});

// Click to upload
dropZone.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

function handleFiles(files) {
    if (files.length === 0) return;
    
    const file = files[0];
    
    // Validate file type
    const allowedTypes = ['image/png', 'image/jpeg', 'image/gif', 'image/bmp', 'image/tiff'];
    if (!allowedTypes.includes(file.type)) {
        alert('Invalid file type. Please upload: PNG, JPG, JPEG, GIF, BMP, or TIFF');
        return;
    }
    
    // Validate file size (25MB)
    if (file.size > 25 * 1024 * 1024) {
        alert('File too large. Maximum size is 25MB');
        return;
    }
    
    selectedFile = file;
    displayFileInfo(file);
}

function displayFileInfo(file) {
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileSize').textContent = formatFileSize(file.size);
    fileInfo.style.display = 'block';
    analyzeBtn.style.display = 'inline-flex';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Analyze button click
analyzeBtn.addEventListener('click', () => {
    if (!selectedFile) {
        alert('Please select a file');
        return;
    }
    
    analyzeImage(selectedFile);
});

async function analyzeImage(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    // Show loading
    loadingSection.style.display = 'block';
    analyzeBtn.disabled = true;
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Analysis failed');
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        alert('Error: ' + error.message);
        console.error('Analysis error:', error);
    } finally {
        loadingSection.style.display = 'none';
        analyzeBtn.disabled = false;
    }
}

function displayResults(data) {
    // Display uploaded image
    document.getElementById('resultImage').src = data.image;
    document.getElementById('uploadTime').textContent = new Date(data.timestamp).toLocaleString();
    
    const analysis = data.analysis;
    
    // Display analysis type and basic info
    let analysisHTML = `
        <div class="analysis-info">
            <p><strong>Report Type:</strong> ${analysis.type}</p>
            <p><strong>Timestamp:</strong> ${new Date(data.timestamp).toLocaleString()}</p>
    `;
    
    // Add Urgency and Severity
    if (analysis.urgency) {
        const urgencyColor = analysis.urgency === 'IMMEDIATE' ? '#dc2626' : analysis.urgency === 'URGENT' ? '#f59e0b' : '#10b981';
        analysisHTML += `
            <div style="margin-top: 1rem; padding: 1rem; background-color: ${urgencyColor}20; border-left: 4px solid ${urgencyColor}; border-radius: 0.5rem;">
                <p><strong style="color: ${urgencyColor};">Urgency Level:</strong> <span style="color: ${urgencyColor}; font-weight: bold;">${analysis.urgency}</span></p>
                ${analysis.severity ? `<p><strong>Severity:</strong> ${analysis.severity}</p>` : ''}
            </div>
        `;
    }
    
    if (analysis.image_quality) {
        analysisHTML += `
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #e5e7eb;">
                <h4>Image Quality Assessment</h4>
                <p><strong>Blur Score:</strong> ${analysis.image_quality.blur_score}</p>
                <p><strong>Contrast Score:</strong> ${analysis.image_quality.contrast_score}</p>
                <p><strong>Quality Grade:</strong> ${analysis.image_quality.quality_grade || 'N/A'}</p>
                <p><strong>Assessment:</strong> ${analysis.image_quality.assessment}</p>
            </div>
        `;
    }
    
    analysisHTML += `</div>`;
    
    document.getElementById('analysisResults').innerHTML = analysisHTML;
    
    // Display detailed findings with professional report format
    let detailedHTML = `
        <div>
            <div style="background: #fee2e2; border-left: 4px solid #dc2626; padding: 1rem; margin-bottom: 1.5rem; border-radius: 0.5rem;">
                <p style="color: #991b1b; margin: 0;">⚠️ ${analysis.disclaimer}</p>
            </div>
    `;
    
    // FINDINGS SECTION
    if (analysis.findings && Array.isArray(analysis.findings) && analysis.findings.length > 0) {
        detailedHTML += `
            <h4 style="color: #1f2937; margin-top: 1.5rem; margin-bottom: 1rem; border-bottom: 2px solid #2563eb; padding-bottom: 0.5rem;">📋 FINDINGS</h4>
            <ul style="list-style-position: inside;">
        `;
        analysis.findings.forEach(finding => {
            detailedHTML += `<li style="margin: 0.75rem 0; line-height: 1.6;">• ${finding}</li>`;
        });
        detailedHTML += `</ul>`;
    }
    
    // IMPRESSION SECTION
    if (analysis.impression) {
        detailedHTML += `
            <div style="background: #dbeafe; border-left: 4px solid #2563eb; padding: 1rem; margin: 1.5rem 0; border-radius: 0.5rem;">
                <h4 style="color: #1e40af; margin-top: 0;">📝 IMPRESSION</h4>
                <p style="color: #1e3a8a; margin: 0.5rem 0;">${analysis.impression}</p>
            </div>
        `;
    }
    
    // COMPLICATIONS SECTION
    if (analysis.complications && Array.isArray(analysis.complications) && analysis.complications.length > 0) {
        detailedHTML += `
            <h4 style="color: #991b1b; margin-top: 1.5rem;">⚠️ POTENTIAL COMPLICATIONS</h4>
            <ul style="list-style-position: inside; color: #7f1d1d;">
        `;
        analysis.complications.forEach(comp => {
            detailedHTML += `<li style="margin: 0.5rem 0;">• ${comp}</li>`;
        });
        detailedHTML += `</ul>`;
    }
    
    // TREATMENT OPTIONS SECTION
    if (analysis.treatment_options && Array.isArray(analysis.treatment_options) && analysis.treatment_options.length > 0) {
        detailedHTML += `
            <h4 style="color: #059669; margin-top: 1.5rem;">💊 TREATMENT OPTIONS</h4>
            <ul style="list-style-position: inside; color: #065f46;">
        `;
        analysis.treatment_options.forEach(treatment => {
            detailedHTML += `<li style="margin: 0.5rem 0;">• ${treatment}</li>`;
        });
        detailedHTML += `</ul>`;
    }
    
    // NEXT STEPS SECTION
    if (analysis.next_steps && Array.isArray(analysis.next_steps) && analysis.next_steps.length > 0) {
        detailedHTML += `
            <h4 style="color: #2563eb; margin-top: 1.5rem;">→ NEXT STEPS</h4>
            <ol style="list-style-position: inside;">
        `;
        analysis.next_steps.forEach((step, idx) => {
            detailedHTML += `<li style="margin: 0.75rem 0; line-height: 1.6;">${step}</li>`;
        });
        detailedHTML += `</ol>`;
    }
    
    // CLINICAL RECOMMENDATIONS
    if (analysis.clinical_recommendations && Array.isArray(analysis.clinical_recommendations) && analysis.clinical_recommendations.length > 0) {
        detailedHTML += `
            <div style="background: #fef3c7; border-left: 4px solid #f59e0b; padding: 1rem; margin: 1.5rem 0; border-radius: 0.5rem;">
                <h4 style="color: #b45309; margin-top: 0;">🔔 CLINICAL RECOMMENDATIONS</h4>
                <ul style="list-style-position: inside; color: #78350f;">
        `;
        analysis.clinical_recommendations.forEach(rec => {
            detailedHTML += `<li style="margin: 0.5rem 0;">${rec}</li>`;
        });
        detailedHTML += `</ul></div>`;
    }
    
    detailedHTML += `</div>`;
    document.getElementById('detailedAnalysis').innerHTML = detailedHTML;
    
    // Display recommendations (keep for backward compatibility)
    let recommendationsHTML = ``;
    if (analysis.recommendations && analysis.recommendations.length > 0) {
        recommendationsHTML = `<ul style="list-style-position: inside;">`;
        analysis.recommendations.forEach(rec => {
            recommendationsHTML += `<li style="margin: 0.75rem 0;">${rec}</li>`;
        });
        recommendationsHTML += `</ul>`;
    }
    
    document.getElementById('recommendations').innerHTML = recommendationsHTML;
    
    // Scroll to results
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function resetUpload() {
    selectedFile = null;
    fileInput.value = '';
    fileInfo.style.display = 'none';
    analyzeBtn.style.display = 'none';
    resultsSection.style.display = 'none';
    loadingSection.style.display = 'none';
    uploadSection.scrollIntoView({ behavior: 'smooth' });
}

// Load about info on page load
document.addEventListener('DOMContentLoaded', () => {
    loadAboutInfo();
});

async function loadAboutInfo() {
    try {
        const response = await fetch('/api/about');
        const data = await response.json();
        console.log('Platform Info:', data);
    } catch (error) {
        console.error('Error loading about info:', error);
    }
}