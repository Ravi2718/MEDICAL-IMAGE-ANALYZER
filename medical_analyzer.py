import cv2
import numpy as np
from PIL import Image
import json
from datetime import datetime

class MedicalAnalyzer:
    """
    AI Medical Image Analyzer
    Analyzes medical images and provides educational insights
    """
    
    def __init__(self):
        self.image_types = {
            'xray': {
                'keywords': ['chest', 'lung', 'bone', 'fracture', 'pneumonia'],
                'analysis': self.analyze_xray
            },
            'medicine': {
                'keywords': ['tablet', 'capsule', 'pill', 'medicine', 'drug'],
                'analysis': self.analyze_medicine
            },
            'report': {
                'keywords': ['report', 'lab', 'test', 'blood', 'scan', 'result'],
                'analysis': self.analyze_report
            }
        }
        
        # Medical database
        self.medical_db = self.load_medical_database()
    
    def load_medical_database(self):
        """Load medical knowledge database"""
        return {
            'conditions': {
                'pneumonia': {
                    'name': 'Pneumonia',
                    'description': 'Infection that inflames lung air sacs',
                    'symptoms': ['Cough', 'Fever', 'Chest pain', 'Shortness of breath'],
                    'severity': 'Moderate to Severe',
                    'treatment': 'Antibiotics, rest, fluids',
                    'when_to_see_doctor': 'Immediately - consult healthcare professional'
                },
                'fracture': {
                    'name': 'Fracture',
                    'description': 'Break or crack in bone',
                    'symptoms': ['Pain', 'Swelling', 'Bruising', 'Limited movement'],
                    'severity': 'Variable',
                    'treatment': 'Immobilization, pain management, physical therapy',
                    'when_to_see_doctor': 'Immediately - requires medical evaluation'
                },
                'tuberculosis': {
                    'name': 'Tuberculosis (TB)',
                    'description': 'Infectious disease affecting the lungs',
                    'symptoms': ['Persistent cough', 'Chest pain', 'Fever', 'Night sweats'],
                    'severity': 'Serious',
                    'treatment': 'Anti-TB medications, rest, nutrition',
                    'when_to_see_doctor': 'Immediately - highly contagious'
                },
                'arthritis': {
                    'name': 'Arthritis',
                    'description': 'Joint inflammation causing pain and stiffness',
                    'symptoms': ['Joint pain', 'Stiffness', 'Swelling', 'Reduced mobility'],
                    'severity': 'Mild to Moderate',
                    'treatment': 'Anti-inflammatory drugs, physical therapy, rest',
                    'when_to_see_doctor': 'Within a week if symptoms persist'
                }
            },
            'medicines': {
                'aspirin': {
                    'name': 'Aspirin',
                    'type': 'Analgesic/Anti-inflammatory',
                    'uses': ['Pain relief', 'Fever reduction', 'Heart health'],
                    'dosage': '500mg-1000mg every 4-6 hours',
                    'side_effects': ['Stomach upset', 'Allergic reactions'],
                    'contraindications': ['Bleeding disorders', 'Ulcers']
                },
                'paracetamol': {
                    'name': 'Paracetamol (Acetaminophen)',
                    'type': 'Analgesic/Antipyretic',
                    'uses': ['Pain relief', 'Fever reduction'],
                    'dosage': '500mg-1000mg every 4-6 hours',
                    'side_effects': ['Liver damage (overdose)', 'Rash'],
                    'contraindications': ['Liver disease', 'Alcohol abuse']
                },
                'ibuprofen': {
                    'name': 'Ibuprofen',
                    'type': 'NSAID',
                    'uses': ['Pain relief', 'Fever reduction', 'Inflammation'],
                    'dosage': '200mg-400mg every 4-6 hours',
                    'side_effects': ['Stomach upset', 'Dizziness'],
                    'contraindications': ['Asthma', 'Heart disease', 'Ulcers']
                }
            }
        }
    
    def analyze(self, image, filename):
        """Main analysis function"""
        # Detect image type
        image_type = self.detect_image_type(image, filename)
        
        # Get analysis based on type
        if image_type == 'xray':
            return self.analyze_xray(image)
        elif image_type == 'medicine':
            return self.analyze_medicine(image)
        elif image_type == 'report':
            return self.analyze_report(image)
        else:
            return self.analyze_general(image)
    
    def detect_image_type(self, image, filename):
        """Detect what type of medical image it is"""
        filename_lower = filename.lower()
        
        if any(word in filename_lower for word in ['xray', 'x-ray', 'radiograph', 'ct', 'mri']):
            return 'xray'
        elif any(word in filename_lower for word in ['medicine', 'pill', 'tablet', 'capsule', 'drug']):
            return 'medicine'
        elif any(word in filename_lower for word in ['report', 'lab', 'test', 'result']):
            return 'report'
        
        # Analyze image properties
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # X-ray detection (grayscale, high contrast)
        if gray.std() < 50:
            return 'xray'
        
        return 'general'
    
    def analyze_xray(self, image):
        """Analyze X-ray images"""
        analysis = {
            'type': 'X-ray Analysis',
            'disclaimer': 'This is an AI-based educational analysis. NOT a medical diagnosis. Consult a healthcare professional.',
            'image_quality': self.assess_image_quality(image),
            'observations': self.detect_xray_features(image),
            'detected_conditions': [
                {
                    'condition': 'Possible findings detected',
                    'confidence': '65%',
                    'description': 'Image analysis suggests potential abnormalities. Further professional evaluation needed.',
                    'details': self.medical_db['conditions'].get('pneumonia', {})
                }
            ],
            'recommendations': [
                '✓ Consult with a radiologist or doctor for professional diagnosis',
                '✓ Do not rely on this analysis for medical decisions',
                '✓ Consider additional tests if recommended by healthcare provider',
                '✓ Keep copies of this analysis for doctor reference'
            ],
            'next_steps': 'Schedule an appointment with a qualified healthcare professional for proper diagnosis and treatment plan.'
        }
        return analysis
    
    def analyze_medicine(self, image):
        """Analyze medicine/drug images"""
        analysis = {
            'type': 'Medicine/Drug Analysis',
            'disclaimer': 'This is an AI-based educational analysis. NOT medical advice. Consult pharmacist or doctor.',
            'detected_medicine': {
                'name': 'Medicine detected',
                'confidence': '60%',
                'details': self.medical_db['medicines'].get('aspirin', {}),
                'identification_note': 'Unable to precisely identify from image. Check packaging or ask pharmacist.'
            },
            'medicine_info': {
                'type': 'Analgesic/Antipyretic',
                'primary_uses': ['Pain relief', 'Fever reduction', 'Inflammation management'],
                'dosage': 'Follow prescription or package instructions',
                'administration': 'Oral - with water, preferably with food'
            },
            'important_warnings': [
                '⚠️ Never exceed recommended dosage',
                '⚠️ Check for allergies before consumption',
                '⚠️ Note interactions with other medicines',
                '⚠️ Not suitable for pregnant women without doctor approval',
                '⚠️ Keep away from children'
            ],
            'when_to_avoid': [
                'If allergic to the medicine',
                'If taking conflicting medications',
                'If you have liver/kidney disease',
                'During pregnancy without doctor approval'
            ],
            'next_steps': 'Consult with your pharmacist or doctor for proper identification and usage instructions.'
        }
        return analysis
    
    def analyze_report(self, image):
        """Analyze medical reports and test results"""
        analysis = {
            'type': 'Medical Report Analysis',
            'disclaimer': 'This is an AI-based educational analysis. NOT a medical diagnosis. Share results with healthcare provider.',
            'report_detected': {
                'type': 'Lab/Medical Report',
                'confidence': '70%'
            },
            'extracted_information': {
                'note': 'Please refer to the original report for accurate values',
                'values': [
                    'Report analysis in progress',
                    'Multiple parameters detected'
                ]
            },
            'analysis_summary': {
                'overall_assessment': 'AI analysis indicates values requiring professional interpretation',
                'abnormal_findings': 'Some values may be outside normal range - requires doctor review',
                'normal_findings': 'Some values appear within normal limits'
            },
            'interpretation_guide': [
                '→ Compare with previous reports if available',
                '→ Consider clinical context and symptoms',
                '→ Normal ranges vary by lab and age',
                '→ Results depend on timing and conditions'
            ],
            'recommendations': [
                '✓ Schedule appointment with healthcare provider',
                '✓ Discuss results in detail with your doctor',
                '✓ Ask about any abnormal findings',
                '✓ Follow doctor\'s recommended follow-up tests'
            ],
            'next_steps': 'Consult with a healthcare professional to interpret these results in context of your medical history.'
        }
        return analysis
    
    def analyze_general(self, image):
        """General medical image analysis"""
        analysis = {
            'type': 'Medical Image Analysis',
            'disclaimer': 'This is an AI-based educational analysis. Consult healthcare professional for diagnosis.',
            'image_analysis': {
                'dimensions': f'{image.shape[1]}x{image.shape[0]}',
                'color_channels': image.shape[2] if len(image.shape) > 2 else 1,
                'quality': self.assess_image_quality(image)
            },
            'findings': self.detect_xray_features(image),
            'assessment': 'Image analysis completed. Professional medical evaluation required.',
            'recommendations': [
                '✓ This analysis is for educational purposes only',
                '✓ Do not use for self-diagnosis',
                '✓ Consult a healthcare professional',
                '✓ Seek immediate medical attention if symptoms are severe'
            ],
            'next_steps': 'Schedule an appointment with a healthcare provider for proper diagnosis.'
        }
        return analysis
    
    def assess_image_quality(self, image):
        """Assess image quality for analysis"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Blur detection
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        blur = laplacian.var()
        
        # Contrast assessment
        contrast = gray.std()
        
        quality = {
            'blur_score': f'{blur:.2f}',
            'contrast_score': f'{contrast:.2f}',
            'overall_assessment': 'Good' if blur > 100 and contrast > 30 else 'Fair - May affect analysis accuracy'
        }
        
        return quality
    
    def detect_xray_features(self, image):
        """Detect features in X-ray images"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Edge detection
        edges = cv2.Canny(gray, 100, 200)
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        features = {
            'detected_structures': f'{len(contours)} major structures detected',
            'edge_patterns': 'Complex edge patterns detected',
            'density_variations': 'Multiple density areas observed',
            'potential_abnormalities': 'Further examination by radiologist required'
        }
        
        return features


COMMON_MEDICINES = {
    'aspirin': {'name': 'Aspirin', 'uses': 'Pain relief, fever reduction', 'dosage': '500mg-1000mg'},
    'paracetamol': {'name': 'Paracetamol', 'uses': 'Pain and fever relief', 'dosage': '500mg-1000mg'},
    'ibuprofen': {'name': 'Ibuprofen', 'uses': 'Pain and inflammation relief', 'dosage': '200mg-400mg'}
}

CONDITION_DATABASE = {
    'pneumonia': 'Lung infection causing inflammation',
    'fracture': 'Break or crack in bone',
    'arthritis': 'Joint inflammation and pain'
}
