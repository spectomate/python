document.addEventListener('DOMContentLoaded', () => {
    // Initialize syntax highlighting
    hljs.highlightAll();
    
    // Handle documentation tab switching
    const docLinks = document.querySelectorAll('.docs-menu a');
    const docSections = document.querySelectorAll('.doc-section');
    
    docLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active class from all links and sections
            docLinks.forEach(l => l.classList.remove('active'));
            docSections.forEach(s => s.classList.remove('active'));
            
            // Add active class to clicked link
            link.classList.add('active');
            
            // Show corresponding section
            const targetSection = document.getElementById(link.getAttribute('data-doc'));
            if (targetSection) {
                targetSection.classList.add('active');
            }
        });
    });
    
    // Handle format selection and code highlighting
    const sourceFormatSelect = document.getElementById('source-format');
    const targetFormatSelect = document.getElementById('target-format');
    const sourceCode = document.getElementById('source-code');
    const targetCode = document.getElementById('target-code');
    
    // Sample data for different formats
    const sampleData = {
        pip: `numpy==1.22.0
pandas>=1.4.0
requests==2.27.1
# Development dependencies
pytest>=7.0.0
black==22.1.0`,
        conda: `name: myproject
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - numpy=1.22.0
  - pandas>=1.4.0
  - requests=2.27.1
  - pip:
    - pytest>=7.0.0
    - black==22.1.0`,
        poetry: `[tool.poetry]
name = "myproject"
version = "0.1.0"
description = ""
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.9"
numpy = "1.22.0"
pandas = ">=1.4.0"
requests = "2.27.1"

[tool.poetry.dev-dependencies]
pytest = ">=7.0.0"
black = "22.1.0"
`
    };
    
    // Update source code based on selected format
    sourceFormatSelect.addEventListener('change', () => {
        const format = sourceFormatSelect.value;
        sourceCode.textContent = sampleData[format];
        
        // Update language class for syntax highlighting
        sourceCode.className = getLanguageClass(format);
        
        // Re-highlight
        hljs.highlightElement(sourceCode);
    });
    
    // Update target code based on selected format
    targetFormatSelect.addEventListener('change', () => {
        const format = targetFormatSelect.value;
        
        // Update language class for syntax highlighting
        targetCode.className = getLanguageClass(format);
        
        // Simulate conversion
        simulateConversion();
    });
    
    // Convert button click handler
    document.getElementById('convert-btn').addEventListener('click', () => {
        simulateConversion();
    });
    
    // Helper function to get language class for syntax highlighting
    function getLanguageClass(format) {
        switch (format) {
            case 'pip':
                return 'language-python';
            case 'conda':
                return 'language-yaml';
            case 'poetry':
                return 'language-toml';
            default:
                return 'language-python';
        }
    }
    
    // Simulate conversion between formats
    function simulateConversion() {
        const sourceFormat = sourceFormatSelect.value;
        const targetFormat = targetFormatSelect.value;
        const projectName = document.getElementById('project-name').value || 'myproject';
        const projectVersion = document.getElementById('project-version').value || '0.1.0';
        
        // In a real application, this would call the API
        // For demo purposes, we'll just show the sample data
        targetCode.textContent = sampleData[targetFormat];
        
        // Re-highlight
        hljs.highlightElement(targetCode);
        
        // Show success message (in a real app)
        console.log(`Converted from ${sourceFormat} to ${targetFormat}`);
    }
    
    // API integration (would be implemented in a real application)
    async function convertViaAPI(sourceFormat, targetFormat, sourceContent, options) {
        try {
            const response = await fetch('/api/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    source_format: sourceFormat,
                    target_format: targetFormat,
                    source_content: sourceContent,
                    options: options
                })
            });
            
            if (!response.ok) {
                throw new Error('Conversion failed');
            }
            
            const data = await response.json();
            return data.target_content;
        } catch (error) {
            console.error('Error during conversion:', error);
            return null;
        }
    }
});
