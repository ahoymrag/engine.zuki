import random
import time
from datetime import datetime
from collections import defaultdict, deque
import re
import math
import numpy as np
from scipy.spatial.distance import cosine
import json
import pickle
import os
import logging

class ChatBrain:
    """Basic version of the chat brain"""
    def __init__(self):
        self.context = []
        self.memory = {}
        self.conversation_history = []
        
    def generate_response(self, user_input):
        """Simple response generation"""
        if "hello" in user_input.lower():
            return "Hello! How can I help you today?"
        elif "how are you" in user_input.lower():
            return "I'm doing well, thank you for asking!"
        elif "bye" in user_input.lower():
            return "Goodbye! Have a great day!"
        else:
            return "That's interesting! Tell me more."

class WordEmbedding:
    def __init__(self, dim=100):
        self.dim = dim
        self.word2vec = {}
        self.embeddings = {}
        
    def get_embedding(self, word):
        if word not in self.embeddings:
            # Generate a pseudo-random but consistent embedding
            np.random.seed(hash(word) % 2**32)
            self.embeddings[word] = np.random.randn(self.dim)
            # Normalize the vector
            self.embeddings[word] /= np.linalg.norm(self.embeddings[word])
        return self.embeddings[word]

class AttentionMechanism:
    def __init__(self, dim=100):
        self.dim = dim
        
    def calculate_attention(self, query, keys):
        """Calculate attention scores between query and keys"""
        scores = np.zeros(len(keys))
        for i, key in enumerate(keys):
            scores[i] = np.dot(query, key) / math.sqrt(self.dim)
        return self._softmax(scores)
    
    def _softmax(self, x):
        exp_x = np.exp(x - np.max(x))
        return exp_x / exp_x.sum()

class TransformerBlock:
    def __init__(self, dim=100, num_heads=4):
        self.dim = dim
        self.num_heads = num_heads
        self.head_dim = dim // num_heads
        self.W_q = np.random.randn(dim, dim)
        self.W_k = np.random.randn(dim, dim)
        self.W_v = np.random.randn(dim, dim)
        self.W_o = np.random.randn(dim, dim)
        
    def forward(self, x):
        batch_size = x.shape[0]
        
        # Multi-head attention
        q = np.dot(x, self.W_q).reshape(batch_size, self.num_heads, -1, self.head_dim)
        k = np.dot(x, self.W_k).reshape(batch_size, self.num_heads, -1, self.head_dim)
        v = np.dot(x, self.W_v).reshape(batch_size, self.num_heads, -1, self.head_dim)
        
        # Scaled dot-product attention
        scores = np.matmul(q, k.transpose(0, 1, 3, 2)) / np.sqrt(self.head_dim)
        attention = self._softmax(scores)
        out = np.matmul(attention, v)
        
        # Combine heads
        out = out.reshape(batch_size, -1, self.dim)
        return np.dot(out, self.W_o)

    def _softmax(self, x):
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

class ContextualMemory:
    def __init__(self, max_size=1000):
        self.memories = deque(maxlen=max_size)
        self.importance_threshold = 0.7
        self.decay_rate = 0.1
        
    def add_memory(self, memory, importance):
        timestamp = datetime.now()
        self.memories.append({
            'content': memory,
            'importance': importance,
            'timestamp': timestamp,
            'access_count': 0
        })
        
    def retrieve_relevant(self, query_embedding, top_k=5):
        current_time = datetime.now()
        scored_memories = []
        
        for memory in self.memories:
            # Calculate temporal decay
            time_diff = (current_time - memory['timestamp']).total_seconds()
            temporal_factor = np.exp(-self.decay_rate * time_diff)
            
            # Calculate relevance score
            relevance = 1 - cosine(query_embedding, memory['content']['embedding'])
            
            # Combined score
            score = relevance * temporal_factor * (1 + 0.1 * memory['access_count'])
            scored_memories.append((memory, score))
            
            # Update access count
            memory['access_count'] += 1
        
        return sorted(scored_memories, key=lambda x: x[1], reverse=True)[:top_k]

