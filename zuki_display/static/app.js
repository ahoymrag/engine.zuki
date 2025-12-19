// Zuki Display - Three.js 3D Animated Face
// Kid-friendly animated robot face with big expressive eyes

let scene, camera, renderer;
let face, leftEye, rightEye, leftPupil, rightPupil, mouth;
let currentExpression = 'happy';
let eyeAnimation = { time: 0, blinkTimer: 0, lookDirection: { x: 0, y: 0 } };

// Initialize Three.js scene
function init() {
    // Scene setup
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xfecfef);
    
    // Camera setup
    const container = document.getElementById('face-container');
    const width = container.clientWidth;
    const height = container.clientHeight;
    
    camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000);
    camera.position.z = 5;
    
    // Renderer setup
    const canvas = document.getElementById('zuki-canvas');
    renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);
    
    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.6);
    directionalLight.position.set(5, 5, 5);
    scene.add(directionalLight);
    
    // Create Zuki's face
    createFace();
    
    // Handle window resize
    window.addEventListener('resize', onWindowResize);
    
    // Menu button handlers
    setupMenuButtons();
    
    // Start animation loop
    animate();
}

// Create Zuki's 3D face
function createFace() {
    const faceGroup = new THREE.Group();
    
    // Main face (soft rounded shape)
    const faceGeometry = new THREE.SphereGeometry(1.5, 32, 32);
    const faceMaterial = new THREE.MeshPhongMaterial({
        color: 0xffd4e5,
        shininess: 30,
        flatShading: false
    });
    face = new THREE.Mesh(faceGeometry, faceMaterial);
    faceGroup.add(face);
    
    // Left Eye (big and expressive)
    const eyeGeometry = new THREE.SphereGeometry(0.4, 32, 32);
    const eyeMaterial = new THREE.MeshPhongMaterial({
        color: 0xffffff,
        shininess: 100
    });
    
    leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    leftEye.position.set(-0.5, 0.3, 1.2);
    faceGroup.add(leftEye);
    
    // Left Pupil
    const pupilGeometry = new THREE.SphereGeometry(0.25, 32, 32);
    const pupilMaterial = new THREE.MeshPhongMaterial({
        color: 0x6bc8cd,
        shininess: 50
    });
    leftPupil = new THREE.Mesh(pupilGeometry, pupilMaterial);
    leftPupil.position.set(-0.5, 0.3, 1.4);
    faceGroup.add(leftPupil);
    
    // Right Eye
    rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    rightEye.position.set(0.5, 0.3, 1.2);
    faceGroup.add(rightEye);
    
    // Right Pupil
    rightPupil = new THREE.Mesh(pupilGeometry, pupilMaterial);
    rightPupil.position.set(0.5, 0.3, 1.4);
    faceGroup.add(rightPupil);
    
    // Mouth (will be animated)
    const mouthGeometry = new THREE.TorusGeometry(0.3, 0.1, 16, 32, Math.PI);
    const mouthMaterial = new THREE.MeshPhongMaterial({
        color: 0xff6b9d,
        shininess: 30
    });
    mouth = new THREE.Mesh(mouthGeometry, mouthMaterial);
    mouth.position.set(0, -0.4, 1.2);
    mouth.rotation.x = Math.PI;
    faceGroup.add(mouth);
    
    // Cheeks (cute rosy cheeks)
    const cheekGeometry = new THREE.SphereGeometry(0.2, 16, 16);
    const cheekMaterial = new THREE.MeshPhongMaterial({
        color: 0xffb3d9,
        shininess: 20
    });
    
    const leftCheek = new THREE.Mesh(cheekGeometry, cheekMaterial);
    leftCheek.position.set(-0.8, -0.2, 1.1);
    faceGroup.add(leftCheek);
    
    const rightCheek = new THREE.Mesh(cheekGeometry, cheekMaterial);
    rightCheek.position.set(0.8, -0.2, 1.1);
    faceGroup.add(rightCheek);
    
    scene.add(faceGroup);
}

