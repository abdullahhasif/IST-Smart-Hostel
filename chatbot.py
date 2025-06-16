import google.generativeai as genai
from flask import current_app
import os
from datetime import datetime

class HostelChatbot:
    def __init__(self):
        # Initialize Gemini API
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # System prompt to define chatbot behavior
        self.system_prompt = """You are a helpful hostel management assistant. You can help with:
        1. Room booking and availability queries
        2. Complaint submission and tracking
        3. Payment information
        4. General hostel information
        5. Student profile management
        
        Always be polite and professional. If you don't know something, say so.
        Keep responses concise and to the point."""
        
        # Initialize chat history
        self.chat = self.model.start_chat(history=[])
        
    def get_response(self, user_input, user_context=None):
        """
        Get response from the chatbot
        user_context: Dictionary containing user information if available
        """
        try:
            # Add context if available
            if user_context:
                context_str = f"User Context: {user_context}\n"
                prompt = f"{self.system_prompt}\n{context_str}User: {user_input}"
            else:
                prompt = f"{self.system_prompt}\nUser: {user_input}"
            
            # Get response from Gemini
            response = self.chat.send_message(prompt)
            return response.text
            
        except Exception as e:
            current_app.logger.error(f"Chatbot error: {str(e)}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again later."

    def get_room_availability(self, hostel_id=None):
        """Get room availability information"""
        try:
            from app import db
            from models import Room, Hostel
            
            query = Room.query.filter_by(is_available=True)
            if hostel_id:
                query = query.filter_by(hostel_id=hostel_id)
            
            available_rooms = query.all()
            
            if not available_rooms:
                return "No rooms are currently available."
            
            response = "Available rooms:\n"
            for room in available_rooms:
                hostel = Hostel.query.get(room.hostel_id)
                response += f"- Room {room.room_number} in {hostel.name} ({room.room_type})\n"
            
            return response
            
        except Exception as e:
            current_app.logger.error(f"Error getting room availability: {str(e)}")
            return "I'm having trouble checking room availability. Please try again later."

    def get_complaint_status(self, complaint_id):
        """Get status of a specific complaint"""
        try:
            from app import db
            from models import Complaint
            
            complaint = Complaint.query.get(complaint_id)
            if not complaint:
                return "Complaint not found."
            
            return f"Complaint Status: {complaint.status}\nLast Updated: {complaint.updated_at}"
            
        except Exception as e:
            current_app.logger.error(f"Error getting complaint status: {str(e)}")
            return "I'm having trouble checking the complaint status. Please try again later."

    def get_payment_info(self, user_id):
        """Get payment information for a user"""
        try:
            from app import db
            from models import Payment
            
            payments = Payment.query.filter_by(user_id=user_id).order_by(Payment.created_at.desc()).all()
            
            if not payments:
                return "No payment history found."
            
            response = "Recent payments:\n"
            for payment in payments:
                response += f"- {payment.payment_type}: ${payment.amount} ({payment.status})\n"
            
            return response
            
        except Exception as e:
            current_app.logger.error(f"Error getting payment info: {str(e)}")
            return "I'm having trouble retrieving payment information. Please try again later." 