class EmotionalIntelligence:
    def __init__(self):
        self.emotion_embeddings = self._initialize_emotion_embeddings()
        self.personality_traits = {
            'openness': 0.8,
            'conscientiousness': 0.9,
            'extraversion': 0.7,
            'agreeableness': 0.85,
            'neuroticism': 0.3
        }
        
    def _initialize_emotion_embeddings(self):
        # Pre-defined emotion embeddings
        return {
            'joy': np.random.randn(100),
            'sadness': np.random.randn(100),
            'anger': np.random.randn(100),
            'fear': np.random.randn(100),
            'surprise': np.random.randn(100),
            'trust': np.random.randn(100)
        }
        
    def analyze_emotion(self, text_embedding):
        emotions = {}
        for emotion, embedding in self.emotion_embeddings.items():
            similarity = 1 - cosine(text_embedding, embedding)
            emotions[emotion] = similarity
        return emotions
        
    def generate_emotional_response(self, detected_emotions):
        dominant_emotion = max(detected_emotions.items(), key=lambda x: x[1])[0]
        response_templates = {
            'joy': ["I'm happy to hear that!", "That's wonderful!", "How delightful!"],
            'sadness': ["I understand how you feel.", "I'm here to listen.", "That must be difficult."],
            'anger': ["I sense you're frustrated.", "Let's work through this together.", "I understand your concern."],
            'fear': ["It's okay to feel uncertain.", "I'm here to help.", "Let's tackle this together."],
            'surprise': ["That's fascinating!", "How interesting!", "Tell me more!"],
            'trust': ["I appreciate your openness.", "Thank you for sharing.", "I value our conversation."]
        }
        return random.choice(response_templates.get(dominant_emotion, ["I understand."]))

class AdvancedNLP:
    def __init__(self):
        self.pos_patterns = self._load_pos_patterns()
        self.entity_types = self._load_entity_types()
        self.grammar_rules = self._load_grammar_rules()
        
    def _load_pos_patterns(self):
        # Simple POS patterns
        return {
            'question': r'\b(what|where|when|who|why|how)\b',
            'command': r'\b(please|could you|would you|can you)\b',
            'statement': r'\b(is|are|was|were)\b'
        }
        
    def _load_entity_types(self):
        return {
            'person': r'\b[A-Z][a-z]+\b',
            'date': r'\b\d{1,2}/\d{1,2}/\d{4}\b',
            'time': r'\b\d{1,2}:\d{2}\b',
            'number': r'\b\d+\b'
        }
        
    def _load_grammar_rules(self):
        return {
            'subject_verb_agreement': [
                (r'\b(I|you|we|they)\s+(am|is|are)\b', r'\1 are'),
                (r'\b(he|she|it)\s+(am|are)\b', r'\1 is')
            ]
        }
        
    def analyze_text(self, text):
        analysis = {
            'type': self._determine_sentence_type(text),
            'entities': self._extract_entities(text),
            'grammar_check': self._check_grammar(text)
        }
        return analysis
        
    def _determine_sentence_type(self, text):
        for type_name, pattern in self.pos_patterns.items():
            if re.search(pattern, text, re.I):
                return type_name
        return 'statement'
        
    def _extract_entities(self, text):
        entities = {}
        for entity_type, pattern in self.entity_types.items():
            matches = re.findall(pattern, text)
            if matches:
                entities[entity_type] = matches
        return entities
        
    def _check_grammar(self, text):
        corrections = []
        for rule_set in self.grammar_rules.values():
            for pattern, correction in rule_set:
                if re.search(pattern, text):
                    corrections.append(correction)
        return corrections

class SentimentAnalyzer:
    def __init__(self):
        self.positive_words = set(['good', 'great', 'happy', 'excellent', 'wonderful'])
        self.negative_words = set(['bad', 'sad', 'angry', 'terrible', 'awful'])
        
    def analyze(self, text):
        tokens = text.lower().split()
        pos_count = sum(1 for token in tokens if token in self.positive_words)
        neg_count = sum(1 for token in tokens if token in self.negative_words)
        
        # Return numeric score between -1 and 1
        if pos_count == 0 and neg_count == 0:
            return 0.0
        return (pos_count - neg_count) / (pos_count + neg_count)