// Update expression based on button click
function setExpression(expression) {
    currentExpression = expression;
    updateStatus(`Feeling ${expression}!`);
    
    // Reset all scales first
    if (leftEye) leftEye.scale.set(1, 1, 1);
    if (rightEye) rightEye.scale.set(1, 1, 1);
    if (leftPupil) leftPupil.scale.set(1, 1, 1);
    if (rightPupil) rightPupil.scale.set(1, 1, 1);
    if (mouth) {
        mouth.scale.set(1, 1, 1);
        mouth.rotation.x = Math.PI;
    }
    
    switch(expression) {
        case 'happy':
            // Big smile
            mouth.scale.y = 1.5;
            mouth.rotation.x = Math.PI;
            face.material.color.setHex(0xffd4e5);
            break;
            
        case 'excited':
            // Very big smile, eyes wide
            mouth.scale.y = 2;
            mouth.rotation.x = Math.PI;
            leftEye.scale.set(1.2, 1.2, 1);
            rightEye.scale.set(1.2, 1.2, 1);
            face.material.color.setHex(0xffe5f0);
            break;
            
        case 'sleepy':
            // Half-closed eyes, small smile
            leftEye.scale.set(1, 0.3, 1);
            rightEye.scale.set(1, 0.3, 1);
            mouth.scale.y = 0.8;
            face.material.color.setHex(0xe5d4ff);
            break;
            
        case 'surprised':
            // Wide open eyes, O mouth
            leftEye.scale.set(1.3, 1.3, 1);
            rightEye.scale.set(1.3, 1.3, 1);
            mouth.scale.set(0.8, 0.8, 1);
            mouth.rotation.x = Math.PI / 2;
            face.material.color.setHex(0xfff0d4);
            break;
            
        case 'wink':
            // One eye closed
            leftEye.scale.set(1, 0.1, 1);
            rightEye.scale.set(1, 1, 1);
            mouth.scale.y = 1.2;
            face.material.color.setHex(0xffd4e5);
            break;
            
        case 'love':
            // Heart eyes effect (bigger pupils, happy face)
            leftPupil.scale.set(1.3, 1.3, 1);
            rightPupil.scale.set(1.3, 1.3, 1);
            mouth.scale.y = 1.5;
            face.material.color.setHex(0xffb3d9);
            break;
            
        case 'sad':
            // Frown, smaller eyes
            leftEye.scale.set(1, 0.8, 1);
            rightEye.scale.set(1, 0.8, 1);
            mouth.scale.y = 0.6;
            mouth.rotation.x = Math.PI * 1.2;
            face.material.color.setHex(0xd4e5ff);
            break;
            
        default:
            // Reset to default
            leftEye.scale.set(1, 1, 1);
            rightEye.scale.set(1, 1, 1);
            mouth.scale.set(1, 1, 1);
            mouth.rotation.x = Math.PI;
            face.material.color.setHex(0xffd4e5);
    }
}

// Animate the face
function animate() {
    requestAnimationFrame(animate);
    
    eyeAnimation.time += 0.02;
    eyeAnimation.blinkTimer += 0.01;
    
    // Gentle rotation of the face
    if (scene.children.length > 0) {
        scene.children[0].rotation.y = Math.sin(eyeAnimation.time * 0.5) * 0.1;
    }
    
    // Blinking animation
    if (Math.sin(eyeAnimation.blinkTimer) < -0.8) {
        const blinkAmount = Math.abs(Math.sin(eyeAnimation.blinkTimer * 5));
        leftEye.scale.y = Math.max(0.1, 1 - blinkAmount * 0.9);
        rightEye.scale.y = Math.max(0.1, 1 - blinkAmount * 0.9);
    } else {
        // Restore eye size if not blinking
        if (currentExpression !== 'sleepy' && currentExpression !== 'wink') {
            leftEye.scale.y = 1;
            rightEye.scale.y = 1;
        }
    }
    
    // Pupil movement (following mouse or gentle wandering)
    const currentMouseEvent = window.lastMouseEvent || null;
    const mouseX = currentMouseEvent ? (currentMouseEvent.clientX / window.innerWidth) * 2 - 1 : 0;
    const mouseY = currentMouseEvent ? -(currentMouseEvent.clientY / window.innerHeight) * 2 + 1 : 0;
    
    const maxOffset = 0.15;
    leftPupil.position.x = -0.5 + mouseX * maxOffset;
    leftPupil.position.y = 0.3 + mouseY * maxOffset;
    rightPupil.position.x = 0.5 + mouseX * maxOffset;
    rightPupil.position.y = 0.3 + mouseY * maxOffset;
    
    // Gentle mouth animation
    mouth.rotation.z = Math.sin(eyeAnimation.time) * 0.1;
    
    renderer.render(scene, camera);
}

// Handle window resize
function onWindowResize() {
    const container = document.getElementById('face-container');
    const width = container.clientWidth;
    const height = container.clientHeight;
    
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
}

// Setup menu button handlers
function setupMenuButtons() {
    // Expression buttons
    const expressionButtons = document.querySelectorAll('.menu-btn[data-action]');
    expressionButtons.forEach(button => {
        button.addEventListener('click', () => {
            const action = button.getAttribute('data-action');
            setExpression(action);
            
            // Visual feedback
            button.style.transform = 'scale(0.95)';
            setTimeout(() => {
                button.style.transform = '';
            }, 150);
        });
    });
    
    // Feature buttons
    const featureButtons = document.querySelectorAll('.menu-btn[data-feature]');
    featureButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const feature = button.getAttribute('data-feature');
            await handleFeature(feature);
            
            // Visual feedback
            button.style.transform = 'scale(0.95)';
            setTimeout(() => {
                button.style.transform = '';
            }, 150);
        });
    });
    
    // Chat send button
    const chatSendBtn = document.getElementById('chat-send');
    const chatInput = document.getElementById('chat-input');
    
    if (chatSendBtn && chatInput) {
        chatSendBtn.addEventListener('click', sendChatMessage);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        });
    }
}