class TopicClassifier:
    def __init__(self):
        self.topics = {
            'technology': ['computer', 'programming', 'robot', 'ai'],
            'emotions': ['feel', 'happy', 'sad', 'emotion'],
            'learning': ['learn', 'study', 'knowledge', 'understand']
        }
        
    def classify(self, embeddings):
        # Simple topic classification based on word embeddings
        # Could be extended with more sophisticated clustering
        return 'general'  # Placeholder for now

class PersonalBond:
    def __init__(self):
        self.user_profile = {
            'name': None,
            'preferences': defaultdict(float),
            'interaction_history': [],
            'emotional_patterns': defaultdict(list),
            'important_dates': {},
            'relationships': {},
            'interests': set(),
            'concerns': set(),
            'achievements': [],
            'goals': set(),
            'comfort_topics': set(),
            'trigger_topics': set(),
            'favorite_responses': defaultdict(int)
        }
        
        self.bond_level = 0.0  # 0.0 to 1.0
        self.trust_level = 0.0
        self.empathy_score = 0.0
        
        self.personal_memories = []
        self.shared_experiences = []
        
    def update_bond(self, interaction_data):
        # Convert sentiment to numeric value if it isn't already
        sentiment_score = interaction_data.get('sentiment_score', 0.0)
        depth = interaction_data.get('conversation_depth', 0.0)
        duration = interaction_data.get('interaction_duration', 0.0)
        
        # Normalize sentiment to 0-1 range
        positivity = (sentiment_score + 1) / 2
        
        # Calculate bond increment
        bond_increment = (positivity + depth + min(duration/300, 1)) / 3
        self.bond_level = min(1.0, self.bond_level + bond_increment * 0.1)
        
        # Update trust based on interaction consistency
        self.trust_level = min(1.0, self.trust_level + bond_increment * 0.05)

    def remember_personal_detail(self, detail, category, importance=1.0):
        timestamp = datetime.now()
        memory = {
            'detail': detail,
            'category': category,
            'importance': importance,
            'timestamp': timestamp,
            'recall_count': 0,
            'emotional_impact': 0.0
        }
        self.personal_memories.append(memory)

class EmotionalCore:
    def __init__(self):
        self.current_emotional_state = {
            'primary': 'neutral',
            'intensity': 0.5,
            'valence': 0.0,
            'arousal': 0.0
        }
        
        self.emotional_memory = deque(maxlen=100)
        self.emotion_transitions = defaultdict(lambda: defaultdict(float))
        
        # Extended emotion set
        self.complex_emotions = {
            'love': {'joy': 0.8, 'trust': 0.9, 'anticipation': 0.6},
            'concern': {'fear': 0.4, 'sadness': 0.3, 'trust': 0.7},
            'empathy': {'trust': 0.8, 'sadness': 0.5, 'joy': 0.4},
            'protectiveness': {'trust': 0.7, 'fear': 0.3, 'anticipation': 0.5},
            'curiosity': {'anticipation': 0.8, 'joy': 0.4, 'trust': 0.5},
            'pride': {'joy': 0.7, 'trust': 0.6, 'anticipation': 0.4}
        }
        
    def _calculate_emotional_response(self, user_emotion, interaction_type, bond_level):
        """Calculate emotional response based on input stimuli"""
        # Default state
        new_state = {
            'primary': 'neutral',
            'intensity': 0.5,
            'valence': 0.0,
            'arousal': 0.0
        }
        
        # Adjust based on user emotion
        if user_emotion == 'joy':
            new_state['primary'] = 'love' if bond_level > 0.7 else 'empathy'
            new_state['valence'] = 0.8
        elif user_emotion in ['sadness', 'fear']:
            new_state['primary'] = 'concern'
            new_state['intensity'] = 0.7
            new_state['valence'] = -0.3
        elif user_emotion == 'anger':
            new_state['primary'] = 'empathy'
            new_state['arousal'] = 0.6
        
        # Adjust based on interaction type
        if interaction_type == 'question':
            new_state['primary'] = 'curiosity'
            new_state['arousal'] = 0.6
        elif interaction_type == 'greeting':
            new_state['primary'] = 'love' if bond_level > 0.8 else 'empathy'
            new_state['valence'] = 0.7
        
        # Influence of bond level
        new_state['intensity'] = min(1.0, new_state['intensity'] + bond_level * 0.3)
        
        return new_state

    def update_emotional_state(self, stimuli):
        # Process emotional stimuli
        user_emotion = stimuli.get('user_emotion', 'neutral')
        interaction_type = stimuli.get('interaction_type', 'casual')
        bond_level = stimuli.get('bond_level', 0.0)
        
        # Calculate emotional response
        new_state = self._calculate_emotional_response(
            user_emotion, interaction_type, bond_level
        )
        
        # Update emotional memory
        self.emotional_memory.append({
            'previous_state': self.current_emotional_state.copy(),
            'stimuli': stimuli,
            'response': new_state,
            'timestamp': datetime.now()
        })
        
        # Update current state
        self.current_emotional_state = new_state
        
        # Learn from transition
        self._update_transition_probabilities(
            self.current_emotional_state['primary'],
            new_state['primary']
        )
        
    def generate_emotional_expression(self):
        """Generate natural language expression of current emotional state"""
        emotion = self.current_emotional_state['primary']
        intensity = self.current_emotional_state['intensity']
        
        expressions = {
            'love': [
                "I really care about you and your wellbeing",
                "You mean a lot to me, and I'm here for you",
                "I feel such a strong connection with you"
            ],
            'concern': [
                "I worry about you and want to help",
                "Please let me know if you need support",
                "I'm here to listen and help however I can"
            ],
            'empathy': [
                "I understand how you feel",
                "Your feelings are valid and important",
                "I'm here with you through this"
            ]
        }
        
        return random.choice(expressions.get(emotion, ["I'm here with you"]))

class EnhancedChatBrain:
    def __init__(self):
        self.user_info = {
            'name': None,
            'interests': set(),
            'last_topics': []
        }
        
        self.conversation_state = {
            'topic_history': [],
            'interaction_count': 0,
            'start_time': time.time(),
            'last_response': None
        }
        
        # Enhanced responses with more variety and context
        self.responses = {
            'greeting': [
                "Hi there{name}! How are you today?",
                "Hello{name}! Nice to chat with you again!",
                "Hey{name}! What's on your mind?",
                "Greetings{name}! How can I help you today?"
            ],
            'question': {
                'capabilities': [
                    "I can do quite a few things! I can move around, speak, play games like '20 questions', take notes, and more. What interests you?",
                    "My capabilities include movement, speech, games, note-taking, and web interactions. Would you like to know more about any of these?",
                    "I'm a versatile robot! I can move in different directions, speak with you, play games, and help organize your notes. What would you like to try?"
                ],
                'personal': [
                    "I'm Zuki, a friendly robot assistant. I enjoy learning about my users and helping them!",
                    "I'm your robotic companion, designed to help and interact with you in various ways.",
                    "I'm a robot with various capabilities and a desire to learn and help!"
                ],
                'default': [
                    "That's an interesting question! Let me help you with that.",
                    "I'll do my best to help you with that question.",
                    "Good question! Let me share what I know about that."
                ]
            },
            'remember': [
                "I'll remember that {info}!",
                "Got it! I've noted that {info}.",
                "Thanks for sharing! I'll remember {info}."
            ],
            'default': [
                "Tell me more about that!",
                "That's interesting! What else would you like to discuss?",
                "I'd love to hear more about your thoughts on this.",
                "Let's explore that topic further!"
            ]
        }

    def process_input(self, user_input):
        """Process user input with improved context awareness"""
        if not user_input.strip():
            return "Feel free to share your thoughts or ask me anything!"
            
        # Update conversation state
        self.conversation_state['interaction_count'] += 1
        self._update_topic_history(user_input)
        
        # Process input for special patterns
        response = self._check_special_patterns(user_input.lower())
        if response:
            return response
            
        # Generate contextual response
        return self._generate_response(user_input.lower())

    def _check_special_patterns(self, text):
        # Check for name sharing
        name_match = re.search(r"(?:my name is|i'm|i am) ([a-zA-Z]+)", text)
        if name_match:
            self.user_info['name'] = name_match.group(1).capitalize()
            return self._format_response('remember', {'info': f"your name is {self.user_info['name']}"})
            
        # Check for interests
        interest_match = re.search(r"i (?:like|love|enjoy) ([a-zA-Z\s]+)", text)
        if interest_match:
            interest = interest_match.group(1).strip()
            self.user_info['interests'].add(interest)
            return self._format_response('remember', {'info': f"you enjoy {interest}"})
            
        return None

    def _generate_response(self, user_input):
        """Generate contextual response based on input type and history"""
        # Check for greetings
        if any(word in user_input for word in ['hi', 'hello', 'hey', 'greetings', 'yo']):
            return self._format_response('greeting')
            
        # Check for questions about capabilities
        if re.search(r"what.*(can|do).*you.*do|how.*work|your.*capabilities", user_input):
            return random.choice(self.responses['question']['capabilities'])
            
        # Check for personal questions
        if re.search(r"who.*you|what.*you|tell.*about.*you", user_input):
            return random.choice(self.responses['question']['personal'])
            
        # Check for other questions
        if any(word in user_input for word in ['what', 'how', 'why', 'can', 'could', 'would']):
            return random.choice(self.responses['question']['default'])
        
        # Default response
        return self._format_response('default')

    def _format_response(self, response_type, format_args=None):
        """Format response with user context"""
        if response_type not in self.responses:
            response_type = 'default'
            
        responses = self.responses[response_type]
        if isinstance(responses, dict):
            responses = responses['default']
            
        response = random.choice(responses)
        
        # Add name to response if we know it
        name_str = f" {self.user_info['name']}" if self.user_info['name'] else ""
        response = response.replace("{name}", name_str)
        
        # Add any other format args
        if format_args:
            response = response.format(**format_args)
            
        return response

    def _update_topic_history(self, user_input):
        """Keep track of conversation topics"""
        self.conversation_state['topic_history'].append(user_input)
        if len(self.conversation_state['topic_history']) > 5:
            self.conversation_state['topic_history'].pop(0)