// Update status display
function updateStatus(text) {
    const statusElement = document.getElementById('status-text');
    if (statusElement) {
        statusElement.textContent = text;
    }
}

// Update mood display
function updateMood(mood) {
    const moodElement = document.getElementById('mood-text');
    if (moodElement) {
        moodElement.textContent = mood.charAt(0).toUpperCase() + mood.slice(1);
    }
    
    // Update face expression based on mood
    if (mood === 'sad') {
        setExpression('sad');
    } else if (mood === 'lonely') {
        setExpression('sleepy');
    } else {
        setExpression('happy');
    }
}

// Handle Zuki features
async function handleFeature(feature) {
    updateStatus('Processing...');
    
    try {
        switch(feature) {
            case 'greet':
                const greetResponse = await fetch('/api/greet', { method: 'POST' });
                const greetData = await greetResponse.json();
                if (greetData.success) {
                    updateStatus('Zuki greeted!');
                    setExpression('happy');
                    addChatMessage('Zuki', greetData.message);
                } else {
                    updateStatus('Error: ' + greetData.message);
                }
                break;
                
            case 'sense':
                const senseResponse = await fetch('/api/sense');
                const senseData = await senseResponse.json();
                if (senseData.success) {
                    updateStatus('Sensors read!');
                    addChatMessage('Zuki', 'Sensor data: ' + senseData.data);
                } else {
                    updateStatus('Error: ' + senseData.message);
                }
                break;
                
            case 'magic':
                updateStatus('Magic trick - check console/terminal!');
                addChatMessage('Zuki', '🪄 Magic trick started! Check the server console for the game.');
                // Note: Games require terminal interaction, so we show a message
                alert('Magic trick requires terminal interaction. Please run "zuki magic" in the server console.');
                break;
                
            case '20q':
                updateStatus('20 Questions - check console/terminal!');
                addChatMessage('Zuki', '❓ 20 Questions started! Check the server console for the game.');
                alert('20 Questions requires terminal interaction. Please run "20 questions" in the server console.');
                break;
                
            case 'notes':
                const notesResponse = await fetch('/api/notes');
                const notesData = await notesResponse.json();
                if (notesData.success) {
                    updateStatus('Notes loaded!');
                    addChatMessage('Zuki', '📒 Notes:\n' + notesData.notes);
                } else {
                    updateStatus('Error: ' + notesData.message);
                }
                break;
                
            case 'care':
                const careResponse = await fetch('/api/care-guide');
                const careData = await careResponse.json();
                if (careData.success) {
                    updateStatus('Care guide loaded!');
                    addChatMessage('Zuki', '💝 Care Guide:\n' + careData.guide);
                } else {
                    updateStatus('Error: ' + careData.message);
                }
                break;
        }
    } catch (error) {
        updateStatus('Error: ' + error.message);
        console.error('Feature error:', error);
    }
}

// Send chat message
async function sendChatMessage() {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addChatMessage('You', message);
    chatInput.value = '';
    
    updateStatus('Zuki is thinking...');
    setExpression('surprised');
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        if (data.success) {
            updateStatus('Zuki replied!');
            setExpression('happy');
            addChatMessage('Zuki', data.response);
        } else {
            updateStatus('Error: ' + data.message);
            setExpression('sad');
            addChatMessage('Zuki', 'Sorry, I had trouble understanding. ' + data.message);
        }
    } catch (error) {
        updateStatus('Error: ' + error.message);
        setExpression('sad');
        addChatMessage('Zuki', 'Sorry, I encountered an error. Please try again.');
    }
}

// Add message to chat display
function addChatMessage(sender, message) {
    const chatMessages = document.getElementById('chat-messages');
    if (!chatMessages) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chat-message';
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${message.replace(/\n/g, '<br>')}`;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Check Zuki's mood periodically
async function checkMood() {
    try {
        const response = await fetch('/api/mood');
        const data = await response.json();
        
        if (data.success) {
            updateMood(data.mood);
            if (data.message) {
                // Show mood message in chat if there is one
                const chatMessages = document.getElementById('chat-messages');
                if (chatMessages && chatMessages.children.length === 0) {
                    addChatMessage('Zuki', data.message);
                }
            }
        }
    } catch (error) {
        console.error('Mood check error:', error);
    }
}

// Check status on load
async function checkStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        if (data.modules_available) {
            updateStatus('All features available!');
        } else {
            updateStatus('Display mode only');
            addChatMessage('System', '⚠️ Zuki modules not found. Running in display-only mode.');
        }
        
        if (data.mood) {
            updateMood(data.mood);
        }
    } catch (error) {
        console.error('Status check error:', error);
        updateStatus('Connection error');
    }
}

// Track mouse movement for eye following
document.addEventListener('mousemove', (event) => {
    window.lastMouseEvent = event;
});

// Initialize when page loads
window.addEventListener('load', () => {
    init();
    checkStatus();
    // Check mood every 30 seconds
    setInterval(checkMood, 30000);
});