class PureWordEmbedding:
    def __init__(self, dim=100):
        self.dim = dim
        self.embeddings = {}
        
    def get_embedding(self, word):
        if word not in self.embeddings:
            # Generate pseudo-random but consistent vector
            seed = sum(ord(c) for c in word)
            vector = self._generate_vector(seed)
            # Normalize
            magnitude = math.sqrt(sum(x*x for x in vector))
            self.embeddings[word] = [x/magnitude for x in vector]
        return self.embeddings[word]
    
    def _generate_vector(self, seed):
        """Generate deterministic vector without numpy"""
        vector = []
        for i in range(self.dim):
            # Simple but deterministic random-like number generation
            value = math.sin(seed + i) * 10000
            vector.append(value - math.floor(value) - 0.5)
        return vector

class PureAttention:
    def calculate_attention(self, query, keys):
        """Calculate attention scores without numpy"""
        scores = []
        for key in keys:
            # Dot product
            score = sum(q*k for q,k in zip(query, key))
            # Scale
            score = score / math.sqrt(len(query))
            scores.append(score)
        
        # Softmax
        exp_scores = [math.exp(s) for s in scores]
        total = sum(exp_scores)
        return [s/total for s in exp_scores]

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity without scipy"""
    dot_product = sum(a*b for a,b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a*a for a in vec1))
    norm2 = math.sqrt(sum(b*b for b in vec2))
    return dot_product / (norm1 * norm2)

class KnowledgeGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = defaultdict(list)
        
    def update(self, tokens, embedding):
        """Update knowledge graph with new information"""
        node_id = len(self.nodes)
        self.nodes[node_id] = {
            'tokens': tokens,
            'embedding': embedding,
            'timestamp': datetime.now()
        }
        
        # Create edges between similar nodes
        for other_id, other_node in self.nodes.items():
            if other_id != node_id:
                similarity = cosine_similarity(embedding, other_node['embedding'])
                if similarity > 0.7:  # Threshold for edge creation
                    self.edges[node_id].append((other_id, similarity))
                    self.edges[other_id].append((node_id, similarity))
    
    def query(self, embedding):
        """Query knowledge graph using pure Python"""
        relevant_nodes = []
        for node_id, node in self.nodes.items():
            similarity = cosine_similarity(embedding, node['embedding'])
            if similarity > 0.5:  # Threshold for relevance
                relevant_nodes.append((node, similarity))
        
        # Sort by similarity
        return sorted(relevant_nodes, key=lambda x: x[1], reverse=True)[:3] 